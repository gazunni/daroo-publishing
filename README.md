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


v0.2.8: Replace header text wordmark with approved DaRoo logo on all four site pages; show supplied original artwork on Imprint; remove redundant footer above fixed bottom navigation. Reader and book assets unchanged.


v0.2.9: Reduced space between header and content on Imprint and Stories. Added iPad Home Screen standalone web-app metadata, manifest and icon. iPad Safari cannot be programmatically forced into fullscreen; users must use Share > Add to Home Screen > Open as Web App when offered.


## v032 — Site presentation
- The Imprint is condensed into a portrait-friendly layout with tighter typography, spacing and artwork size.
- Stories uses one new Book One illustration instead of the storyboard collage.
- Reader and five page assets remain unchanged from v031.
- ZipToGit FULL and CHANGED packages share the same repository root. No manual deletions; .env.example unchanged.

## v033 security update
See SECURITY_REVIEW_v033.md.

## Application versioning policy (introduced v0.3.4)
- Source of truth: `public/version.json` (`version` and `release`).
- Every website change increments the semantic version and updates the release history below, `DEPLOYED.md`, `CHANGED_FILES.txt`, and the two ZipToGit packages.
- Before packaging, run `python sync-version.py` to update the visible bottom-right version label on every HTML page, including the reader.
- The visible label reflects the **packaged version**, not an independently verified live deployment. Verify after deploying and refresh stale browser caches if needed.
- The release history should include date, version, scope and verification status.

### Release history
| Date | Version | Change | Status |
| --- | --- | --- | --- |
| 2026-10-08 | v0.3.4 (ZipToGit v034) | Fixed-menu version label, centralized version metadata, synchronization script and release logging | Packaged; live deployment not verified |
| 2026-10-08 | v0.3.3 (ZipToGit v033) | Security response headers, installable-app icons and manifest update | Previous package |
| 2026-10-08 | v0.3.2 (ZipToGit v032) | Compressed Imprint layout and single story illustration | Previous package |

| 2026-10-08 | v0.3.5 (ZipToGit v035) | Compact Main landing layout; replace obsolete storyboard with original story artwork; keep site header/navigation | Packaged; live review pending |

## v0.3.6 — Responsive landing hero repair (2026-10-08)
Merged hero copy and artwork into one layered responsive section, preventing separate black text block and excessive portrait crop. Preserved site header, reader, bottom nav and other pages. Package prepared; deployment not verified.

## v0.3.7 — Hero image composition correction (2026-10-08)
Replaced cropped mockup-derived hero art with clean artwork in separate landscape and portrait WebP assets. Existing HTML header and fixed navigation remain; responsive artwork uses `<picture>` and one overlaid HTML copy layer. Package prepared; live layout review pending.

## v0.3.8 — Contained hero image layout (2026-10-08)
Removed background-style cover cropping; artwork is a normal proportional image. Wide screens use text and artwork side by side; portrait screens stack text above the entire illustration. Fixed navigation and header preserved. Static checks only; live device review pending.
