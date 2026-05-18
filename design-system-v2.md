# PapeX Design System v2

Marketing website and brand UI spec for **`papex-v3.html`** and **`papex-v3.css`**.

**Layout reference:** [Flighty](https://www.flighty.com) — centered hero, generous whitespace, soft floating notification cards around a phone mockup (`papex-v3-reference-flighty.png`).

**Product reference:** PapeX app mockup (`papex-v3-mockup.png`) — dark in-app UI on a white marketing canvas.

> This document supersedes v1 marketing rules for the v3 site. It does **not** describe glass cards, `#F2FCFF` bands, or dark marketing canvases from the legacy system.

---

## 1. Principles

| Principle | Rule |
|-----------|------|
| **White canvas** | Page background is always **`#FFFFFF`**. No light-blue tints on the marketing site. |
| **Flighty-inspired layout** | Centered headline → subcopy → horizontal badge row → hero stage (mockup + floating cards). Primary download CTA lives in the nav. |
| **Consumer-first** | Hero sells the app; business/investor content lives below the fold. |
| **Restraint** | Orange is for logo accent, nav emphasis, eyebrows, and key highlights — not full sections. |
| **App vs web** | In-app UI is **dark** (`#121B22` family). The **website** stays light; the mockup carries the dark product UI. |

---

## 2. Color

### 2.1 Marketing (website)

| Token | Hex | Usage |
|-------|-----|--------|
| `--bg` | `#FFFFFF` | Page, hero, nav, default cards |
| `--bg-alt` | `#FAFAFA` | Alternating sections only (not blue) |
| `--bg-subtle` | `#F5F5F5` | Stat tiles, icon wells, float card icons |
| `--text` | `#000000` | H1, primary emphasis |
| `--text-secondary` | `#666666` | Body, nav links, subheads |
| `--text-muted` | `#888888` | Labels, meta, badge secondary lines |
| `--orange` | `#F07C26` | Logo mark, eyebrows, primary buttons (nav drawer, sections) |
| `--orange-hover` | `#E06D00` | CTA hover |
| `--border` | `rgba(0, 0, 0, 0.1)` | Cards, inputs, dividers |
| `--green` | `#16A34A` | Live / success indicators (badges, float checkmarks) |

**Do not use:** `#F2FCFF`, `#EEF9FC`, ice/mint section fills, or blue gradients on the website.

### 2.2 In-app UI (mockup / product)

| Token | Hex | Usage |
|-------|-----|--------|
| App background | `#121B22` | Screen base |
| Card surface | `#1E2B37` | Summary cards, list container |
| Primary text | `#FFFFFF` | Amounts, merchant names |
| Secondary text | `#94A3B8` | Categories, dates, labels |
| Accent | `#F07C26` | Logo icon, “Add receipt” FAB |

---

## 3. Typography

**Fonts (Google Fonts):**

- **Plus Jakarta Sans** — display: H1–H4, prices, stat values  
- **Inter** — body, nav, buttons, UI copy  

| Role | Font | Weight | Size (desktop) | Color |
|------|------|--------|----------------|-------|
| Hero H1 | Plus Jakarta Sans | 700 | `clamp(2.5rem, 5.5vw, 3.5rem)` | `#000000` |
| Hero subcopy | Inter | 400 | 17px | `#666666` |
| Section H2 | Plus Jakarta Sans | 600 | ~38px | `#000000` |
| Body | Inter | 400 | 17px | `#666666` |
| Nav links | Inter | 400 | 15px | `#666666` |
| Eyebrow | Inter | 600 | 12px, uppercase, +0.08em | `#F07C26` |
| Float card title | Inter | 600 | 14px | `#000000` |
| Float card meta | Inter | 400 | 12px | `#888888` |

**Letter-spacing:** Tight on headlines (`-0.03em` to `-0.04em`). Normal on body.

**Hierarchy (Flighty pattern):** Weight and color establish importance more than size jumps — bold black titles, grey secondary lines.

---

## 4. Layout

### 4.1 Grid & width

- **Max content width:** `1280px` (`--hero-max`) for nav + hero  
- **Section content:** `1120px` (`--max-w`)  
- **Hero stage max:** `980px` (mockup + floats)  
- **Horizontal padding:** `24px` (mobile `16px`)  

### 4.2 Section rhythm

- **Section padding:** `96px` vertical (mobile `64px`)  
- **Intro block → content:** `48px`  
- **Hero top padding:** `nav height + 56px`  
- **Hero copy → stage:** `48px` between subcopy and mockup stage  

### 4.3 Alternating sections

Odd sections: `#FFFFFF`  
Even bands: `#FAFAFA` with `1px` top/bottom border `rgba(0,0,0,0.1)`  

---

## 5. Navigation

**Structure (desktop):** 3-column grid — logo left, links centered, CTA right (mirrors Flighty).

| Link order | Label |
|------------|--------|
| 1 | Pricing |
| 2 | POS Calculator |
| 3 | Blog |
| 4 | About Us |

**Right CTA:** Text link **“Get the app”** + phone outline icon (not a filled orange pill in the nav).

| Property | Value |
|----------|--------|
| Height | `64px` |
| Background | `rgba(255,255,255,0.9)` + `backdrop-filter: blur(12px)` |
| Border | `1px solid rgba(0,0,0,0.1)` bottom |
| Logo height | `32px` |

**Mobile:** Hamburger → full-screen drawer; primary CTA as orange button at bottom of drawer.

---

## 6. Hero (Flighty-inspired)

**Order (top → bottom):**

1. Centered H1 (black, bold)  
2. Centered subcopy (max ~38rem, grey)  
3. Horizontal **badge row** (App Store live + Google Play coming soon)  
4. **Hero stage:** phone mockup centered, with **floating notification cards** layered around it  

**No** hero gradient. **No** filled orange CTA in the hero body — download action is in the nav (and sticky mobile bar).

### 6.1 Badge row (Flighty award-badge pattern)

Two inline items, icon left + stacked text right:

| Badge | Icon | Primary line | Secondary line |
|-------|------|--------------|----------------|
| App Store | Green check circle | Live on the App Store | Free for consumers |
| Google Play | Play glyph | Google Play | Coming soon |

- Layout: centered flex row, `28–36px` gap  
- Primary line: 15px semibold `#000000`  
- Secondary: 13px `#888888`  

### 6.2 Hero stage & mockup

- **Container:** `.v3-hero__stage` — `position: relative`, centered  
- **Mockup file:** `papex-v3-mockup.png` (hand + iPhone, transparent/black edges)  
- **Image:** max-width `720px`, centered, `z-index: 2`  
- **Background:** white page only; depth comes from the asset and float cards  

### 6.3 Floating notification cards (Flighty pattern)

Rounded rectangles with soft diffused shadow, partially overlapping the mockup:

| Property | Value |
|----------|--------|
| Radius | `18px` |
| Background | `#FFFFFF` |
| Border | `1px solid rgba(0,0,0,0.06)` |
| Shadow | `0 8px 32px rgba(15,23,42,0.1)` |
| Padding | `14px 16px` |
| Icon well | `40×40px`, `12px` radius, `#F5F5F5` fill |
| Title | 14px semibold black |
| Meta | 12px `#888888` |

**Example content (PapeX-themed):** MegaStore capture, Receipt saved, Email forwarded, Chipotle receipt.

**Responsive:** Float cards **hidden** at `≤860px`; mockup remains full-width.

---

## 7. Components (below hero)

### 7.1 Cards

- Background: `#FFFFFF`  
- Border: `1px solid rgba(0,0,0,0.1)`  
- Radius: `20px` (`--radius-lg`)  
- Shadow: `0 1px 3px rgba(0,0,0,0.06)` optional; hover `0 12px 40px rgba(0,0,0,0.08)` on linked cards only  
- **No** glass, **no** `backdrop-filter`, **no** scale-on-hover on static content  

### 7.2 Buttons

| Variant | Background | Border | Text |
|---------|------------|--------|------|
| Primary | `#F07C26` | none | `#FFFFFF` |
| Ghost | `#FFFFFF` | `1px` border | `#000000` |

Radius: pill (`999px`) for section CTAs.

### 7.3 Eyebrow

Uppercase orange label above section H2. One per section max.

### 7.4 Pricing

- Three columns; center card **featured** with orange border + **“Most popular”** pill on top edge  
- Amount typography: Plus Jakarta Sans bold  

### 7.5 FAQ

- Accordion; `+` / `−` toggle  
- Max width ~40rem when centered  

### 7.6 Trust strip

- White background, border bottom only  
- Pilot labels as white pills with grey border (not blue band)  

---

## 8. Imagery & icons

| Asset | Path |
|-------|------|
| Logo | `PapeX Logos/primary orange light.svg` |
| Hero mockup | `papex-v3-mockup.png` |
| Layout reference (Flighty) | `papex-v3-reference-flighty.png` |

**Icons:** Lucide-style stroke icons, `20px`, orange or `#666666` on light surfaces. Float cards may use emoji or simple glyphs in icon wells.

---

## 9. Motion

- Scroll reveal: fade + `16px` translate, `0.5s` ease, once  
- Nav: subtle bottom shadow on scroll  
- Respect `prefers-reduced-motion` (add if not yet in CSS)  
- Float cards: static (no animation required for v1; optional subtle float later)  

---

## 10. Responsive

| Breakpoint | Behavior |
|------------|----------|
| `≤860px` | Nav collapses to drawer; float cards hidden |
| `≤960px` | Grids → 1–2 columns |
| `≤720px` | Comparison table hidden; card list shown |
| `≤520px` | Hero badges stack vertically |
| Mobile | Sticky bottom **Get the app** bar |

---

## 11. Files

| File | Role |
|------|------|
| `papex-v3.html` | Marketing page markup |
| `papex-v3.css` | v2 tokens + layout (standalone) |
| `design-system-v2.md` | This spec |
| `papex-v2.html` | Legacy; unchanged |

---

## 12. Checklist before shipping

- [ ] All section backgrounds are `#FFFFFF` or `#FAFAFA` only  
- [ ] Hero uses `papex-v3-mockup.png` in stage below copy  
- [ ] Float cards match Flighty layering pattern (desktop only)  
- [ ] Nav matches link order + text “Get the app” CTA  
- [ ] App Store URL set in `PAPEX_APP_STORE_URL`  
- [ ] No imports from `papex-shared.css` on v3  
