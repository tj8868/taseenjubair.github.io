/**
 * Prefix an internal path with the configured `base` so links keep working
 * whether the site is served from a project subpath or a domain root.
 */
export function url(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  if (!path.startsWith("/")) return `${base}/${path}`;
  return `${base}${path}`;
}

/** True when `href` is the page currently being rendered. */
export function isActive(href: string, pathname: string): boolean {
  const strip = (s: string) => s.replace(import.meta.env.BASE_URL, "/").replace(/\/+$/, "") || "/";
  return strip(pathname) === strip(href);
}
