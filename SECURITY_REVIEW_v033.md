# DaRoo v033 security review

Static source inspection of v032 only; no live security or Android install test.

- Added HSTS, CSP and Permissions-Policy, retained nosniff/referrer policy, changed frame policy to DENY.
- CSP self-only; no inline scripts/styles or third-party HTML dependencies detected.
- Reader uses textContent and DOM image nodes; no innerHTML injection detected.
- Added 192x192 and 512x512 PWA icons and stable manifest id.
- No login, cookies, service worker, or backend API identified in this static project.
- Cloudflare Pages honors public/_headers when copied into output. Railway/other servers require equivalent response headers configured in their server or proxy; _headers alone may not work.
- HSTS deliberately does not include subdomains/preload, to avoid affecting other Generify services.
- Android install warning cannot be diagnosed conclusively from a header scan.
- Re-test securityheaders.com, Android installation and reader navigation/zoom after deployment.
- No manual deletions; ZipToGit does not remove files.
