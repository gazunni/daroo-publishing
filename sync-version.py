#!/usr/bin/env python3
"""Synchronize visible app version from public/version.json; run before every ZipToGit release."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parent
version=json.loads((root/'public/version.json').read_text())['version']
for p in (root/'public').glob('*.html'):
    s=p.read_text()
    s,n=re.subn(r'(<span class="app-version" aria-label="Application version )[^"]+(">)v[^<]+(</span>)',lambda m:m.group(1)+version+m.group(2)+'v'+version+m.group(3),s)
    if n!=1:raise RuntimeError(f'Expected exactly one version label in {p.name}; got {n}')
    p.write_text(s)
print(f'Version v{version} synchronized across site pages')
