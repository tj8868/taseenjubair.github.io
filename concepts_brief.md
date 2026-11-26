# Portfolio Navigation & Content Restructure

* **Author:** H M Taseen Jubair Bhuiyan (`tj8868`)
* **Date:** 2026-11-26

## Overview

This proposal restructures the portfolio's top-level navigation to **About**, **Research & Publications**, **Tools**, **Experience**, and **CV**, while removing pre-university SSC and HSC entries from Education. It expands **Research & Publications** into Peer-Reviewed, Preprints, and Current Research Focus; introduces **Tools** as a dedicated static catalog of cross-platform AI agents, workflows, plugins, and Spec-Driven Development harnesses (Claude, Gemini, Codex, Hermes, Antigravity, DeepSeek Harness, Pi, OpenCode); and keeps **Experience** focused on roles, appointments, and day-to-day impact, with a concise summary on the Home page.

## Analysis

Six independent Goldfish reviews identified the following structural, UX, and maintenance risks:

1. **Dual-Source-of-Truth & Content Drift (Home vs. Experience):** Mirroring `Tools & Skills`, `Workflows`, and `Day-to-Day Activities` on both the Home page and the `Experience` page creates a high risk of content drift and bloated landing-page DOM if authored separately. Both views must consume a single canonical data source (e.g., Astro Content Collections or a shared `src/data/` module), with the Home page rendering a bounded summary rather than duplicating the full page.
2. **Naming & Mental Model Mismatch:**
   - **Agent Marketplace:** Visitors expect a live store, pricing, or 1-click installs. For a static catalog of personal repos/configs, naming it *Agent Marketplace* risks user confusion unless paired with an explicit 1-line subtitle (or renamed to *Agent Catalog* / *AI Workflows & Plugins*).
   - **Experience:** Ordering `Experience` as *Tools & Skills → Workflows → Day-to-Day Activities* breaks the standard convention where "Experience" means *Work History*. If work history remains in `CV` or below `Day-to-Day Activities`, the hierarchy should be explicit.
3. **Undefined Niche Terms:** Terms like *agentic harnesses*, *Hermes Agent*, *Antigravity*, *DeepSeek Harness*, *Pi*, *OpenCode*, and *Spec-Driven Development* are opaque to academic PIs or general recruiters. Each needs a plain-English 1-line explanation or link.
4. **Preprint & Ongoing Work Privacy Risk:** Including "ongoing work hints" on a public static site risks leaking unpublished paper titles verbatim. Ongoing work must use generalized topic descriptions and explicit status tags (`published`, `preprint`, `ongoing`) rather than verbatim unpublished titles.
5. **Broken Deep Links & Navigation Density:** Replacing `Content` and renaming `Publications` to `Research & Publications` can break existing bookmarks or anchor links (`#publications`, `/content/`). Legacy routes/anchors should be preserved or redirected. Additionally, multi-word nav labels (`Research & Publications`, `Agent Marketplace`) require responsive mobile drawer/collapse rules at 320px–375px viewports.
6. **Marketplace Schema & Bundle Size:** A static catalog of 4+ platforms and 3 artifact types (agents, workflows, plugins) needs a strict, validated schema (`id`, `title`, `type`, `platforms[]`, `status`, `repo_url`, `summary`, `last_verified`) and should link out to GitHub repos rather than bundling full manifests/READMEs into the initial page load.

## Goals vs. Non-Goals

* **In-Scope Goals:**
  - Update top navigation to: `About`, `Research & Publications`, `Agent Marketplace`, `Experience`, `CV`.
  - Remove pre-university SSC and HSC entries from Education (retaining M.Sc. and B.Sc. with graduation year `2024`).
  - Expand `Research & Publications` to list published manuscripts, preprints, and topic-level ongoing work with explicit status tags.
  - Add `Agent Marketplace` as a static, schema-validated catalog of cross-platform AI agents, workflows, and plugins.
  - Reorder `Experience` as `Tools & Skills` (agentic harnesses) → `Workflows` (Spec-Driven Development) → `Day-to-Day Activities`, with a shared data source mirrored on the Home page.
* **Out-of-Scope Non-Goals:**
  - Building an interactive e-commerce marketplace, user accounts, or payment/install backend.
  - Exposing verbatim unpublished paper titles on the public site.
  - Duplicating full READMEs or plugin code inside the Astro client bundle.

## Alternatives Weighed

* **Keep `Content` / Rename to `YouTube` in Top Nav:** Rejected as a 6th top-level nav item because it crowds narrow viewports and mixes YouTube videos with non-video posts; `/content/` can remain accessible via footer/redirect if needed.
* **Merge `Agent Marketplace` into `Projects` or `Tools`:** Weighed as a simpler YAGNI option; kept as a dedicated section/page to highlight cross-platform AI agent tooling, provided it uses a lightweight, schema-validated static list linking to GitHub.
* **Duplicate HTML/Markdown between Home and `Experience`:** Rejected due to guaranteed content drift; replaced with a single canonical data source.

## Key Decisions & Staging for Next Steps

* **Single Source of Truth:** Experience data (`Tools & Skills`, `Workflows`, `Day-to-Day Activities`) and `Agent Marketplace` items must live in a single canonical data file/collection with build-time validation.
* **Privacy Rule:** Ongoing research entries must use topic-level descriptions and standardized status enums (`published`, `preprint`, `ongoing`).
* **Route Compatibility:** Preserve or redirect legacy `/content/` and `/publications/` paths so existing links do not 404.
