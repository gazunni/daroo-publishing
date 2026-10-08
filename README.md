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


## v0.2.1 Reader and branding
- Approved DaRoo logo supplied by publisher (not regenerated).
- One image per reader step, portrait-first; optional two-image spread at >=900px.
- Pointer-based pinch zoom, double-tap, zoom controls (100%-400%), pan while zoomed, swipe only at 100%.
- Development image assets are still contact sheets. Replace with individual full-resolution page files in the book manifest as artwork is finalized.
- iPad Safari fullscreen availability varies; browser zoom gestures are handled within reader stage.

## v0.2.2 lint hotfix
Fixed unused variables ignoreClick and old; explicitly qualified window.innerWidth in reader.js. No UI changes. .env.example unchanged.

## v0.2.3 Page 1 deployment preview
- Reader first item now Page 1 five-panel artwork draft, followed by three clearly labelled historical concept previews.
- Original Page 1 screenplay transcription at `public/books/gabe-and-jinx/book-01/page-01-script.txt`.
- Visual draft is NOT final: panel 3 does not depict 16:17/pedestrian interruption; panel 5 shows more of Jinx than the screenplay allows. Lettering not baked into art.
- No changes to `.env.example`; deployment remains GitHub/ZipToGit to Cloudflare Pages, output `public`.


## v0.2.4 Page 1 lettering preview
Original screenplay lettering is added as responsive HTML overlay, not burned into the image. Page 1 panel 3 and panel 5 artwork are still not screenplay-accurate; this is a website/lettering preview, not final approved art.

## v0.2.5 Page 1 lettering
Lettering is rendered as a responsive SVG using artwork coordinates; location moved into open sky, Gabe dialogue to the lower left of panel 2, and courier dialogue to the left of panel 4. The intrusive development caption is removed from the image. No changes to .env.example. Art remains a preview.


v0.2.6: Fixed detached lettering by baking Page 1 captions into the page artwork. The original unlettered preview remains available. Panel 3 and Panel 5 art are still pending correction.


## v0.2.7: Multi-page site

Four dedicated routes: `/` (Main), `/stories.html`, `/imprint.html`, `/disclaimers.html`. Fixed bottom navigation across all pages, including the comic reader. Disclaimer text is editorial draft pending rights/legal review before commercial print.
