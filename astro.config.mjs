import { defineConfig } from 'astro/config';

// PAGES_BASE is set only on the GitHub Pages staging build (e.g. "/eddie-bazil").
// Production (Cloudflare) leaves it empty so the site serves from root.
const base = process.env.PAGES_BASE || '';

export default defineConfig({
  site: 'https://eddiebazil.co.uk',
  base: base || '/',
  trailingSlash: 'ignore',
});
