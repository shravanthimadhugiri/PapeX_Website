# PapeX Design System v2

Marketing website and brand UI spec for **`papex-v3.html`** and **`papex-v3.css`**.

**Layout reference:** Centered hero with top light blue gradient, generous whitespace, primary CTAs inline (`papex-v3-reference.png`). Nav and typography structure inspired by Flighty.

**Product reference:** PapeX app mockup (`papex-v3-mockup.png`) — dark in-app UI on a white/light marketing canvas.

> This document supersedes v1 marketing rules for the v3 site. It retains the dark product UI against a bright canvas but updates the layout and hero constraints.

---

## 1. Principles

| Principle | Rule |
|-----------|------|
| **Primary White Canvas** | The primary page background is always **`#FFFFFF`**. The only exception is the header/hero section, which features a light blue gradient fading to `#FFFFFF`. |
| **Updated Layout** | Centered headline → subcopy → horizontal CTA row → hero stage (standalone mockup held by hand). |
| **Consumer-first** | Hero sells the app; business/investor content lives below the fold. |
| **Restraint** | Orange is for logo accent, nav emphasis, eyebrows, and key highlights — and now specifically the primary hero CTA. |
| **App vs web** | In-app UI is **dark** (`#121B22` family). The **website** stays light; the mockup carries the dark product UI. |

---

## 2. Color

### 2.1 Marketing (website)

| Token | Hex | Usage |
|-------|-----|--------|
| `--bg` | `#FFFFFF` | Primary page background, nav, default cards |
| `--bg-hero-gradient` | `#EEF9FC` to `#FFFFFF` | Light blue top gradient exclusively for the header/hero section |
| `--bg-alt` | `#FAFAFA` | Alternating sections only (not blue) |
| `--bg-subtle` | `#F5F5F5` | Stat tiles, icon wells, float card icons |
| `--text` | `#000000` | H1, primary emphasis |
| `--text-secondary` | `#666666` | Body, nav links, subheads |
| `--text-muted` | `#888888` | Labels, meta, badge secondary lines |
| `--orange` | `#F07C26` | Logo mark, eyebrows, primary buttons (hero CTA, nav drawer, sections) |
| `--orange-hover` | `#E06D00` | CTA hover |
| `--border` | `rgba(0, 0, 0, 0.1)` | Cards, inputs, dividers |
| `--green` | `#16A34A` | Live / success indicators |

**Do not use:** Blue gradients outside of the header/hero. Ice/mint section fills remain prohibited in the body of the page.

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
| Component title | Inter | 600 | 14px | `#000000` |
| Component meta | Inter | 400 | 12px | `#888888` |

**Letter-spacing:** Tight on headlines (`-0.03em` to `-0.04em`). Normal on body.

**Hierarchy:** Weight and color establish importance more than size jumps — bold black titles, grey secondary lines.

---

## 4. Layout

### 4.1 Grid & width

- **Max content width:** `1280px` (`--hero-max`) for nav + hero  
- **Section content:** `1120px` (`--max-w`)  
- **Hero stage max:** `980px` (mockup)  
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

**Structure (desktop):** 3-column grid — logo left, links centered, CTA right.

| Link order | Label |
|------------|--------|
| 1 | Pricing |
| 2 | POS Calculator |
| 3 | Blog |
| 4 | About Us |

**Right CTA:** Text link **“Get the app”** + phone outline icon.

| Property | Value |
|----------|--------|
| Height | `64px` |
| Background | Transparent (inherits from hero gradient at top, defaults to white below) |
| Border | None on top gradient, `1px solid rgba(0,0,0,0.1)` when sticky/scrolling |
| Logo height | `32px` |

**Mobile:** Hamburger → full-screen drawer; primary CTA as orange button at bottom of drawer.

---

## 6. Hero

**Order (top → bottom):**

1. Centered H1 (black, bold)  
2. Centered subcopy (max ~38rem, grey)  
3. Horizontal **CTA row** (Orange Get the app + White Google Play)  
4. **Hero stage:** phone mockup held by hand, centered, standing alone.  

**Background:** Uses the top light blue gradient fading down to white (`--bg-hero-gradient`).

### 6.1 CTA row

Two inline pill buttons:

| Button | Style | Content |
|--------|-------|---------|
| Get the app | Primary (Orange fill) | Mobile phone icon + "Get the app" |
| Google Play | Ghost (White fill, outline) | "COMING SOON TO" + Google Play logo |

- Layout: centered flex row, `24px` gap  

### 6.2 Hero stage & mockup

- **Container:** `.v3-hero__stage` — `position: relative`, centered  
- **Mockup file:** `papex-v3-mockup.png` (hand + iPhone)  
- **Image:** max-width `720px`, centered, `z-index: 2`  
- **Note:** Floating notification cards are **not** used in the hero section.

---

## 7. Components (below hero)

### 7.1 Floating notification cards (Reserved for future/other sections)

*Note: Not used in the hero, but kept for potential use elsewhere in the UI.*

Rounded rectangles with soft diffused shadow:

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

### 7.2 Cards

- Background: `#FFFFFF`  
- Border: `1px solid rgba(0,0,0,0.1)`  
- Radius: `20px` (`--radius-lg`)  
- Shadow: `0 1px 3px rgba(0,0,0,0.06)` optional; hover `0 12px 40px rgba(0,0,0,0.08)` on linked cards only  
- **No** glass, **no** `backdrop-filter`, **no** scale-on-hover on static content  

### 7.3 Buttons

| Variant | Background | Border | Text |
|---------|------------|--------|------|
| Primary | `#F07C26` | none | `#FFFFFF` |
| Ghost | `#FFFFFF` | `1px` border | `#000000` |

Radius: pill (`999px`) for primary CTAs like in the hero.

### 7.4 Eyebrow

Uppercase orange label above section H2. One per section max.

### 7.5 Pricing

- Three columns; center card **featured** with orange border + **“Most popular”** pill on top edge  
- Amount typography: Plus Jakarta Sans bold  

### 7.6 FAQ

- Accordion; `+` / `−` toggle  
- Max width ~40rem when centered  

### 7.7 Trust strip

- White background, border bottom only  
- Pilot labels as white pills with grey border (not blue band)  

---

## 8. Imagery & icons

| Asset | Path |
|-------|------|
| Logo | `PapeX Logos/primary orange light.svg` |
| Hero mockup | `papex-v3-mockup.png` |
| Layout reference | `papex-v3-reference.png` |

**Icons:** Lucide-style stroke icons, `20px`, orange or `#666666` on light surfaces. 

---

## 9. Motion

- Scroll reveal: fade + `16px` translate, `0.5s` ease, once  
- Nav: subtle bottom shadow on scroll  
- Respect `prefers-reduced-motion`  

---

## 10. Responsive

| Breakpoint | Behavior |
|------------|----------|
| `≤860px` | Nav collapses to drawer |
| `≤960px` | Grids → 1–2 columns |
| `≤720px` | Comparison table hidden; card list shown |
| `≤520px` | Hero CTAs stack vertically |
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

- [ ] Header/Hero features the light blue gradient fading to `#FFFFFF`.
- [ ] All other section backgrounds are `#FFFFFF` or `#FAFAFA` only.
- [ ] Hero stage displays the standalone mockup held by hand.
- [ ] Hero includes the prominent orange "Get the app" CTA.
- [ ] Nav matches link order + text “Get the app” CTA.
- [ ] App Store URL set in `PAPEX_APP_STORE_URL`.
- [ ] No imports from `papex-shared.css` on v3.
