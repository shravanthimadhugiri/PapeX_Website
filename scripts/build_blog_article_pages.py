#!/usr/bin/env python3
"""
Build static article wrapper pages under PapeX/articles/.

Live papex.app blog posts render in the browser; a simple HTTP GET does not
return the full article HTML. Each page uses the marketing shell plus an iframe
that loads the canonical post URL (parent URL stays local).

Inputs:
  - ../blog-post-urls.txt (default, next to PapeX/ under Downloads/)
  - data/blog-posts.json for title and coverFile (optional)

Usage (from Downloads/):
  python3 PapeX/scripts/build_blog_article_pages.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def downloads_dir() -> Path:
    return repo_root().parent


def slug_from_url(url: str) -> str:
    u = url.strip().rstrip("/")
    m = re.search(r"/blog/([^/?#]+)/?$", u, re.I)
    if not m:
        raise ValueError(f"Could not parse slug from URL: {url!r}")
    return m.group(1).lower()


def load_json_meta(root: Path) -> dict[str, dict]:
    p = root / "data" / "blog-posts.json"
    if not p.is_file():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {row["slug"]: row for row in data if "slug" in row}


def article_html(
    *,
    title: str,
    canonical_url: str,
    cover_rel: str | None,
) -> str:
    cover_block = ""
    if cover_rel:
        cover_alt = escape(f"Featured cover illustration for: {title}", quote=True)
        cover_block = (
            f'<div class="blog-article-hero"><img src="{escape(cover_rel)}" '
            f'alt="{cover_alt}" width="1200" height="630" loading="eager" decoding="async" '
            'class="blog-article-hero-img" /></div>\n'
        )
    iframe_src = escape(canonical_url, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} | PapeX Blog</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,400..700;1,14..32,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../papex-shared.css">
<style>
  .blog-article-shell {{ padding-top: 24px; padding-bottom: 80px; max-width: 1200px; margin: 0 auto; }}
  .blog-article-back {{ margin-bottom: 20px; }}
  .blog-article-back a {{ font-size: 14px; font-weight: 500; color: var(--orange); text-decoration: none; }}
  .blog-article-back a:hover {{ text-decoration: underline; }}
  .blog-article-title {{ font-family: var(--font-display); font-size: clamp(26px, 3.5vw, 38px); font-weight: 700; letter-spacing: -0.04em; line-height: 1.15; color: var(--text-primary); margin: 0 0 12px; max-width: 42ch; }}
  .blog-article-note {{ font-size: 14px; color: var(--text-muted); margin: 0 0 24px; max-width: 60ch; line-height: 1.55; }}
  .blog-article-hero {{ border-radius: 17px; overflow: hidden; border: 1px solid #EEDDEE; margin-bottom: 24px; max-height: 420px; background: var(--bg-surface); }}
  .blog-article-hero-img {{ width: 100%; height: auto; max-height: 420px; object-fit: cover; display: block; }}
  .blog-article-frame-wrap {{ border-radius: 17px; overflow: hidden; border: 1px solid var(--border); background: var(--bg-primary); min-height: min(85vh, 1200px); }}
  .blog-article-frame-wrap iframe {{ width: 100%; min-height: min(85vh, 1200px); border: 0; display: block; }}
</style>
</head>
<body>
<nav class="site-nav" aria-label="Primary">
  <div class="nav-inner">
    <a href="../index.html" class="nav-logo" aria-label="PapeX">
      <img src="../PapeX%20Logos/primary%20orange%20light.svg" alt="PapeX" />
    </a>
    <div class="nav-links">
      <a href="../pos-calculator.html">POS Calculator</a>
      <a href="#">About Us</a><!-- placeholder: link to about-us.html -->
      <a href="../index.html#pricing">Pricing</a>
      <a href="../blog.html">Blog</a>
    </div>
    <div class="nav-right">
      <a href="#" class="btn btn-ghost btn-sm">Log In</a>
      <a href="#" class="btn btn-primary btn-sm">Download App</a>
    </div>
  </div>
</nav>

<main class="subpage-main blog-article-shell">
  <p class="blog-article-back"><a href="../blog.html">Back to blog</a></p>
  <h1 class="blog-article-title">{escape(title)}</h1>
  <p class="blog-article-note">Full article loads in the frame below. If it stays blank, open this site over HTTP (not file://) or allow third-party content; the frame points at the live post URL.</p>
  {cover_block}
  <div class="blog-article-frame-wrap">
    <iframe src="{iframe_src}" title="{escape(title)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
</main>

<footer>
  <div class="footer-inner">
    <a href="../index.html" class="footer-logo" aria-label="PapeX">
      <img src="../PapeX%20Logos/primary%20orange%20light.svg" alt="PapeX" />
    </a>
    <div class="footer-links" role="navigation" aria-label="Footer">
      <a href="../pos-calculator.html">POS Calculator</a>
      <a href="#">About Us</a><!-- placeholder: link to about-us.html -->
      <a href="../index.html#pricing">Pricing</a>
      <a href="../blog.html">Blog</a>
    </div>
    <div class="footer-legal-wrap">
      <p class="footer-legal">© 2026 PapeX Inc. · Dallas, TX · Proprietary and confidential.</p>
      <p class="footer-legal" style="margin-top:4px">Receipts, reimagined.</p>
    </div>
  </div>
</footer>
<script>
(function () {{
  window.addEventListener('scroll', function () {{
    var bar = document.querySelector('.site-nav');
    if (bar) bar.style.boxShadow = window.scrollY > 20 ? '0 1px 0 rgba(0,0,0,0.06)' : 'none';
  }}, {{ passive: true }});
}})();
</script>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--urls",
        type=Path,
        default=None,
        help="Path to blog-post-urls.txt (default: sibling of PapeX/, e.g. Downloads/blog-post-urls.txt)",
    )
    args = ap.parse_args()

    root = repo_root()
    urls_path = args.urls if args.urls else downloads_dir() / "blog-post-urls.txt"
    if not urls_path.is_file():
        print(f"URLs file not found: {urls_path}", file=sys.stderr)
        return 1

    lines = [
        ln.strip()
        for ln in urls_path.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    if len(lines) != 24:
        print(f"Expected 24 URLs, got {len(lines)} in {urls_path}", file=sys.stderr)
        return 1

    meta = load_json_meta(root)
    out_dir = root / "articles"
    out_dir.mkdir(parents=True, exist_ok=True)

    for url in lines:
        slug = slug_from_url(url)
        row = meta.get(slug, {})
        title = row.get("title") or slug.replace("-", " ").title()
        cover_file = row.get("coverFile")
        cover_rel = None
        if cover_file:
            cover_rel = "../" + str(cover_file).replace("\\", "/")

        html = article_html(
            title=title,
            canonical_url=url.strip(),
            cover_rel=cover_rel,
        )
        (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"Wrote articles/{slug}.html")

    print(f"Done. {len(lines)} pages in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
