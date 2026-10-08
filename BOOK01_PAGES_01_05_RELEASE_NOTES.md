# Book One — Pages 1–5 reader integration

This build inserts five separate page images into the existing DaRoo reader, replacing the four-item development-preview manifest. It preserves the existing site navigation and reader controls.

IMPORTANT: The five supplied artwork sources are enlarged storyboard proofs, not independently re-rendered print-resolution masters. This build is a functional website review release, NOT certified print-production artwork. Do not label it publication-ready.

ZipToGit MANUAL DELETIONS: NONE REQUIRED. Existing old preview assets are left in place and unreferenced; do not delete them until separately authorized.

Changed files:
- public/assets/images/gabe-jinx-book01-page-01.webp
- public/assets/images/gabe-jinx-book01-page-02.webp
- public/assets/images/gabe-jinx-book01-page-03.webp
- public/assets/images/gabe-jinx-book01-page-04.webp
- public/assets/images/gabe-jinx-book01-page-05.webp
- public/books/gabe-and-jinx/book-01/manifest.json
- public/assets/reader.js

Validation: JSON manifest parse, five referenced images exist, image decoding, JS syntax check.
