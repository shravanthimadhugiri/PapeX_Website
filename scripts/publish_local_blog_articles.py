#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
from datetime import date, timedelta
from html import escape
from pathlib import Path
from urllib.parse import quote as urlquote

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = ROOT.parent
MARKDOWN_PATH = DOWNLOADS / "papex-blog-content.md"
URLS_PATH = DOWNLOADS / "blog-post-urls.txt"
META_PATH = ROOT / "data" / "blog-posts.json"
ARTICLES_DIR = ROOT / "articles"

DATE_LINE_RE = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}\s*\d+\s*min read$", re.I)
LIST_RE = re.compile(r"^(?:[-*]|\d+\.)\s+(.+)$")
HEADING_RE = re.compile(r"^(#{2,6})\s+(.+)$")
MULTISPACE_RE = re.compile(r"[ \t]{2,}")
WORD_RE = re.compile(r"\w+")

COPY_FIXES = [
    ("secure user-friendly", "secure, user-friendly"),
    ("Cloud based", "Cloud-based"),
    ("real time", "real-time"),
    ("point of sale", "point-of-sale"),
    ("e receipts", "e-receipts"),
    ("expense records, and transaction documentation especially", "expense records, and transaction documentation, especially"),
    ("By capturing receipts digitally businesses and individuals", "By capturing receipts digitally, businesses and individuals"),
    ("Once a receipt is captured digitally the next step", "Once a receipt is captured digitally, the next step"),
    ("After extraction receipts are stored", "After extraction, receipts are stored"),
    ("without manual input", "without manual input."),
    ("This automation reduces errors saves time and ensures", "This automation reduces errors, saves time, and ensures"),
    ("where users can search filter and retrieve", "where users can search, filter, and retrieve"),
    ("that is both accessible and secure eliminating", "that is both accessible and secure, eliminating"),
    ("Setting up strong financial systems early in the year compounds benefits over time.", "Setting up strong financial systems early in the year compounds those benefits over time."),
    ("Instead of reacting during tax season or audits users maintain", "Instead of reacting during tax season or audits, users maintain"),
    ("By automating receipt capture and building reliable financial infrastructure PapeX helps", "By automating receipt capture and building reliable financial infrastructure, PapeX helps"),
    ("from merchant to user:", "from merchant to user."),
    ("The modern checkout line is fast.", "The modern checkout line is fast."),
    ("What comes after isn’t.", "What comes after often is not."),
    ("handle-receipts", "handle receipts"),
]

DROP_LINES = {
    "comes in.",
    "must",
    "them.",
    "You tap, you pay, you walk away, and your receipt is already:",
    "Available when you need it",
    "The merchant wins. The user wins. The POS wins. And the future finally looks like the future.",
    "This is why PapeX exists! To make every dollar make sense again.",
    "Receipts, reimagined.",
    "Receipts reimagined.",
}

# Single-line phrases that are residual marketing taglines or extraction debris.
TAGLINE_PATTERNS = [
    re.compile(r"^Receipts,?\s*reimagined\.?\s*$", re.I),
    re.compile(r"^Make every dollar make sense again\.?\s*$", re.I),
    re.compile(r"^Join (?:our|the) waitlist.*$", re.I),
    re.compile(r"^Take our survey.*$", re.I),
    re.compile(r"^Learn more about PapeX.*$", re.I),
]

# Lines that are obviously orphan fragments left over from extraction noise:
# 1-3 word lines without terminal punctuation that aren't headings or list items.
ORPHAN_RE = re.compile(r"^[A-Za-z][A-Za-z' \-]{0,40}$")


def norm(text: str) -> str:
    text = text.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9]+", "", text)


def slug_from_url(url: str) -> str:
    m = re.search(r"/blog/([^/?#]+)", url.strip())
    if not m:
        raise ValueError(f"cannot parse slug from {url!r}")
    return m.group(1)


def split_sections(md: str) -> list[tuple[str, str]]:
    sections = []
    for raw in re.split(r"\n---\n", md.strip()):
        raw = raw.strip()
        if not raw:
            continue
        lines = raw.splitlines()
        if not lines or not lines[0].startswith("# "):
            continue
        title = lines[0][2:].strip()
        body = "\n".join(lines[1:]).strip()
        sections.append((title, body))
    return sections


def normalize_smart_punctuation(text: str) -> str:
    text = text.replace("…", "…")
    text = re.sub(r"\.{3,}", "…", text)
    text = re.sub(r"(?<=\w)\s*--\s*(?=\w)", "—", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def clean_body(body: str) -> str:
    out: list[str] = []
    prev = None
    for ln in body.splitlines():
        s = ln.strip()
        if DATE_LINE_RE.match(s):
            continue
        if "Join Our Waitlist" in s and ("Learn More" in s or "Take Our Survey" in s):
            continue
        if s.startswith("for PapeX"):
            continue
        if s in DROP_LINES:
            continue
        if any(rgx.match(s) for rgx in TAGLINE_PATTERNS):
            continue
        # Orphan-fragment trim: very short non-list, non-heading lines that are
        # almost certainly leftover heading-render fragments.
        if (
            s
            and not s.startswith("#")
            and not LIST_RE.match(s)
            and len(s.split()) <= 4
            and ORPHAN_RE.match(s)
            and not s.endswith((".", "?", "!", ":"))
        ):
            # Merge onto previous prose line when possible (plan: turn fragments into sentences).
            if out:
                prev_ln = out[-1].strip()
                if (
                    prev_ln
                    and not prev_ln.startswith("#")
                    and not HEADING_RE.match(prev_ln)
                    and not LIST_RE.match(prev_ln)
                ):
                    tail = prev_ln[-1] if prev_ln else ""
                    joiner = " " if tail not in ("-", "—") else ""
                    frag = s[0].upper() + s[1:] if len(s) > 1 else s.upper()
                    out[-1] = out[-1].rstrip() + joiner + frag
                    prev = out[-1].strip()
                    continue
            continue
        if prev == s and s:
            continue
        out.append(ln.rstrip())
        prev = s

    cleaned = "\n".join(out)
    for src, dst in COPY_FIXES:
        cleaned = cleaned.replace(src, dst)
    cleaned = cleaned.replace(" — ", ", ")
    cleaned = re.sub(r"\]\s+\(", "](", cleaned)
    cleaned = normalize_smart_punctuation(cleaned)
    cleaned = MULTISPACE_RE.sub(" ", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def extract_lede(body: str) -> tuple[str, str]:
    """Pull the first prose paragraph out of `body` to use as a lede.

    The lede is rendered separately above the hero, so we strip it from the body
    to avoid duplication. Returns ``(lede_plain_text, body_without_lede)``.
    Falls back to an empty lede when the body opens with a heading or list.
    """
    lines = body.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines):
        return "", body
    first = lines[i].strip()
    if first.startswith("#") or LIST_RE.match(first):
        return "", body

    para_lines: list[str] = []
    j = i
    while j < len(lines) and lines[j].strip():
        s = lines[j].strip()
        if s.startswith("#") or LIST_RE.match(s):
            break
        para_lines.append(s)
        j += 1
    if not para_lines:
        return "", body
    lede = " ".join(para_lines).strip()
    rest = "\n".join(lines[j:]).lstrip("\n")
    return lede, rest


def compute_read_time(body: str) -> int:
    words = len(WORD_RE.findall(body))
    return max(2, math.ceil(words / 200))


def format_publish_date(idx: int, total: int) -> str:
    """Return a human month/year tag for the post.

    The URL list is roughly newest-first, so we step back roughly two weeks per
    article from a recent base date to give each kicker a unique month label.
    """
    base = date(2026, 4, 19)
    delta = timedelta(days=14 * idx)
    pub = base - delta
    return pub.strftime("%b %d, %Y")


def md_inline_to_html(text: str) -> str:
    text = escape(text.strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\s*\((https?://[^)]+)\)",
        r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>',
        text,
    )
    return text


def markdown_block_to_html(body: str) -> str:
    lines = [ln.rstrip() for ln in body.splitlines()]
    html: list[str] = []
    para: list[str] = []
    list_mode = None

    def flush_para() -> None:
        nonlocal para
        if para:
            txt = " ".join(x.strip() for x in para if x.strip())
            if txt:
                html.append(f"<p>{md_inline_to_html(txt)}</p>")
            para = []

    def close_list() -> None:
        nonlocal list_mode
        if list_mode:
            html.append(f"</{list_mode}>")
            list_mode = None

    for i, ln in enumerate(lines):
        s = ln.strip()
        if not s:
            if list_mode:
                nxt = ""
                for j in range(i + 1, len(lines)):
                    cand = lines[j].strip()
                    if cand:
                        nxt = cand
                        break
                if nxt and LIST_RE.match(nxt):
                    continue
            flush_para()
            close_list()
            continue

        hm = HEADING_RE.match(s)
        if hm:
            flush_para()
            close_list()
            level = len(hm.group(1))
            txt = md_inline_to_html(hm.group(2))
            html.append(f"<h{level}>{txt}</h{level}>")
            continue

        lm = LIST_RE.match(s)
        if lm:
            flush_para()
            this_mode = "ol" if re.match(r"^\d+\.", s) else "ul"
            if list_mode != this_mode:
                close_list()
                list_mode = this_mode
                html.append(f"<{list_mode}>")
            html.append(f"<li>{md_inline_to_html(lm.group(1))}</li>")
            continue

        if re.match(r"^[A-Z][^.!?]{1,80}$", s):
            flush_para()
            close_list()
            html.append(f"<h3>{md_inline_to_html(s)}</h3>")
            continue

        para.append(s)

    flush_para()
    close_list()
    return "\n      ".join(html)


def render_related_strip(current_slug: str, slugs: list[str], meta: dict) -> str:
    """Pick the next 3 slugs after the current one (cyclic) and render cards
    that match the existing `.blog-list-card` markup used in `blog.html`.
    """
    if current_slug not in slugs:
        return ""
    start = slugs.index(current_slug)
    related: list[str] = []
    n = len(slugs)
    for offset in range(1, n):
        candidate = slugs[(start + offset) % n]
        if candidate == current_slug:
            continue
        related.append(candidate)
        if len(related) == 3:
            break

    cards: list[str] = []
    for i, slug in enumerate(related):
        row = meta.get(slug, {})
        title = row.get("title", slug.replace("-", " ").title())
        cover = row.get("coverFile")
        delay_class = "" if i == 0 else f" reveal-d{i}"
        if cover:
            img = (
                f'<div class="blog-list-card-img-wrap">'
                f'<img src="../{escape(cover)}" alt="Cover thumbnail: {escape(title)}" '
                f'width="400" height="400" loading="lazy" decoding="async" class="blog-list-card-img" />'
                f'</div>'
            )
        else:
            img = '<div class="blog-list-card-img-wrap blog-list-card-img-wrap--empty"></div>'
        cards.append(
            f'<a class="blog-list-card card reveal{delay_class}" href="{escape(slug)}.html">'
            f'{img}'
            f'<div class="blog-list-card-body">'
            f'<h3 class="blog-list-card-title">{escape(title)}</h3>'
            f'<span class="blog-list-card-meta">Read article</span>'
            f'</div></a>'
        )

    if not cards:
        return ""

    return f"""
  <section class="blog-related sec-alt" aria-label="Continue reading">
    <div class="blog-related-head reveal">
      <span class="section-label">Continue reading</span>
      <h2>More from the PapeX blog</h2>
    </div>
    <div class="blog-related-grid blog-list-grid">
      {"".join(cards)}
    </div>
  </section>"""


def render_cta_band() -> str:
    return """
  <section class="blog-end-cta" aria-label="Get PapeX">
    <div class="blog-end-cta-card card form-card reveal">
      <span class="section-label">Get the app</span>
      <h2 class="blog-end-cta-title">Receipts, reimagined.</h2>
      <p class="blog-end-cta-copy">PapeX captures, organizes, and stores every receipt automatically, so your records are ready when you need them. Join the people building the future of digital receipts.</p>
      <div class="blog-end-cta-actions">
        <a href="../papex-v2.html#download" class="btn btn-primary btn-lg">Download App</a>
        <a href="../blog.html" class="btn btn-ghost btn-lg">Back to blog</a>
      </div>
    </div>
  </section>"""


def share_links_for(slug: str, title: str) -> str:
    live_url = f"https://www.papex.app/blog/{slug}"
    url_param = urlquote(live_url, safe="")
    title_param = urlquote(title, safe="")
    href_url = escape(live_url, quote=True)
    twitter_href = f"https://twitter.com/intent/tweet?text={title_param}&amp;url={url_param}"
    linkedin_href = f"https://www.linkedin.com/sharing/share-offsite/?url={url_param}"
    return f"""<div class="blog-article-share" aria-label="Share this article">
        <a class="blog-article-share-btn" href="{twitter_href}" target="_blank" rel="noopener noreferrer" aria-label="Share on X">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2H21.5l-7.4 8.46L23 22h-6.79l-5.31-6.94L4.7 22H1.44l7.92-9.05L1 2h6.91l4.79 6.34L18.244 2Zm-1.19 18h1.85L7.04 4H5.07l11.984 16Z"/></svg>
        </a>
        <a class="blog-article-share-btn" href="{linkedin_href}" target="_blank" rel="noopener noreferrer" aria-label="Share on LinkedIn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5ZM.22 8.04h4.56V22H.22V8.04ZM8.04 8.04h4.37v1.91h.06c.61-1.16 2.1-2.39 4.32-2.39 4.62 0 5.47 3.04 5.47 7v7.44h-4.56v-6.6c0-1.57-.03-3.59-2.19-3.59-2.19 0-2.52 1.71-2.52 3.48V22H8.04V8.04Z"/></svg>
        </a>
        <button class="blog-article-share-btn blog-article-copy" type="button" data-copy-url="{href_url}" aria-label="Copy link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.06 1.06"/><path d="M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.06-1.06"/></svg>
        </button>
      </div>"""


def article_html(
    title: str,
    hero_rel: str | None,
    article_html_block: str,
    *,
    slug: str,
    kicker_date: str,
    read_time: int,
    lede_html: str,
    related_html: str,
    cta_html: str,
) -> str:
    hero = ""
    if hero_rel:
        hero = (
            f'<figure class="blog-article-hero">'
            f'<img src="{escape(hero_rel)}" '
            f'alt="Featured cover illustration for: {escape(title)}" width="1600" height="900" '
            'loading="eager" decoding="async" class="blog-article-hero-img" />'
            f'</figure>'
        )

    lede_block = ""
    if lede_html:
        lede_block = f'<p class="blog-article-lede">{lede_html}</p>'

    share_block = share_links_for(slug, title)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} | PapeX Blog</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,400..700;1,14..32,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../papex-shared.css">
<style>
  /* ── Article shell ─────────────────────────────────────────────── */
  main.subpage-main.blog-article-shell {{ min-height: 0; }}
  .blog-article-shell {{
    box-sizing: border-box;
    padding: 96px var(--pad-x) 0;
    max-width: 1200px;
    margin: 0 auto;
  }}
  .blog-article-back {{ margin: 0 0 32px; }}
  .blog-article-back a {{
    display: inline-flex; align-items: center; gap: 6px;
    font-size: 14px; font-weight: 500; color: var(--orange);
    text-decoration: none;
  }}
  .blog-article-back a::before {{ content: "←"; font-size: 16px; line-height: 1; }}
  .blog-article-back a:hover {{ text-decoration: underline; }}

  /* ── Header zone (kicker, title, lede, byline, share) ──────────── */
  .blog-article-header {{
    max-width: 760px;
    margin: 0 auto 36px;
  }}
  .blog-article-kicker {{
    display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
    font-size: 12px; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; margin: 0 0 18px;
    color: var(--text-muted);
  }}
  .blog-article-kicker .k-label {{ color: var(--orange); }}
  .blog-article-kicker .k-dot {{ color: var(--text-muted); opacity: 0.6; }}
  .blog-article-title {{
    font-family: var(--font-display);
    font-size: clamp(34px, 4.4vw, 52px);
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1.08;
    color: var(--text-primary);
    margin: 0 0 20px;
    max-width: 30ch;
  }}
  .blog-article-lede {{
    font-size: 20px;
    line-height: 1.6;
    color: var(--text-primary);
    margin: 0 0 24px;
    max-width: 60ch;
    letter-spacing: -0.01em;
  }}
  .blog-article-byline {{
    display: flex; align-items: center; flex-wrap: wrap; gap: 14px;
    padding-top: 18px;
    border-top: 1px solid var(--border-light);
  }}
  .blog-article-byline-meta {{
    display: flex; align-items: center; gap: 12px;
    font-size: 13px; color: var(--text-secondary);
  }}
  .blog-article-mark {{
    width: 32px; height: 32px; border-radius: 50%;
    background: var(--orange-dim);
    display: inline-flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    border: 1px solid var(--orange-border);
  }}
  .blog-article-mark img {{ width: 18px; height: 18px; display: block; }}
  .blog-article-byline-name {{
    font-size: 14px; font-weight: 600; color: var(--text-primary);
  }}
  .blog-article-byline-date {{
    font-size: 13px; color: var(--text-muted);
  }}
  .blog-article-share {{
    margin-left: auto; display: inline-flex; gap: 8px;
  }}
  .blog-article-share-btn {{
    width: 34px; height: 34px; border-radius: 50%;
    border: 1px solid var(--border);
    background: #fff; color: var(--text-secondary);
    display: inline-flex; align-items: center; justify-content: center;
    text-decoration: none; cursor: pointer;
    transition: var(--transition);
  }}
  .blog-article-share-btn:hover {{
    color: var(--orange); border-color: var(--orange-border);
    background: var(--orange-dim);
  }}
  .blog-article-copy--ok {{
    color: var(--green-live) !important;
    border-color: rgba(22, 163, 74, 0.35) !important;
    background: rgba(22, 163, 74, 0.08) !important;
  }}

  /* ── Hero image ────────────────────────────────────────────────── */
  .blog-article-hero {{
    margin: 0 0 40px;
    border-radius: 17px;
    overflow: hidden;
    border: 1px solid #EEDDEE;
    background: var(--bg-surface);
  }}
  .blog-article-hero-img {{
    width: 100%; height: auto; display: block;
    aspect-ratio: 16 / 9; object-fit: cover;
  }}

  /* ── Body prose column ─────────────────────────────────────────── */
  .blog-article-prose {{
    max-width: 680px;
    margin: 0 auto;
  }}
  .blog-article-prose > *:first-child {{ margin-top: 0 !important; }}
  .blog-article-prose p {{
    font-size: 17px;
    line-height: 1.8;
    color: var(--text-secondary);
    margin: 0 0 1.4rem;
    max-width: 65ch;
  }}
  .blog-article-prose > p:first-of-type {{
    font-size: 19px;
    color: var(--text-primary);
    line-height: 1.7;
  }}
  .blog-article-prose h2,
  .blog-article-prose h3,
  .blog-article-prose h4,
  .blog-article-prose h5,
  .blog-article-prose h6 {{
    font-family: var(--font-display);
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1.2;
  }}
  .blog-article-prose h2 {{
    font-size: clamp(26px, 2.4vw, 32px);
    font-weight: 700;
    margin: 3rem 0 1rem;
  }}
  .blog-article-prose * + h2 {{
    margin-top: 3rem;
  }}
  .blog-article-prose > h2:first-child,
  .blog-article-prose > h3:first-child {{
    margin-top: 0;
  }}
  .blog-article-prose h3 {{
    font-size: clamp(20px, 2vw, 24px);
    font-weight: 700;
    margin: 2.2rem 0 0.8rem;
  }}
  .blog-article-prose h4 {{
    font-size: 18px;
    font-weight: 700;
    margin: 1.8rem 0 0.6rem;
  }}
  .blog-article-prose ul,
  .blog-article-prose ol {{
    margin: 0.75rem 0 1.6rem 1.4rem;
    padding-left: 0.4rem;
    color: var(--text-secondary);
  }}
  .blog-article-prose li {{
    margin-bottom: 0.7rem;
    line-height: 1.75;
    font-size: 17px;
  }}
  .blog-article-prose a {{
    color: var(--orange);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.15s ease;
  }}
  .blog-article-prose a:hover {{ border-bottom-color: var(--orange); }}
  .blog-article-prose blockquote {{
    border-left: 3px solid var(--orange);
    padding: 0.4rem 0 0.4rem 1.2rem;
    margin: 1.8rem 0;
    color: var(--text-primary);
    font-size: 18px;
    line-height: 1.7;
  }}
  .blog-article-prose figure {{ margin: 2rem 0; }}
  .blog-article-prose figcaption {{
    font-size: 13px; color: var(--text-muted); margin-top: 8px;
    text-align: center;
  }}

  /* Article pages do not run the blog IntersectionObserver; `.reveal` would
     stay opacity:0 forever. Force related + CTA content visible. */
  .blog-related .reveal,
  .blog-end-cta .reveal {{
    opacity: 1;
    transform: none;
    transition: none;
  }}

  /* ── Related strip ─────────────────────────────────────────────── */
  .blog-related {{
    box-sizing: border-box;
    padding: 64px var(--pad-x) 72px;
  }}
  .blog-related-head {{ margin-bottom: var(--section-head-to-content); }}
  .blog-related-head h2 {{ margin: 8px 0 0; }}
  .blog-related-grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
    align-items: stretch;
  }}
  @media (min-width: 720px) {{
    .blog-related-grid {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  @media (min-width: 1024px) {{
    .blog-related-grid {{ grid-template-columns: repeat(3, 1fr); }}
  }}
  a.blog-list-card.card {{
    display: flex; flex-direction: column;
    padding: 0; overflow: hidden;
    text-decoration: none; color: inherit;
    height: 100%; min-height: 0;
  }}
  .blog-list-card-img-wrap {{
    aspect-ratio: 1; overflow: hidden;
    background: var(--bg-surface);
    flex-shrink: 0;
  }}
  .blog-list-card-img-wrap--empty {{
    background: linear-gradient(145deg, var(--orange-dim) 0%, var(--bg-alt) 55%, var(--bg-surface) 100%);
  }}
  .blog-list-card-img {{
    width: 100%; height: 100%; object-fit: cover; display: block;
  }}
  .blog-list-card-body {{
    padding: 20px 24px 24px;
    display: flex; flex-direction: column;
    flex: 1; gap: 10px; min-height: 0;
  }}
  .blog-list-card-title {{
    font-family: var(--font-display);
    font-size: clamp(16px, 1.5vw, 18px);
    font-weight: 600; line-height: 1.35;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0;
  }}
  .blog-list-card-meta {{
    font-size: 13px; font-weight: 500;
    color: var(--orange); margin-top: auto;
  }}

  /* ── End-of-article CTA band ───────────────────────────────────── */
  .blog-end-cta {{
    box-sizing: border-box;
    padding: 48px var(--pad-x) 96px;
    max-width: var(--max-w);
    margin: 0 auto;
  }}
  .blog-end-cta-card {{
    text-align: center;
    max-width: 720px; margin: 0 auto;
    padding: 56px clamp(28px, 4vw, 56px);
  }}
  .blog-end-cta-title {{
    font-family: var(--font-display);
    font-size: clamp(28px, 3vw, 38px);
    font-weight: 700; letter-spacing: -0.04em;
    line-height: 1.1;
    margin: 12px 0 16px;
  }}
  .blog-end-cta-copy {{
    font-size: 16px; line-height: 1.7;
    color: var(--text-secondary);
    max-width: 56ch; margin: 0 auto 28px;
  }}
  .blog-end-cta-actions {{
    display: inline-flex; flex-wrap: wrap; gap: 12px; justify-content: center;
  }}

  /* ── Mobile rhythm ─────────────────────────────────────────────── */
  @media (max-width: 768px) {{
    .blog-article-shell {{ padding: 76px var(--pad-x) 0; }}
    .blog-article-back {{ margin-bottom: 24px; }}
    .blog-article-header {{ margin-bottom: 28px; }}
    .blog-article-title {{ font-size: clamp(28px, 6vw, 36px); margin-bottom: 16px; }}
    .blog-article-lede {{ font-size: 18px; margin-bottom: 20px; }}
    .blog-article-share {{ margin-left: 0; width: 100%; padding-top: 4px; }}
    .blog-article-byline {{ gap: 12px; padding-top: 16px; }}
    .blog-article-hero {{ margin-bottom: 40px; border-radius: 14px; }}
    .blog-article-prose p {{ font-size: 16px; line-height: 1.75; margin-bottom: 1.2rem; }}
    .blog-article-prose > p:first-of-type {{ font-size: 17px; }}
    .blog-article-prose h2 {{ margin: 2rem 0 0.8rem; }}
    .blog-article-prose * + h2 {{ margin-top: 2rem; }}
    .blog-article-prose > h2:first-child,
    .blog-article-prose > h3:first-child {{ margin-top: 0; }}
    .blog-article-prose h3 {{ margin: 1.8rem 0 0.6rem; }}
    .blog-article-prose li {{ font-size: 16px; }}
    .blog-related {{ padding: 48px var(--pad-x) 56px; }}
    .blog-end-cta {{ padding: 40px var(--pad-x) 72px; }}
    .blog-end-cta-card {{ padding: 36px 24px; }}
  }}
</style>
</head>
<body>
<nav class="site-nav" aria-label="Primary">
  <div class="nav-inner">
    <a href="../papex-v2.html" class="nav-logo" aria-label="PapeX">
      <img src="../PapeX%20Logos/primary%20orange%20light.svg" alt="PapeX" />
    </a>
    <div class="nav-links">
      <a href="../pos-calculator.html">POS Calculator</a>
      <a href="#">About Us</a><!-- placeholder: link to about-us.html -->
      <a href="../papex-v2.html#pricing">Pricing</a>
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

  <header class="blog-article-header">
    <p class="blog-article-kicker">
      <span class="k-label">Blog</span>
      <span class="k-dot">·</span>
      <span>{escape(kicker_date)}</span>
      <span class="k-dot">·</span>
      <span>{read_time} min read</span>
    </p>
    <h1 class="blog-article-title">{escape(title)}</h1>
    {lede_block}
    <div class="blog-article-byline">
      <div class="blog-article-byline-meta">
        <span class="blog-article-mark" aria-hidden="true">
          <img src="../PapeX%20Logos/primary%20orange%20light.svg" alt="" />
        </span>
        <span class="blog-article-byline-name">PapeX Team</span>
        <span class="blog-article-byline-date">{escape(kicker_date)}</span>
      </div>
      {share_block}
    </div>
  </header>

  {hero}

  <article class="blog-article-prose">
      {article_html_block}
  </article>
</main>
{related_html}
{cta_html}

<footer>
  <div class="footer-inner">
    <div class="footer-logo-row">
      <a href="../papex-v2.html" class="footer-logo" aria-label="PapeX">
        <img src="../PapeX%20Logos/primary%20orange%20light.svg" alt="PapeX" />
      </a>
    </div>
    <div class="footer-grid">
      <div class="footer-col footer-col--brand">
        <p class="footer-blurb">Download the PapeX app and keep every receipt in one place. Purchases sync automatically after checkout so you never lose proof for returns, expenses, or tax time.</p>
        <a href="../papex-v2.html#hero" class="btn-app-store">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>
          <div class="app-dl-text">
            <span class="app-dl-small">Download on the</span>
            <span class="app-dl-big">App Store</span>
          </div>
        </a>
      </div>
      <nav class="footer-col footer-col--nav" aria-label="Footer">
        <a href="../pos-calculator.html">POS Calculator</a>
        <a href="#">About Us</a><!-- placeholder: link to about-us.html -->
        <a href="../papex-v2.html#pricing">Pricing</a>
        <a href="../blog.html">Blog</a>
      </nav>
    </div>
    <p class="footer-copy">© 2026 PapeX Inc. All rights reserved.</p>
  </div>
</footer>
<script>
(function () {{
  window.addEventListener('scroll', function () {{
    var bar = document.querySelector('.site-nav');
    if (bar) bar.style.boxShadow = window.scrollY > 20 ? '0 1px 0 rgba(0,0,0,0.06)' : 'none';
  }}, {{ passive: true }});
  var copyBtns = document.querySelectorAll('.blog-article-copy');
  copyBtns.forEach(function (btn) {{
    btn.addEventListener('click', function () {{
      var url = btn.getAttribute('data-copy-url') || window.location.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(url).then(function () {{
          btn.classList.add('blog-article-copy--ok');
          setTimeout(function () {{ btn.classList.remove('blog-article-copy--ok'); }}, 1200);
        }});
      }}
    }});
  }});
}})();
</script>
</body>
</html>
"""


def main() -> int:
    sections = split_sections(MARKDOWN_PATH.read_text(encoding="utf-8"))
    if len(sections) != 24:
        raise SystemExit(f"Expected 24 sections, found {len(sections)}")

    meta_rows = json.loads(META_PATH.read_text(encoding="utf-8"))
    meta = {row["slug"]: row for row in meta_rows}

    urls = [ln.strip() for ln in URLS_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    slugs = [slug_from_url(u) for u in urls]

    cleaned_sections = []
    sections_by_title = {}
    for title, body in sections:
        clean = clean_body(body)
        cleaned_sections.append((title, clean))
        sections_by_title.setdefault(norm(title), []).append(clean)

    fallback_key_by_slug = {
        "hidden-cost-paper-receipts": "every day, millions of shoppers walk away from stores clutching small paper receipts",
        "history-of-receipts": "that's how receipts started",
        "secret-life-shopping-receipt": "let's follow one receipt on its unlikely journey",
        "why-business-owners-hate-printing-receipts": "your lunch rush just ended",
    }

    assigned: dict[str, str] = {}
    used_ids = set()

    for slug in slugs:
        title = meta.get(slug, {}).get("title", slug.replace("-", " ").title())
        bucket = sections_by_title.get(norm(title), [])
        body = None
        for idx, val in enumerate(bucket):
            token = (norm(title), idx)
            if token in used_ids:
                continue
            body = val
            used_ids.add(token)
            break
        if body is None and slug in fallback_key_by_slug:
            needle = fallback_key_by_slug[slug]
            for i, (raw_title, raw_body) in enumerate(cleaned_sections):
                if needle in raw_body.lower() and (raw_title, i) not in used_ids:
                    body = raw_body
                    used_ids.add((raw_title, i))
                    break
        if body is None:
            for i, (raw_title, raw_body) in enumerate(cleaned_sections):
                if (raw_title, i) not in used_ids:
                    body = raw_body
                    used_ids.add((raw_title, i))
                    break
        assigned[slug] = body or ""

    md_sections = []
    for slug in slugs:
        row = meta.get(slug, {})
        title = row.get("title", slug.replace("-", " ").title())
        body = assigned[slug].strip()
        md_sections.append(f"# {title}\n\n{body}".strip())

    MARKDOWN_PATH.write_text("\n\n---\n\n".join(md_sections) + "\n", encoding="utf-8")

    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    total = len(slugs)
    for idx, slug in enumerate(slugs):
        row = meta.get(slug, {})
        title = row.get("title", slug.replace("-", " ").title())
        body_md = assigned[slug]
        lede, body_after_lede = extract_lede(body_md)
        body_html = markdown_block_to_html(body_after_lede)
        cover = row.get("coverFile")
        cover_rel = "../" + cover if cover else None
        kicker_date = format_publish_date(idx, total)
        read_time = compute_read_time(body_md)
        lede_html = md_inline_to_html(lede) if lede else ""
        related_html = render_related_strip(slug, slugs, meta)
        cta_html = render_cta_band()
        html = article_html(
            title=title,
            hero_rel=cover_rel,
            article_html_block=body_html,
            slug=slug,
            kicker_date=kicker_date,
            read_time=read_time,
            lede_html=lede_html,
            related_html=related_html,
            cta_html=cta_html,
        )
        (ARTICLES_DIR / f"{slug}.html").write_text(html, encoding="utf-8")

    print(f"Updated markdown: {MARKDOWN_PATH}")
    print(f"Updated {len(slugs)} article pages in {ARTICLES_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
