# Portfolio v2: H M Taseen Jubair Bhuiyan

A static personal site built with **Astro 5** and **Tailwind CSS v4**. Four pages
(About, Publications, Experience, CV), a muted green dark/light theme, and about
2 KB of JavaScript in total.

---

## Table of contents

1. [Quick start](#quick-start)
2. [What each file does](#what-each-file-does)
3. [Editing in an IDE](#editing-in-an-ide)
4. [Common edits, step by step](#common-edits-step-by-step)
5. [Adding your photo](#adding-your-photo)
6. [Adding your CV PDF](#adding-your-cv-pdf)
7. [Changing the colours](#changing-the-colours)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Quick start

You need [Node.js](https://nodejs.org) 20 or newer. Check with `node --version`.

```bash
npm install
npm run dev
```

Open <http://localhost:4321/taseenjubair.github.io/>

Leave `npm run dev` running while you work. Every time you save a file, the browser
updates by itself within a second, you do not need to restart anything or press
refresh. This is called hot reload.

| Command | What it does |
|---|---|
| `npm run dev` | Starts the local preview server. Use this while editing. |
| `npm run build` | Produces the final site in `dist/`. Run before deploying. |
| `npm run preview` | Serves the built `dist/` so you can check the real output. |
| `npm run check` | Type-checks the project and reports errors. |

Press `Ctrl + C` in the terminal to stop the dev server.

---

## What each file does

### The one file you will actually edit

| File | Purpose |
|---|---|
| **`src/data/site.ts`** | **All site content.** Your name, bio, links, stats, skills, every job, every publication, education, contact text. This is the only file you need for normal updates. Lines marked `// TODO` are placeholders still waiting on real values. |

### Pages: one file per URL

Astro maps files in `src/pages/` directly to URLs. Add a file, get a page.

| File | URL | Contains |
|---|---|---|
| `src/pages/index.astro` | `/` | About page: hero, stat cards, background/current-work narrative, research interests, skills grid, contact panel. |
| `src/pages/publications.astro` | `/publications/` | Publications, automatically grouped into Published / Under review / In preparation based on each entry's `status` field. |
| `src/pages/experience.astro` | `/experience/` | Work history as a vertical timeline, plus the education cards. |
| `src/pages/cv.astro` | `/cv/` | Everything condensed into a two-column CV, with Print and Download buttons. |

These files hold **layout only**, the words come from `site.ts`. If you want to
change *what a page says*, edit `site.ts`. Change these only to rearrange sections
or alter how something is displayed.

### Shared building blocks

| File | Purpose |
|---|---|
| `src/layouts/BaseLayout.astro` | The page shell every page wraps itself in: `<head>` tags, SEO and Open Graph metadata, JSON-LD structured data, the theme anti-flash script, the sidebar, the nav, the footer, and the skip-to-content link. Edit this to change something that appears on *every* page. |
| `src/components/Sidebar.astro` | The left column: photo (or initials fallback), name, role, location, bio, social icons, CV button. |
| `src/components/Nav.astro` | The sticky top navigation, the light/dark toggle, and the mobile hamburger drawer. Contains the small script that powers both. |
| `src/components/Icon.astro` | Every icon on the site, as inline SVG paths in one object. No icon font, no network request. To add an icon, add a new entry to the `paths` object and use `<Icon name="yourname" />`. |

### Styling and configuration

| File | Purpose |
|---|---|
| `src/styles/global.css` | Theme colours (the `:root` and `[data-theme="dark"]` blocks at the top), base element styles, and the reusable classes `.panel`, `.card`, `.chip`, `.eyebrow`, `.prose-body`, `.link-underline`, `.btn-primary`, `.btn-secondary`. Also the reduced-motion and print rules. Base and component rules sit inside `@layer base` / `@layer components` so Tailwind utilities can still override them; do not move them out of those layers. |
| `src/lib/url.ts` | Two small helpers. `url()` prefixes internal links with the site's base path so they work on GitHub Pages; `isActive()` tells the nav which link to highlight. You will not normally touch this. |
| `astro.config.mjs` | Site URL, base path, sitemap, and the Tailwind plugin. Edit `SITE` and `BASE` at the top if the site ever moves to a different address. |
| `tsconfig.json` | TypeScript settings. Leave alone. |
| `package.json` | Dependency list and the `npm run` commands. |
| `package-lock.json` | Exact dependency versions. Never edit by hand; npm maintains it. |

### Static files and deployment

| File | Purpose |
|---|---|
| `public/` | Anything here is copied to the site as-is, with no processing. **Your photo and CV PDF go in `public/assets/`.** |
| `public/favicon.svg` | The little icon in the browser tab. |
| `public/.nojekyll` | Empty file that stops GitHub Pages from mangling folders beginning with `_`. Required, do not delete. |
| `.github/workflows/deploy.yml` | Builds and publishes the site automatically whenever you push to `main`. |
| `.gitignore` | Lists files git should ignore, e.g. `node_modules/` and `dist/`. |

### Folders that appear on their own

`node_modules/`, `dist/`, and `.astro/` are all generated. Never edit them, never
commit them. Deleting them is harmless, `npm install` and `npm run build` recreate
them.

---

## Editing in an IDE

### Recommended setup: VS Code

1. Install [VS Code](https://code.visualstudio.com/).
2. Open this folder: **File → Open Folder…** → select `portfolio-v2`.
   Open the folder, not an individual file, or the extensions will not work properly.
3. Install the **Astro** extension: click the Extensions icon in the left bar
   (or `Ctrl + Shift + X`), search for `Astro`, install the one published by
   *astro-build*. This gives syntax highlighting, error checking, and autocomplete
   for `.astro` files.
4. Optionally add **Tailwind CSS IntelliSense** (by *Tailwind Labs*), it autocompletes
   class names and shows you the colour behind each one.
5. Open the built-in terminal with `` Ctrl + ` `` and run `npm run dev`.

Any other editor works too, WebStorm has Astro support built in, and the files are
plain text, so even Notepad would do. VS Code just gives the most help.

### Useful shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + P` | Jump to any file by typing part of its name |
| `Ctrl + Shift + F` | Search across every file |
| `Ctrl + S` | Save, the browser reloads on its own |
| `Ctrl + Z` | Undo |
| `Ctrl + /` | Comment out the selected lines |

### Reading the file format

`.astro` files have two parts:

```astro
---
// Everything between the three dashes is JavaScript/TypeScript.
// It runs once, at build time, on your machine, never in the visitor's browser.
import { profile } from "../data/site";
---

<!-- Below the dashes is HTML. This becomes the actual page. -->
<h1>{profile.name}</h1>
```

Curly braces `{ }` inside the HTML insert a value. `{profile.name}` prints your name.

`.ts` files are TypeScript, JavaScript with type labels. In `site.ts` you are only
ever editing text between quotes, so you can treat it as a structured list.

### Rules to avoid breaking things

- **Keep the quotes.** `name: "Taseen"` is correct; `name: Taseen` breaks the build.
- **Keep the commas** at the end of each line in a list.
- **Use a backslash before an apostrophe inside single quotes**, or just use double
  quotes: `"Cox's Bazar"` is fine, `'Cox's Bazar'` is not.
- **Do not delete a `{`, `}`, `[`, or `]`** unless you are deleting the whole block.
- If something breaks, the terminal running `npm run dev` prints the file and line
  number. `Ctrl + Z` gets you back.

---

## Common edits, step by step

**Change a sentence on the About page**
Open `src/data/site.ts` → find `about` → edit the text inside `lead` or `paragraphs`.

**Add a new job**
In `site.ts`, find `experience`. Copy an existing block from `{` to `},` and paste it
above the others (newest first). Change the fields. Set `current: true` only on your
present role, it draws the glowing dot and the "Current" badge.

**Add a publication**
In `site.ts`, find `publications`. Copy an existing entry and edit it. `status` must be
exactly `"published"`, `"review"`, or `"prep"`, that is what sorts it into the right
group. Add a `href: "https://doi.org/..."` to make the "View publication" link appear.

**Add a skill**
In `site.ts`, find `skills`, then the right group, and add `"Your skill",` to its
`items` list.

**Rename or reorder the menu**
In `site.ts`, edit the `nav` list. To *remove* a page entirely you must also delete the
matching file in `src/pages/`.

**Change the footer**
Bottom of `src/layouts/BaseLayout.astro`.

---

## Adding your photo

1. Put the image in `public/assets/`, for example `public/assets/taseen.jpg`.
   Square, at least 400 × 400, JPG or WebP.
2. In `src/data/site.ts`, change:

   ```ts
   photo: null,
   ```

   to:

   ```ts
   photo: "assets/taseen.jpg",
   ```

   The path has no leading slash, and must match the filename exactly, including
   capitals and the extension.
3. Save. Until you do this the sidebar shows your initials instead.
4. Commit and push to publish it.

Only you can change the photo, because changing it means pushing to this repository.
There is no upload form and no login, nothing to attack and nothing to leak.

## Adding your CV PDF

Same pattern: put the PDF in `public/assets/`, then set
`resume: "assets/your-cv.pdf"` in `src/data/site.ts`. That switches on the sidebar
download button and the one on the CV page. The CV page's Print button already works
without any PDF.

---

## Changing the colours

Every colour is defined once, at the top of `src/styles/global.css`:

- the `:root { }` block is **light mode**
- the `[data-theme="dark"] { }` block is **dark mode**

Change a value in one place and it updates everywhere on the site.

| Variable | Controls |
|---|---|
| `--bg` | Page background |
| `--fg` | Normal text |
| `--fg-strong` | Headings |
| `--muted` | Secondary text, captions |
| `--accent` | Links, highlights, buttons |
| `--border` | Card and divider lines |
| `--surface` | Translucent card backgrounds |

If you change `--bg` or `--accent`, check the contrast between text and background at
<https://webaim.org/resources/contrastchecker/>, aim for 4.5:1 or higher so the site
stays readable. Also update the two `theme-color` meta tags in
`src/layouts/BaseLayout.astro` so the mobile browser bar matches.

Dark is the default. On a first visit the site follows the visitor's operating system
preference, then remembers whatever they pick with the toggle.

---

## Deployment

`.github/workflows/deploy.yml` builds and publishes to GitHub Pages on every push to
`main`. One-time setup in the GitHub repository: **Settings → Pages → Source →
GitHub Actions**.

To publish a change:

```bash
git add .
git commit -m "Update publications"
git push
```

Then watch the **Actions** tab. It takes a minute or two.

The site is configured for `https://tj8868.github.io/taseenjubair.github.io/`. If you
move to a custom domain or a user site, edit `SITE` and `BASE` at the top of
`astro.config.mjs`, for a domain root, `BASE` becomes `"/"`.

---

## Troubleshooting

**The page is blank or unstyled**
Check the terminal running `npm run dev` for a red error, then fix the file and line
it names.

**`npm run dev` says the port is in use**
Another copy is already running. Close the other terminal, or use
`npm run dev -- --port 4322`.

**Changes are not showing**
Confirm you saved, and that you are on <http://localhost:4321/taseenjubair.github.io/>
including the trailing path. Failing that, stop the server and start it again.

**The photo does not appear**
The filename in `site.ts` must match the real file exactly, `Photo.JPG` and
`photo.jpg` are different. The file must be inside `public/assets/`, and the path in
`site.ts` must have no leading slash.

**Everything is broken and you want to start over**
Delete `node_modules/` and `dist/`, then run `npm install`. Your content in
`site.ts` is untouched by this.
