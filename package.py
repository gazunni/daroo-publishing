#!/usr/bin/env python3
"""DaRoo release packager.  Run from the repository root:

    python package.py

Never zip a release by hand.  This script:
  1. checks the release is consistent (version, labels, manifest, file lists);
  2. regenerates PROJECT_TREE.txt;
  3. builds two ZipToGit packages in ./dist/ :
       daroo-publishing-<release>-CHANGED.zip   (files named in CHANGED_FILES.txt)
       daroo-publishing-<release>-FULL.zip      (the whole repository)
  4. re-opens both zips and verifies them;
  5. prints the manual GitHub deletions from MANUAL_DELETIONS.txt.

Both zips contain ONE wrapper directory, daroo-publishing-main/ (ZipToGit strips it).
Nothing is written to ./dist/ if any check fails.  Exit code 0 = ready, 1 = fix the errors.

Release routine for whoever (or whatever) makes the next release:
  - edit files; bump public/version.json (version, release, previous_version, notes)
  - list every changed/new file in CHANGED_FILES.txt (first line is a title)
  - list anything to delete on GitHub in MANUAL_DELETIONS.txt
  - run:  python package.py
"""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WRAPPER = "daroo-publishing-main"
DIST = ROOT / "dist"
SKIP_NAMES = {"deploy.info", ".DS_Store"}      # deploy.info is written by ZipToGit, never shipped
SKIP_DIRS = {"dist", ".git", "__pycache__", "node_modules"}

errors = []


def err(msg):
    errors.append(msg)


def repo_files():
    out = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if set(rel.parts[:-1]) & SKIP_DIRS or p.name in SKIP_NAMES:
            continue
        out.append(rel.as_posix())
    return out


def read_list(name, skip_first=False):
    p = ROOT / name
    if not p.exists():
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    if skip_first:
        lines = lines[1:]
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]


# ---------------------------------------------------------------- checks
def check_version():
    vp = ROOT / "public/version.json"
    try:
        v = json.loads(vp.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"public/version.json unreadable: {e}")
        return None
    ver, rel, prev = v.get("version"), v.get("release"), v.get("previous_version")
    if not ver or not re.fullmatch(r"\d+\.\d+\.\d+", ver):
        err(f"version.json 'version' must look like 0.4.9, got {ver!r}")
        return None
    if rel != "v" + ver.replace(".", ""):
        err(f"version.json 'release' should be 'v{ver.replace('.', '')}' for version {ver}, got {rel!r}")
    if prev == ver:
        err("version.json 'previous_version' equals 'version': bump the version for every release")
    return v


def check_pages(ver):
    for p in sorted((ROOT / "public").glob("*.html")):
        s = p.read_text(encoding="utf-8")
        labels = re.findall(r'<span class="app-version" aria-label="Application version ([^"]+)">v([^<]+)</span>', s)
        if len(labels) != 1:
            err(f"{p.name}: expected exactly one static version label, found {len(labels)}")
        elif labels[0] != (ver, ver):
            err(f"{p.name}: static label says {labels[0]}, version.json says {ver}")
        if s.count('<script src="/assets/version.js" defer></script>') != 1:
            err(f"{p.name}: missing the /assets/version.js script tag (the label cannot self-heal)")
        for ref in re.findall(r'(?:src|href)="(/[^"?#]+)"', s):
            if ref.startswith("/assets/") or ref.startswith("/books/"):
                if not (ROOT / "public" / ref.lstrip("/")).exists():
                    err(f"{p.name}: references missing file {ref}")


def check_manifest():
    mp = ROOT / "public/books/gabe-and-jinx/book-01/manifest.json"
    try:
        m = json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"book manifest unreadable: {e}")
        return
    pages = m.get("pages", [])
    n = len(pages)
    for i, pg in enumerate(pages, 1):
        if pg.get("number") != i:
            err(f"manifest page entry {i} has number {pg.get('number')}")
        img = pg.get("image", "")
        if not (ROOT / "public" / img.lstrip("/")).exists():
            err(f"manifest page {i}: image missing {img}")
        if f"of {n}" not in pg.get("alt", ""):
            err(f"manifest page {i}: alt text does not say 'of {n}'")
    for ch in m.get("chapters", []):
        if ch.get("end_page", 0) > n:
            err(f"manifest chapter {ch.get('number')} ends at page {ch['end_page']} but book has {n}")


def check_lists(files):
    changed = read_list("CHANGED_FILES.txt", skip_first=True)
    if changed is None:
        err("CHANGED_FILES.txt is missing")
        changed = []
    fileset = set(files)
    for c in changed:
        if c not in fileset:
            err(f"CHANGED_FILES.txt lists a file that does not exist: {c}")
    need = {"public/version.json", "CHANGED_FILES.txt", "PROJECT_TREE.txt"}
    need |= {f"public/{p.name}" for p in (ROOT / "public").glob("*.html")}
    for n in sorted(need - set(changed)):
        err(f"CHANGED_FILES.txt must include {n} (the version changed, so every page and the tree must ship)")
    deletions = read_list("MANUAL_DELETIONS.txt") or []
    for d in deletions:
        if d in fileset:
            err(f"MANUAL_DELETIONS.txt lists {d} but it still exists in the repo; remove it here too")
    return changed, deletions


def check_reference_isolation():
    for p in (ROOT / "public").rglob("*"):
        if p.suffix in (".html", ".css", ".js", ".json", ".xml", ".webmanifest", ".txt") and p.is_file():
            if re.search(r"""["'(=/]reference/""", p.read_text(encoding="utf-8", errors="ignore")):
                err(f"public/{p.relative_to(ROOT / 'public')} links to reference/ (reference material must not be served)")


# ---------------------------------------------------------------- build
def write_tree():
    tree = sorted(set(repo_files()) | {"PROJECT_TREE.txt"})
    (ROOT / "PROJECT_TREE.txt").write_text("\n".join(tree) + "\n", encoding="utf-8")


def build_zip(path, rels):
    dirs = {WRAPPER + "/"}
    for r in rels:
        parts = r.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            dirs.add(WRAPPER + "/" + "/".join(parts[:i]) + "/")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for d in sorted(dirs):
            z.writestr(zipfile.ZipInfo(d), b"")
        for r in rels:
            z.write(ROOT / r, f"{WRAPPER}/{r}")


def verify_zip(path, expected_rels, version, deletions):
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            err(f"{path.name}: corrupt entry {bad}")
        names = z.namelist()
        tops = {n.split("/")[0] for n in names}
        if tops != {WRAPPER}:
            err(f"{path.name}: expected one wrapper directory {WRAPPER}/, found {sorted(tops)}")
        files = {n[len(WRAPPER) + 1:] for n in names if not n.endswith("/")}
        if files != set(expected_rels):
            err(f"{path.name}: contents differ from the list "
                f"(missing {sorted(set(expected_rels) - files)}, extra {sorted(files - set(expected_rels))})")
        if "deploy.info" in files:
            err(f"{path.name}: must not contain deploy.info")
        for d in deletions:
            if d in files:
                err(f"{path.name}: contains {d}, which is marked for deletion")
        vj = f"{WRAPPER}/public/version.json"
        if vj in names and json.loads(z.read(vj)).get("version") != version:
            err(f"{path.name}: version.json inside the zip is not {version}")


def main():
    v = check_version()
    if v is None:
        return fail()
    ver, rel = v["version"], v["release"]

    r = subprocess.run([sys.executable, str(ROOT / "sync-version.py")], capture_output=True, text=True)
    if r.returncode != 0:
        err("sync-version.py failed: " + (r.stderr.strip().splitlines() or ["?"])[-1])
    check_pages(ver)
    check_manifest()
    check_reference_isolation()
    files = repo_files()
    changed, deletions = check_lists(files)
    if errors:
        return fail()

    write_tree()
    files = repo_files()
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("*.zip"):
        old.unlink()
    changed_zip = DIST / f"daroo-publishing-{rel}-CHANGED.zip"
    full_zip = DIST / f"daroo-publishing-{rel}-FULL.zip"
    build_zip(changed_zip, changed)
    build_zip(full_zip, files)
    verify_zip(changed_zip, changed, ver, deletions)
    verify_zip(full_zip, files, ver, deletions)
    if errors:
        for z in (changed_zip, full_zip):
            z.unlink(missing_ok=True)
        return fail()

    print(f"OK  v{ver} ({rel})")
    for z, n in ((changed_zip, len(changed)), (full_zip, len(files))):
        print(f"    {z.relative_to(ROOT)}  {n} files  {z.stat().st_size // 1024} KB")
    print("    checked: version/release, one label per page, version.js on every page, manifest images and alt text,")
    print("             file lists, reference/ not served, wrapper directory, no deploy.info")
    if deletions:
        print("\nMANUAL DELETIONS on GitHub (ZipToGit never deletes):")
        for d in deletions:
            print("    " + d)
    print("\nNot verified by this script: the live deployment and device rendering.")
    return 0


def fail():
    print("NOT READY. Fix these and run again (no zips were written):")
    for e in errors:
        print("  - " + e)
    return 1


if __name__ == "__main__":
    sys.exit(main())
