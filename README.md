# DaRoo Publishing — v0.1.0

Static GitHub → Cloudflare Pages publishing site for **daroo.generify.ca**.

## ZipToGit deployment
Upload the complete `DaRoo_v010_ZipToGit_full.zip` directly into ZipToGit. Its single `DaRoo_v010/` wrapper is removed automatically, placing `public/` and `deploy.info` at repository root. The site remains undeployed until GitHub and Cloudflare are configured.

## Deploy
1. Create GitHub repository `daroo-publishing` and upload the contents of this project (not the zip itself).
2. Cloudflare dashboard → Workers & Pages → Create → Pages → Connect to Git → choose repository.
3. Framework: None; production branch: `main`; build command: `exit 0`; output directory: `public`.
4. After deployment, Pages project → Custom domains → add `daroo.generify.ca`. Confirm Cloudflare DNS association.
5. New commits to `main` automatically deploy. Pull requests may receive preview URLs.

## Distribution architecture
- `public/index.html`: imprint landing, series and library
- `public/reader.html`: keyboard/swipe/slider reader, fullscreen and optional spread
- `public/books/gabe-and-jinx/book-01/manifest.json`: sample book catalog
- `public/assets/`: site assets
- Published art: later store in R2 at `assets.daroo.generify.ca` or another chosen asset domain and set absolute HTTPS `image` URLs in manifests. No R2 required for demo.

## Publishing a book
Add a manifest JSON with `pages` array. Each page accepts `number`, `title`, `description`, and optional `image` (absolute URL or site-relative path) and `alt`. Set `status` to `published` only after final art and editorial approval. Add book ID/path to the allowlist in `public/assets/reader.js`, and a card in `index.html`. No CMS or user accounts in v0.1.

## Important
- Book pages are intentionally text-only placeholders; no generated storyboards or master photograph are published.
- Current logo and cover are **temporary typographic/CSS concepts**, not the approved DaRoo kangaroo-smash logo. Replace with approved production assets later.
- `The Eye of the Desert` is a working title.
- No secrets, keys, analytics or database are required.
- Static assets on Pages have a per-file size limit; R2 is planned for full-resolution books.

## Local test
Run `python3 -m http.server 8000 -d public` and visit `http://localhost:8000`. Opening `index.html` directly as a file will not load the JSON reader manifest.
