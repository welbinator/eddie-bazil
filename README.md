# Eddie Bazil

Personal brand site for **Eddie Bazil** — sound designer, mix engineer, mastering engineer and educator with 35+ years of experience. Built with Astro (static).

## Design system
Warm editorial ("ElevenLabs" refero reference): eggshell paper canvas, whisper-weight display type (Fraunces), Inter body, hairline borders, violet→orange audio-sphere motif for graphics only. Mobile-first, scroll-reveal fails open.

## Develop
```bash
npm install
npm run dev      # local dev
npm run build    # static build to dist/
npm run preview
```

## Deploy
- **Production:** Cloudflare Pages (base path empty, indexable).
- **Staging:** GitHub Pages via `staging` branch → `.github/workflows/deploy-staging.yml` (noindex injected at build time, `PAGES_BASE=/eddie-bazil/`).

## Scripts
- `scripts/dedash.py` — verifies no em/en dashes in source (anti-AI-slop rule).
