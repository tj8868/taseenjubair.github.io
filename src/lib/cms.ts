/**
 * Build-time content loader.
 *
 * Pulls Profile / About / Education / Content from the FastAPI backend while
 * `astro build` runs and bakes the result into static HTML. Nothing is fetched in
 * the browser, so the published site works with the backend switched off.
 *
 * Three sources, tried in order, so a build never fails and never silently ships
 * stale-but-wrong content:
 *
 *   1. The live API. On success the payload is saved to `src/data/cms-snapshot.json`.
 *   2. That snapshot file. This is what makes the GitHub Actions deploy work, since
 *      the runner cannot reach a backend running on your laptop. Commit it.
 *   3. `src/data/site.ts`, the original hand-written content.
 */

import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

import {
  profile as fallbackProfile,
  about as fallbackAbout,
  education as fallbackEducation,
} from "../data/site";

const CMS_URL = (import.meta.env.PUBLIC_CMS_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
const TIMEOUT_MS = 4000;
// Resolved from the project root, not from import.meta.url: this module gets
// bundled into dist/chunks/ during a build, so a module-relative path would
// write the snapshot into dist/ and it would never be committed.
const SNAPSHOT_PATH = resolve(process.cwd(), "src/data/cms-snapshot.json");

export type Profile = {
  name: string;
  shortName: string;
  kicker: string;
  role: string;
  location: string;
  bio: string;
  photo: string | null;
  photoAlt: string;
  resume: string | null;
};

export type About = {
  lead: string;
  sections: { heading: string; paragraphs: string[] }[];
  interests: string[];
};

export type EducationEntry = {
  degree: string;
  school: string;
  note: string | null;
  year: string;
};

export type ContentItem = {
  id: number;
  platform: string;
  platformLabel: string;
  title: string;
  description: string;
  url: string;
  videoId: string | null;
  thumbnail: string | null;
  publishedAt: string;
  tags: string[];
  featured: boolean;
};

export type Payload = {
  profile: Profile;
  about: About;
  education: EducationEntry[];
  content: ContentItem[];
};

export type Site = Payload & {
  /** Where the content came from. Reported in the build log. */
  source: "api" | "snapshot" | "site.ts";
};

const hardcoded: Payload = {
  profile: { ...fallbackProfile },
  about: fallbackAbout,
  education: fallbackEducation,
  content: [],
};

async function fromApi(): Promise<Payload> {
  const res = await fetch(`${CMS_URL}/api/site`, { signal: AbortSignal.timeout(TIMEOUT_MS) });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return (await res.json()) as Payload;
}

function saveSnapshot(payload: Payload): void {
  try {
    writeFileSync(SNAPSHOT_PATH, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  } catch (err) {
    console.warn(`[cms] could not write the snapshot: ${String(err)}`);
  }
}

function fromSnapshot(): Payload | null {
  try {
    return JSON.parse(readFileSync(SNAPSHOT_PATH, "utf8")) as Payload;
  } catch {
    return null;
  }
}

async function resolveSite(): Promise<Site> {
  try {
    const payload = await fromApi();
    saveSnapshot(payload);
    console.info(`[cms] content loaded from ${CMS_URL} and snapshotted.`);
    return { ...payload, source: "api" };
  } catch (err) {
    const reason = err instanceof Error ? err.message : String(err);
    const snapshot = fromSnapshot();
    if (snapshot) {
      console.info(`[cms] ${CMS_URL} unreachable (${reason}): using cms-snapshot.json.`);
      return { ...snapshot, source: "snapshot" };
    }
    console.warn(
      `[cms] ${CMS_URL} unreachable (${reason}) and no snapshot found: using src/data/site.ts.`
    );
    return { ...hardcoded, source: "site.ts" };
  }
}

let cached: Promise<Site> | null = null;

/** Memoised so a multi-page build hits the API once, not once per page. */
export function getSite(): Promise<Site> {
  cached ??= resolveSite();
  return cached;
}
