# DaRoo Publishing — v0.2.0

Production domain: https://daroo.generify.ca

Static Cloudflare Pages site deployed via GitHub and ZipToGit.

## Deployment
Upload the **full** ZipToGit ZIP to `daroo-publishing` / `main`. ZipToGit strips the single outer wrapper directory. Cloudflare Pages: build command `exit 0`, output directory `public`. No secrets or environment variables required.

## Preview policy
All artwork on the site is **development concept/storyboard imagery**, not approved final comic pages. The 1926 photograph displayed in the reader is an annotated development reference. Replace with approved production-ready art when available. The book is not published.

## Reader
Responsive image-first reader with swipe, arrows, slider, fullscreen, fit-width, and two-page layout on screens >= 800px. Catalog JSON controls pages and status. Images currently stored under `public/assets/images/`; Cloudflare R2 can be added later.

## Versioning
Full ZIP = entire repository. Changed ZIP = changed/new files only; no deletions in this release. Both have a single wrapper directory. `.env.example` unchanged.
