#!/usr/bin/env python3
"""
Extract blog index cards from a saved full-page HTML export (e.g. SingleFile).

Outputs (under PapeX/):
  - data/blog-posts.json       — slug, title, coverFile (relative or null)
  - blog-covers/{slug}.webp|.jpg|.png — hero images when decodable
  - blog-posts.partial.html    — card markup for blog.html

Re-run when you save a fresh copy of the blog index:
  python3 PapeX/scripts/extract_blog_listing.py
  python3 PapeX/scripts/extract_blog_listing.py --export "/path/to/saved.html"
  python3 PapeX/scripts/extract_blog_listing.py --write-blog-html PapeX/blog.html

Paths are resolved from the repository root (parent of scripts/).
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from html import escape
from pathlib import Path

# Default export filename (under Downloads, sibling of PapeX/)
DEFAULT_EXPORT_NAME = (
    "PapeX ｜ Digital Receipts Revolutionized - Paperless Receipt Solutions "
    "(4_26_2026 5：21：04 PM).html"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def downloads_dir() -> Path:
    return repo_root().parent


def parse_posts(html: str) -> list[dict]:
    """Return list of {slug, title, data_uri|None} in document order."""
    parts = html.split("</article>")
    posts: list[dict] = []
    slug_re = re.compile(r"https?://(?:www\.)?papex\.app/blog/([a-z0-9-]+)", re.I)
    # Raster data URIs (length so we ignore tiny tracking pixels)
    data_raster_re = re.compile(
        r"data:image/(webp|jpeg|png);base64,([A-Za-z0-9+/=]{200,})",
        re.I,
    )
    h_re = re.compile(r"<h[23][^>]*>([^<]{3,300})</h[23]>", re.I)
    img_alt_re = re.compile(r'<img[^>]+alt="([^"]*)"', re.I)

    for part in parts:
        sm = slug_re.search(part)
        if not sm:
            continue
        slug = sm.group(1).lower()

        title = None
        hm = h_re.search(part)
        if hm:
            title = _clean_title(hm.group(1))
        if not title:
            for am in img_alt_re.finditer(part):
                alt = _clean_title(am.group(1))
                if alt and "papex logo" not in alt.lower():
                    title = alt
                    break
        if not title:
            title = slug.replace("-", " ").title()

        candidates = data_raster_re.findall(part)
        data_uri: str | None = None
        if candidates:
            # Longest payload is almost always the hero (vs nav logo, etc.)
            best = max(candidates, key=lambda c: len(c[1]))
            ext = best[0].lower()
            b64 = best[1]
            data_uri = f"data:image/{ext};base64,{b64}"

        posts.append({"slug": slug, "title": title, "data_uri": data_uri})

    # Dedupe by slug preserving first occurrence
    seen: set[str] = set()
    out: list[dict] = []
    for p in posts:
        if p["slug"] in seen:
            continue
        seen.add(p["slug"])
        out.append(p)
    return out


def _clean_title(raw: str) -> str:
    t = re.sub(r"\s+", " ", raw).strip()
    t = t.replace("&amp;", "&").replace("&rsquo;", "\u2019").replace("&nbsp;", " ")
    return t


def decode_cover(data_uri: str) -> tuple[bytes, str] | None:
    m = re.match(r"data:image/(webp|jpeg|png);base64,(.+)", data_uri, re.I | re.S)
    if not m:
        return None
    ext = m.group(1).lower()
    if ext == "jpeg":
        ext = "jpg"
    try:
        raw = base64.b64decode(m.group(2), validate=False)
    except Exception:
        return None
    if len(raw) < 100:
        return None
    return raw, ext


def build_partial_html(posts: list[dict], covers_rel: Path) -> str:
    """posts items: slug, title, cover_file (str|None) relative to blog.html."""
    lines: list[str] = []
    for i, p in enumerate(posts):
        slug = p["slug"]
        title = escape(p["title"])
        local_href = f"articles/{slug}.html"
        delay_cls = ""
        if i % 3 == 1:
            delay_cls = " reveal-d1"
        elif i % 3 == 2:
            delay_cls = " reveal-d2"
        cover = p.get("cover_file")
        if cover:
            img = (
                f'<div class="blog-list-card-img-wrap">'
                f'<img src="{escape(str(cover))}" alt="" width="400" height="400" '
                f'loading="lazy" decoding="async" class="blog-list-card-img" /></div>'
            )
        else:
            img = '<div class="blog-list-card-img-wrap blog-list-card-img-wrap--empty" aria-hidden="true"></div>'
        lines.append(
            f'<a class="blog-list-card card reveal{delay_cls}" href="{escape(local_href)}">'
            f"{img}"
            f'<div class="blog-list-card-body">'
            f'<h3 class="blog-list-card-title">{title}</h3>'
            f'<span class="blog-list-card-meta">Read article</span>'
            f"</div></a>"
        )
    return "\n".join(lines)


def inject_into_blog(blog_html_path: Path, partial: str) -> None:
    text = blog_html_path.read_text(encoding="utf-8")
    start = "<!-- BLOG_LISTING_START -->"
    end = "<!-- BLOG_LISTING_END -->"
    if start not in text or end not in text:
        print(
            f"Warning: markers {start!r} / {end!r} not found in {blog_html_path}; "
            "skipping inject. Paste blog-posts.partial.html manually.",
            file=sys.stderr,
        )
        return
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    new_body = f"{pre}{start}\n{partial}\n{end}{post}"
    blog_html_path.write_text(new_body, encoding="utf-8")
    print(f"Injected listing into {blog_html_path}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--export",
        type=Path,
        help="Path to saved blog index HTML",
    )
    ap.add_argument(
        "--skip-images",
        action="store_true",
        help="Do not write blog-covers/ files (JSON only, cover_file null)",
    )
    ap.add_argument(
        "--write-blog-html",
        type=Path,
        help="Replace BLOG_LISTING markers in this blog.html file",
    )
    args = ap.parse_args()

    root = repo_root()
    data_dir = root / "data"
    covers_dir = root / "blog-covers"
    data_dir.mkdir(parents=True, exist_ok=True)
    covers_dir.mkdir(parents=True, exist_ok=True)

    export_path = args.export
    if not export_path:
        export_path = downloads_dir() / DEFAULT_EXPORT_NAME
    if not export_path.is_file():
        print(f"Export not found: {export_path}", file=sys.stderr)
        return 1

    html = export_path.read_text(encoding="utf-8", errors="replace")
    parsed = parse_posts(html)
    if not parsed:
        print("No posts found in export.", file=sys.stderr)
        return 1

    json_rows: list[dict] = []
    for p in parsed:
        slug = p["slug"]
        title = p["title"]
        cover_file: str | None = None
        if not args.skip_images and p["data_uri"]:
            dec = decode_cover(p["data_uri"])
            if dec:
                raw, ext = dec
                fname = f"{slug}.{ext}"
                fpath = covers_dir / fname
                fpath.write_bytes(raw)
                cover_file = f"blog-covers/{fname}"
        json_rows.append({"slug": slug, "title": title, "coverFile": cover_file})

    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "blog-posts.json").write_text(
        json.dumps(json_rows, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {data_dir / 'blog-posts.json'} ({len(json_rows)} posts)")

    # partial uses same cover_file paths as JSON
    posts_for_html = [
        {"slug": r["slug"], "title": r["title"], "cover_file": r["coverFile"]}
        for r in json_rows
    ]
    partial = build_partial_html(posts_for_html, Path("blog-covers"))
    (root / "blog-posts.partial.html").write_text(partial + "\n", encoding="utf-8")
    print(f"Wrote {root / 'blog-posts.partial.html'}")

    if args.write_blog_html:
        inject_into_blog(args.write_blog_html.resolve(), partial)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
