# Portfolio Navigation, Research & Tools Restructure

* **Author:** H M Taseen Jubair Bhuiyan (`tj8868`)
* **Date:** 2026-11-26

## The Problem

The current portfolio site (`About`, `Content`, `Publications`, `Experience`, `CV`) has three structural weaknesses for academic admissions and AI/research engineering audiences:

1. **Unclear Navigation Labels:** `Content` does not communicate what is on the page, while cross-platform AI agents, workflows, and plugins have no dedicated home.
2. **Pre-University Clutter & Research Scope:** Including SSC and HSC dates creates unnecessary timeline noise on an academic portfolio, and the current `Publications` page lacks a structured way to present preprints and ongoing research topics without exposing unpublished paper titles.
3. **Mixed Experience Hierarchy:** Work history, day-to-day activities, and AI engineering tooling (agentic harnesses and Spec-Driven Development) are not cleanly separated between the Home page, `Experience`, and `Tools`.

## Overview

This design restructures the portfolio's top-level navigation to **About**, **Research & Publications**, **Tools**, **Experience**, and **CV**. It removes pre-university SSC and HSC entries from Education, expands **Research & Publications** into three clear tiers (Peer-Reviewed, Preprints, and Current Research Focus), introduces a dedicated **Tools** page for cross-platform AI agents, workflows, and plugins, and keeps **Experience** focused on roles and day-to-day impact with a concise highlight on the Home page.

## Goals

* **Update Top Navigation:** Set the primary header links to `About`, `Research & Publications`, `Tools`, `Experience`, and `CV`, with responsive layout support on narrow mobile viewports.
* **Clean Education Timeline:** Remove SSC and HSC entries from both the frontend data and FastAPI CMS seed/records, retaining university degrees (M.Sc. and B.Sc. with graduation year `2024`).
* **Structured Research & Publications:** Organize research outputs into `Peer-Reviewed`, `Preprints`, and `Current Research Focus` using topic-level descriptions for unpublished work.
* **Dedicated Tools Catalog:** Create `/tools/` to showcase cross-platform AI agents, workflows, plugins, and agentic harnesses (Claude, Gemini, Codex, Hermes Agent, Antigravity, DeepSeek Harness, Pi, OpenCode) alongside Spec-Driven Development.
* **Single Source of Truth:** Ensure Experience highlights on the Home page and the full `Experience` page read from one shared data source.
* **Backward-Compatible Routes:** Preserve or redirect legacy `/content/` and `/publications/` URLs so existing external links do not 404.

## Non-Goals

* Building an interactive e-commerce marketplace, user accounts, or payment/install backend.
* Exposing verbatim unpublished paper titles on the public site.
* Bundling full plugin source code or large READMEs into the Astro client bundle.

## Technical Plan

### Architecture & Data Flow

The portfolio remains a static Astro 5 site (`frontend/`) built from `frontend/src/data/site.ts` and `frontend/src/data/cms-snapshot.json` (which is updated by the local FastAPI CMS in `backend/`).

```
+-----------------------------------+
|  Single Source of Truth (Data)    |
|  - frontend/src/data/site.ts      |
|  - frontend/src/data/cms-snapshot |
+-----------------+-----------------+
                  |
        +---------+---------+-------------------+
        |                   |                   |
        v                   v                   v
+---------------+   +---------------+   +---------------+
|  Home (About) |   |  Experience   |   |     Tools     |
|  Summary view |   |  Full roles & |   |  Catalog +    |
|  (3 bullets)  |   |  activities   |   |  Harnesses    |
+---------------+   +---------------+   +---------------+
```

### Component & Route Changes

1. **Navigation (`frontend/src/data/site.ts`, `frontend/src/components/Nav.astro`)**
   - Update `nav` array to:
     - `About` (`/`)
     - `Research & Publications` (`/research/`)
     - `Tools` (`/tools/`)
     - `Experience` (`/experience/`)
     - `CV` (`/cv/`)
   - Keep `Nav.astro` responsive drawer/collapse behavior so multi-word labels (`Research & Publications`) do not wrap awkwardly on 320px–375px viewports.

2. **Education Cleanup (`frontend/src/data/site.ts`, `frontend/src/data/cms-snapshot.json`, `backend/app/seed.py`)**
   - Remove SSC and HSC entries from `education` arrays and database seed records.
   - Retain M.Sc. (Jahangirnagar University) and B.Sc. (RUET, `2024`).

3. **Research & Publications (`frontend/src/pages/research.astro`, legacy `/publications/` redirect)**
   - Replace `publications.astro` with `research.astro` (and keep `publications.astro` as a lightweight static redirect to `/research/` so existing links do not 404).
   - Group entries into three sections:
     - **Peer-Reviewed Publications** (with DOI/journal links)
     - **Preprints & Under Review** (with `(Preprint / Preparing for journal resubmission)` status tags)
     - **Current Research Focus** (topic-level descriptions only; no verbatim unpublished titles)

4. **Tools Catalog (`frontend/src/pages/tools.astro`, `frontend/src/data/tools.ts`)**
   - Add a typed static data module `frontend/src/data/tools.ts` with schema:
     `{ id, name, category: 'agent' | 'workflow' | 'plugin' | 'harness', platforms: string[], summary, repoUrl, lastVerified }`.
   - Render `tools.astro` with:
     - **Agentic Harnesses** (Hermes Agent, Claude, Codex, Antigravity, DeepSeek Harness, Pi, OpenCode) with 1-line plain-English explanations.
     - **Workflows (Spec-Driven Development)** explaining specification-first execution.
     - **Agents & Plugins Catalog** with platform filter chips (reusing the existing chip pattern from `content.astro`) and external GitHub links.
   - Keep `/content/` accessible via a legacy redirect or footer link if needed.

5. **Experience & Home Mirroring (`frontend/src/pages/experience.astro`, `frontend/src/pages/index.astro`)**
   - `experience.astro` renders roles, appointments, and day-to-day activities from the shared `site.ts` data.
   - `index.astro` renders a bounded 3-bullet highlight (Current Role, Core Harnesses, Spec-Driven Workflow) from the same data source, linking to `/experience/` and `/tools/`.

### Visual Alignment & Consistency Rules

* **Shared Layout & Typography:** All pages (`index.astro`, `research.astro`, `tools.astro`, `experience.astro`, `cv.astro`) must use `BaseLayout.astro` with the exact same eyebrow-header pattern (`<p class="eyebrow">`, `<h2>` scale, and `max-w-[68ch]` intro paragraph).
* **Card & Grid Symmetry:** `tools.astro` and `research.astro` must reuse the existing `.card`, `.panel`, and `.chip` classes from `global.css` so spacing, borders, and dark/light theme colors match `experience.astro` and `content.astro`.
* **Navigation Bar Alignment:** `Nav.astro` must keep all 5 top-level items on a single horizontal row at desktop widths (`>= 1024px`) using `whitespace-nowrap`, and collapse cleanly into the mobile menu below that breakpoint.

## Alternatives Considered

1. **Keep `Content` / Rename to `YouTube` as a 6th Top-Level Nav Item**
   * **Rejected because:** Adding a 6th item crowds the horizontal navigation bar on laptops and tablets, especially with multi-word labels like `Research & Publications`. Additionally, `/content/` currently holds mixed media (LinkedIn posts, articles, talks), so renaming it `YouTube` would mislabel non-video items. Keeping `/content/` accessible as a legacy route or footer link avoids breaking bookmarks without cluttering the header.

2. **Name the Catalog "Agent Marketplace" and Embed It Inside `Experience`**
   * **Rejected because:** "Marketplace" implies a live storefront, pricing, or third-party submissions, which misleads visitors for a static catalog of personal repos. Embedding a full tool/harness inventory at the top of `Experience` also buries actual work and research appointments. Separating `Tools` into its own page keeps `Experience` focused on roles and impact while giving AI harnesses and Spec-Driven Development a clear home.

3. **Duplicate `Experience` HTML/Markdown Directly on the Home Page**
   * **Rejected because:** Maintaining two separate copies of roles, tools, and day-to-day activities guarantees content drift over time and bloats the landing page. Using a single canonical data source (`site.ts` / `cms-snapshot.json`) with a bounded 3-bullet summary on `index.astro` eliminates drift.

## Detailed Implementation

1. **`frontend/src/data/site.ts`**
   * **Change:** Update `nav` array to `About` (`/`), `Research & Publications` (`/research/`), `Tools` (`/tools/`), `Experience` (`/experience/`), `CV` (`/cv/`). Remove SSC and HSC entries from `education`, keeping M.Sc. and B.Sc. (`2024`). Add `researchFocus` topic-level bullets and `experienceHighlights` (3-bullet summary) for the Home page.
   * **Rationale:** Establishes a single canonical data source for navigation, cleaned education, research focus, and Home/Experience alignment.

2. **`frontend/src/data/cms-snapshot.json` & `backend/app/seed.py`**
   * **Change:** Remove SSC and HSC records from the seed data and snapshot JSON so the FastAPI CMS and Astro build stay in sync.
   * **Rationale:** Prevents pre-university entries from reappearing when the CMS regenerates `cms-snapshot.json`.

3. **`frontend/src/data/tools.ts`** *(New File)*
   * **Change:** Define typed arrays for `harnesses` (Hermes Agent, Claude, Codex, Antigravity, DeepSeek Harness, Pi, OpenCode), `workflows` (Spec-Driven Development), and `catalogItems` (`id`, `name`, `category`, `platforms`, `summary`, `repoUrl`, `lastVerified`).
   * **Rationale:** Separates the Tools catalog schema from `site.ts` and enables build-time TypeScript validation.

4. **`frontend/src/components/Nav.astro`**
   * **Change:** Apply `whitespace-nowrap` to desktop nav links (`>= 1024px`) and verify mobile drawer collapse below `1024px`.
   * **Rationale:** Prevents multi-word labels (`Research & Publications`) from wrapping unevenly across viewports.

5. **`frontend/src/pages/research.astro`** *(New File)* & **`frontend/src/pages/publications.astro`**
   * **Change:** Create `research.astro` using `BaseLayout.astro` and `.card`/`.panel` classes, rendering three sections: `Peer-Reviewed Publications`, `Preprints & Under Review`, and `Current Research Focus` (topic-level only). Convert `publications.astro` into a static redirect (`<meta http-equiv="refresh" content="0;url=/research/" />`).
   * **Rationale:** Delivers the expanded Research & Publications page while preserving backward compatibility for `/publications/` links.

6. **`frontend/src/pages/tools.astro`** *(New File)*
   * **Change:** Create `tools.astro` using `BaseLayout.astro` and `.card`/`.chip` classes to display Agentic Harnesses, Spec-Driven Development workflow, and filterable cross-platform Agents & Plugins.
   * **Rationale:** Gives AI tooling and workflows a dedicated home without cluttering `Experience`.

7. **`frontend/src/pages/index.astro` & `frontend/src/pages/experience.astro`**
   * **Change:** Update `index.astro` to render the bounded 3-bullet `experienceHighlights` summary linking to `/experience/` and `/tools/`. Keep `experience.astro` focused on roles, appointments, and day-to-day activities.
   * **Rationale:** Ensures visual consistency and eliminates duplicate content maintenance.

8. **Verification**
   * **Change:** Run `npm --prefix frontend run build` (on Linux after `npm install` in `frontend/` or via GitHub Actions) and verify zero broken links, clean 320px–1280px nav alignment, and absence of SSC/HSC on all pages.
   * **Rationale:** Confirms static build integrity and responsive layout before deployment.
