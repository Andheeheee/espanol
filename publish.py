#!/usr/bin/env python3
"""Build the public, read-only copy of the course site and push it to GitHub Pages.

    python3 publish.py          # build public/ and commit + push it to the gh-pages branch
    python3 publish.py --dry    # just build public/ (open public/index.html to check it)

The public copy is the same site minus anything that needs the home server: no progress saving, no Vocabulary Bank
(that's Quizlet's content, so it stays on the tailnet site), no on-demand voice clips. public/ is a git worktree
of the gh-pages branch, which GitHub Pages serves at DOMAIN.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build import VAULT, build  # noqa: E402

DOMAIN = "espanol.dunne.systems"  # Porkbun CNAME espanol → andheeheee.github.io
OUT = HERE / "public"
SITE_FILES = ["index.html", "i18n.js", "app.js", "style.css", "content.js"]


def git(*args, cwd=HERE):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def worktree():
    """public/ = a checkout of the gh-pages branch (created empty the first time)."""
    if (OUT / ".git").exists():
        return
    if OUT.exists():
        shutil.rmtree(OUT)
    if git("branch", "--list", "gh-pages"):
        git("worktree", "add", str(OUT), "gh-pages")
    else:
        git("worktree", "add", "--orphan", "-b", "gh-pages", str(OUT))


def main():
    build()
    worktree()
    for p in OUT.iterdir():  # start clean so deleted files disappear from the site too
        if p.name != ".git":
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    for name in SITE_FILES:
        shutil.copy2(HERE / "site" / name, OUT / name)
    index = OUT / "index.html"
    index.write_text(index.read_text(encoding="utf-8").replace(
        '<script src="app.js">', '<script>window.PUBLIC_SITE = true;</script>\n<script src="app.js">'), encoding="utf-8")
    # photos and the recorded es-MX clips; not audio/say/ (on-demand clips for Vocabulary Bank words)
    shutil.copytree(VAULT / "Media" / "img", OUT / "media" / "img")
    shutil.copytree(VAULT / "Media" / "audio", OUT / "media" / "audio", ignore=lambda d, names: ["say"] if Path(d).name == "audio" else [])
    (OUT / ".nojekyll").touch()  # serve files as-is
    if DOMAIN:
        (OUT / "CNAME").write_text(DOMAIN + "\n")
    print(f"Built {OUT}")
    if "--dry" in sys.argv:
        return
    git("add", "-A", cwd=OUT)
    if not git("status", "--porcelain", cwd=OUT):
        print("Nothing changed — already published.")
        return
    git("commit", "-q", "-m", "Publish site", cwd=OUT)
    git("push", "-q", "origin", "gh-pages", cwd=OUT)
    print(f"Pushed to gh-pages{' — live at https://' + DOMAIN if DOMAIN else ''} in a minute or two.")


if __name__ == "__main__":
    main()
