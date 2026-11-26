#!/usr/bin/env python3
"""Render index.html with every public gjed repository that has GitHub Pages.

Usage: build.py [--out DIR]   (default: _site)
GITHUB_TOKEN, when set, is used to avoid the unauthenticated rate limit.
"""

import argparse
import html
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

OWNER = "gjed"
ROOT = Path(__file__).resolve().parent


def pages_repos():
    req = urllib.request.Request(
        f"https://api.github.com/users/{OWNER}/repos?per_page=100&type=owner&sort=full_name",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    # SIMPLIFIED: one page of 100 repos; paginate via the Link header past that.
    with urllib.request.urlopen(req, timeout=30) as resp:
        repos = json.load(resp)
    return [
        r
        for r in repos
        if r["has_pages"]
        and not (r["private"] or r["fork"] or r["archived"])
        and r["name"] != f"{OWNER}.github.io"
    ]


def card(repo):
    name = html.escape(repo["name"])
    url = html.escape(repo["homepage"] or f"https://{OWNER}.github.io/{repo['name']}/")
    desc = html.escape(repo["description"] or "")
    return (
        f'        <li><a href="{url}">\n'
        f'          <h2 class="h2">{name}</h2>\n'
        f'          <p class="body">{desc}</p>\n'
        f'          <span class="label">{OWNER} / {name}</span>\n'
        f"        </a></li>"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="_site", type=Path)
    out = parser.parse_args().out

    repos = pages_repos()
    if not repos:
        sys.exit("error: no public repositories with GitHub Pages found; refusing to publish an empty page")

    page = (ROOT / "index.html").read_text().replace("{{projects}}", "\n".join(map(card, repos)))
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(ROOT / "assets", out / "assets")
    (out / "index.html").write_text(page)
    print(f"built {out}/index.html with {len(repos)} projects: {', '.join(r['name'] for r in repos)}")


if __name__ == "__main__":
    main()
