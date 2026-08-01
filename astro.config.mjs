// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages project site: https://tj8868.github.io/taseenjubair.github.io/
// If you ever move to a user site (tj8868.github.io) or a custom domain,
// set BASE to "/" and update SITE.
const SITE = "https://tj8868.github.io";
const BASE = "/taseenjubair.github.io";

export default defineConfig({
  site: SITE,
  base: BASE,
  trailingSlash: "always",
  build: { format: "directory" },
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
  compressHTML: true,
  prefetch: {
    prefetchAll: true,
    defaultStrategy: "hover",
  },
});
