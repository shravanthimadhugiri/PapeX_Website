/**
 * Crawl https://www.papex.app/blog, collect post URLs, render each page with
 * Playwright, extract article prose (h1, headings, paragraphs, lists), and
 * write Markdown to ../../papex-blog-content.md (Downloads root).
 *
 * Setup:
 *   cd PapeX/scripts && npm install
 *   npx playwright install chromium
 *
 * Run:
 *   npm run fetch-blog
 *   node fetch-blog-to-markdown.mjs
 */

import { chromium } from "playwright";
import { writeFileSync, readFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BLOG_INDEX = "https://www.papex.app/blog";
const EXPECTED_POST_COUNT = 24;
const OUT_FILE = join(__dirname, "..", "..", "papex-blog-content.md");
const FALLBACK_URLS_FILE = join(__dirname, "..", "..", "blog-post-urls.txt");

function normalizePostUrls(hrefs, base) {
  const baseUrl = new URL(base);
  const seen = new Set();
  const urls = [];
  for (const raw of hrefs) {
    let u;
    try {
      u = new URL(raw, baseUrl);
    } catch {
      continue;
    }
    if (u.hostname !== baseUrl.hostname) continue;
    const path = u.pathname.replace(/\/$/, "");
    const m = path.match(/^\/blog\/([^/]+)$/);
    if (!m) continue;
    if (m[1] === "blog" || m[1] === "") continue;
    const canonical = `${baseUrl.origin}/blog/${m[1]}`;
    if (seen.has(canonical)) continue;
    seen.add(canonical);
    urls.push(canonical);
  }
  return urls.sort();
}

function loadFallbackUrls() {
  if (!existsSync(FALLBACK_URLS_FILE)) return [];
  return readFileSync(FALLBACK_URLS_FILE, "utf8")
    .split("\n")
    .map((l) => l.trim())
    .filter(Boolean);
}

/**
 * Serialized into the page — must not close over Node scope.
 * @returns {Array<{tag: string, text?: string, lines?: string[]}>}
 */
function extractArticleBlocksInPage() {
  const ARTICLE_ROOT_SELECTORS = [
    "main article",
    "article",
    '[role="main"] article',
    '[role="main"]',
    "main",
  ];
  const REMOVE_SELECTOR =
    "nav, header, footer, script, style, iframe, noscript, [role='navigation']";

  function findArticleRoot() {
    for (const sel of ARTICLE_ROOT_SELECTORS) {
      const el = document.querySelector(sel);
      if (el && el.textContent?.trim()) return el;
    }
    return document.body;
  }

  function stripNoise(root) {
    root.querySelectorAll(REMOVE_SELECTOR).forEach((n) => n.remove());
  }

  function inlineText(el) {
    const parts = [];
    const walk = (node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const t = node.textContent?.replace(/\s+/g, " ") ?? "";
        if (t) parts.push(t);
        return;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      const tag = node.tagName.toLowerCase();
      if (tag === "br") {
        parts.push("\n");
        return;
      }
      if (tag === "strong" || tag === "b") {
        const inner = [];
        node.childNodes.forEach((c) => {
          if (c.nodeType === Node.TEXT_NODE)
            inner.push(c.textContent?.replace(/\s+/g, " ") ?? "");
          else if (c.nodeType === Node.ELEMENT_NODE) walk(c);
        });
        const t = inner.join("").trim();
        if (t) parts.push(`**${t}**`);
        return;
      }
      if (tag === "em" || tag === "i") {
        const inner = [];
        node.childNodes.forEach((c) => {
          if (c.nodeType === Node.TEXT_NODE)
            inner.push(c.textContent?.replace(/\s+/g, " ") ?? "");
          else if (c.nodeType === Node.ELEMENT_NODE) walk(c);
        });
        const t = inner.join("").trim();
        if (t) parts.push(`*${t}*`);
        return;
      }
      node.childNodes.forEach(walk);
    };
    walk(el);
    return parts.join("").replace(/\s+/g, " ").trim();
  }

  /** @param {HTMLLIElement} li */
  function listItemMarkdown(li, indent, ordered, itemIndex) {
    const pad = "  ".repeat(indent);
    const prefix = ordered ? `${itemIndex}. ` : "- ";

    const clone = li.cloneNode(true);
    const nested = [];
    clone.querySelectorAll(":scope > ul, :scope > ol").forEach((list) => {
      nested.push(list);
      list.remove();
    });
    const main = inlineText(clone).trim();
    const lines = [];
    if (main) lines.push(`${pad}${prefix}${main}`);

    nested.forEach((list) => {
      const isOl = list.tagName.toLowerCase() === "ol";
      let idx = 1;
      list.querySelectorAll(":scope > li").forEach((sub) => {
        lines.push(...listItemMarkdown(sub, indent + 1, isOl, idx++));
      });
    });
    return lines;
  }

  const root = findArticleRoot();
  stripNoise(root);

  const blocks = [];
  const skipTags = new Set([
    "nav",
    "header",
    "footer",
    "script",
    "style",
    "iframe",
    "noscript",
  ]);

  function emitBlock(tag, text) {
    const t = text.replace(/\s+/g, " ").trim();
    if (!t) return;
    blocks.push({ tag, text: t });
  }

  function walkContainer(container) {
    for (const node of container.childNodes) {
      if (node.nodeType === Node.TEXT_NODE) {
        const looseText = (node.textContent || "").replace(/\s+/g, " ").trim();
        // Some layouts place paragraph text directly under container nodes.
        if (looseText.length >= 20) emitBlock("p", looseText);
        continue;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) continue;
      const el = /** @type {Element} */ (node);
      const tag = el.tagName.toLowerCase();
      if (skipTags.has(tag)) continue;

      if (/^h[1-6]$/.test(tag)) {
        emitBlock(tag, inlineText(el));
        continue;
      }
      if (tag === "p") {
        emitBlock("p", inlineText(el));
        continue;
      }
      if (tag === "ul") {
        const lines = [];
        let i = 1;
        el.querySelectorAll(":scope > li").forEach((li) => {
          lines.push(...listItemMarkdown(/** @type {HTMLLIElement} */ (li), 0, false, i++));
        });
        if (lines.length) blocks.push({ tag: "ul", lines });
        continue;
      }
      if (tag === "ol") {
        const lines = [];
        let i = 1;
        el.querySelectorAll(":scope > li").forEach((li) => {
          lines.push(...listItemMarkdown(/** @type {HTMLLIElement} */ (li), 0, true, i++));
        });
        if (lines.length) blocks.push({ tag: "ol", lines });
        continue;
      }
      if (tag === "section" || tag === "div" || tag === "article") {
        // Some posts render prose in block containers instead of <p>.
        const hasStructuredChildren = !!el.querySelector(
          "h1,h2,h3,h4,h5,h6,p,ul,ol,li,blockquote,table"
        );
        if (!hasStructuredChildren) {
          const containerText = inlineText(el);
          if (containerText.length >= 15) emitBlock("p", containerText);
        }
        walkContainer(el);
        continue;
      }
    }
  }

  walkContainer(root);
  return blocks;
}

function blocksToMarkdown(blocks) {
  const parts = [];
  for (const b of blocks) {
    if (b.tag === "p") {
      parts.push(b.text);
      continue;
    }
    if (/^h[1-6]$/.test(b.tag)) {
      const level = Number(b.tag[1]);
      const hashes = "#".repeat(Math.min(6, Math.max(1, level)));
      parts.push(`${hashes} ${b.text}`);
      continue;
    }
    if (b.tag === "ul" || b.tag === "ol") {
      parts.push(b.lines.join("\n"));
    }
  }
  return parts.join("\n\n").trim();
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function discoverPostUrls(page) {
  // Avoid waitUntil: "networkidle" — SPAs often keep connections open and never idle.
  await page.goto(BLOG_INDEX, { waitUntil: "domcontentloaded", timeout: 90000 });
  await page
    .locator("a[href*='/blog/']")
    .first()
    .waitFor({ state: "attached", timeout: 45000 });
  await sleep(2000);
  const hrefs = await page.$$eval("a[href*='/blog/']", (as) =>
    as.map((a) => a.getAttribute("href") || "")
  );
  let urls = normalizePostUrls(hrefs, BLOG_INDEX);
  const indexCount = urls.length;
  const fallback = normalizePostUrls(loadFallbackUrls(), BLOG_INDEX);

  if (urls.length !== EXPECTED_POST_COUNT && fallback.length === EXPECTED_POST_COUNT) {
    if (urls.length > EXPECTED_POST_COUNT) {
      const fbSet = new Set(fallback);
      const inter = urls.filter((u) => fbSet.has(u)).sort();
      urls = inter.length === EXPECTED_POST_COUNT ? inter : fallback;
      console.warn(
        `Index had ${indexCount} /blog/slug links; narrowed to ${EXPECTED_POST_COUNT} using blog-post-urls.txt`
      );
    } else {
      console.warn(
        `Index found ${urls.length} posts; using ${fallback.length} URLs from blog-post-urls.txt`
      );
      urls = fallback;
    }
  } else if (urls.length !== EXPECTED_POST_COUNT) {
    console.warn(
      `Expected ${EXPECTED_POST_COUNT} posts, found ${urls.length} on index (fallback has ${fallback.length}). Proceeding with collected URLs.`
    );
  }
  return urls;
}

async function extractOnePage(page, url) {
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 90000 });
  await page.waitForLoadState("networkidle", { timeout: 45000 }).catch(() => {});
  const blocks = await page.evaluate(extractArticleBlocksInPage);
  const h1Blocks = blocks.filter((b) => b.tag === "h1");
  const title =
    h1Blocks[0]?.text?.trim() ||
    (await page.title()).replace(/\s*\|\s*PapeX.*$/i, "").trim();
  const bodyBlocks = blocks.filter((b) => b.tag !== "h1");
  const bodyMd = blocksToMarkdown(bodyBlocks);
  return { title, bodyMd };
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  });
  const page = await context.newPage();

  const urls = await discoverPostUrls(page);

  if (urls.length === 0) {
    await browser.close();
    throw new Error("No blog post URLs discovered.");
  }

  const sections = [];
  for (let i = 0; i < urls.length; i++) {
    const url = urls[i];
    process.stdout.write(`[${i + 1}/${urls.length}] ${url}\n`);
    const { title, bodyMd } = await extractOnePage(page, url);
    const header = `# ${title.replace(/^#+\s*/, "").trim()}`;
    const piece = [header, "", bodyMd].filter(Boolean).join("\n");
    sections.push(piece);
  }

  await browser.close();

  const out = sections.join("\n\n---\n\n") + "\n";
  writeFileSync(OUT_FILE, out, "utf8");
  console.log(`Wrote ${sections.length} articles to ${OUT_FILE}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
