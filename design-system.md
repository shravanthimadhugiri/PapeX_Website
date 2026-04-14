# PapeX Design System
### Fintech SaaS Marketing Website — Cursor Reference File

> Paste relevant sections into Cursor chat when generating UI. These are standing rules —
> not one-time instructions. Content copy changes go in chat directly, not here.

---

## 0. Light Mode (Marketing Website — Permanent Default)

**Permanent rule:** The marketing website is **light mode**. This overrides any prior dark-theme styling in CSS, Figma notes, or older prompts. **Do not** revert the live page (`papex-v2.html`) to dark backgrounds unless the stakeholder explicitly requests it.

**Directive for `papex-v2.html` and new landing work:**

- **Page background:** `#FFFFFF` (`--bg-primary`). Do not use dark navy as the primary canvas.
- **Surfaces:** Cards `#F0FAFD` (`--bg-card`), hover / subtle fill `#E8F4F8` (`--bg-card-hover`, `--bg-surface`).
- **Accent:** Brand orange `#E06D00` (`--orange`) for CTAs, labels, links, and icon wells — accent only, never full-page fill.
- **Text:** Primary `#0F172A` (`--text-primary`), body secondary `#475569` (`--text-secondary`), meta `#94A3B8` (`--text-muted`).
- **Borders:** `rgba(0, 0, 0, 0.08)` (`--border`), light dividers `rgba(0, 0, 0, 0.04)` (`--border-light`).
- **Navbar:** `rgba(255, 255, 255, 0.92)` with `backdrop-filter: blur(16px)` and `border-bottom: 1px solid rgba(0, 0, 0, 0.06)`.
- **Cards:** Background `#F0FAFD`, border `1px solid rgba(0, 0, 0, 0.08)`, shadow `0 2px 12px rgba(0, 0, 0, 0.06)`.
- **Hero:** Subtle radial / linear orange tint behind the headline (low opacity) — not loud full-page gradients.
- **Icons:** **Lucide** stroke icons in **orange-dim** boxes (40×40px, 8px radius) — no emoji in UI chrome.
- **Typography (Google Fonts):** **Plus Jakarta Sans** (display / H1–H4 in `papex-v2.html`), **Inter** (body / UI), **JetBrains Mono** (metrics, money, stats, tables).

**Spacing (landing page):** Section vertical padding **120px** desktop / **72px** mobile; **56px** (desktop) / **40px** (mobile) from section intro block to main content; section label to H2 **24px**; H2 to intro paragraph **20px**; default grid gaps between cards **24px**; card interior padding **32px**; body paragraphs **margin-bottom: 1.5em** unless a component overrides.

Dark-theme tokens in §2 remain for **optional** product UI or decks only — not the default marketing site.

---

## 1. Brand Design Philosophy

### Core Premise

PapeX is infrastructure, not an app. On the **marketing site**, that reads as **bright, precise, and trustworthy**: white space, clear type, and disciplined use of orange — not decoration-heavy.

For **dark presentations or product UI**, the language can stay deep, dark, and precise. Every pixel communicates reliability. The interface earns trust through restraint — not decoration.

The light marketing aesthetic pairs **Plus Jakarta Sans** (display / headings in `papex-v2.html`) with **Inter** (body) and **JetBrains Mono** (data). Orange stays the single warm accent (CTAs, highlights, icon wells).

### Tone

| Axis | Direction |
|------|-----------|
| Personality | Composed, direct, operationally confident |
| Voice | Plain language — no jargon, no fluff |
| Aesthetic | Modern fintech infrastructure — not consumer startup |
| Emotional register | Trust, automation, relief |

### What PapeX Is Not

- No purple gradients or generic “AI slop” palettes (even on light backgrounds)
- No playful / illustrative / friendly startup aesthetic
- No legacy enterprise gray
- No crypto / Web3 glow effects
- No marketing-heavy stock photography
- No generic AI purple-blue color schemes

---

## 2. Color System

### Brand Tokens — Light (Marketing Default)

```css
:root {
  /* Brand Identity */
  --orange:           #E06D00;
  --orange-hover:     #F07A00;
  --orange-dim:       rgba(224,109,0,0.12);
  --orange-border:    rgba(224,109,0,0.28);

  /* Backgrounds — light (canonical marketing tokens) */
  --bg-primary:       #FFFFFF;   /* Page base */
  --bg-card:          #F0FAFD;   /* Cards, panels */
  --bg-card-hover:    #E8F4F8;   /* Card hover */
  --bg-surface:       #E8F4F8;   /* Nested surfaces, inputs context */

  /* Text — light */
  --text-primary:     #0F172A;   /* Headlines */
  --text-secondary:   #475569;   /* Body */
  --text-muted:       #94A3B8;   /* Meta */

  /* Borders — light */
  --border:           rgba(0, 0, 0, 0.08);
  --border-light:     rgba(0, 0, 0, 0.04);

  /* Status */
  --green:            #16a34a;
  --green-dim:        rgba(22,163,74,0.1);
  --green-border:     rgba(22,163,74,0.25);
  --blue:             #2563eb;
  --blue-dim:         rgba(37,99,235,0.08);
  --destructive:      #EF4444;
}
```

### Brand Tokens — Dark (Optional / Legacy)

```css
/* Use for dark UI variants only */
:root[data-theme="dark"] {
  --bg-primary:       #00121D;
  --bg-card:          #071E2C;
  --bg-card-hover:    #0A2537;
  --bg-surface:       #0D2B3E;
  --text-primary:     #FFFFFF;
  --text-secondary:   #8BA4B4;
  --text-muted:       #4A6478;
  --border:           rgba(255,255,255,0.07);
  --border-light:     rgba(255,255,255,0.04);
}
```

### Background Usage Rules (Light)

| Layer | Color | Use |
|-------|-------|-----|
| Page base | `#FFFFFF` | Body, default section fill |
| Card | `#F0FAFD` | Cards, stats bar, tab panels |
| Elevated hover / surface | `#E8F4F8` | Hover, nested bands |
| Divider | `rgba(0,0,0,0.08)` | Section breaks, tables |

**Rules:**
- White is the default canvas; orange is **never** a full-page fill.
- Section separation: borders, spacing, or a **slightly** tinted band (`#F0FAFD`), not heavy gray blocks.
- One primary orange CTA per viewport where possible.
- Hero: optional **radial orange glow** behind H1 only (see §2 Gradient).

### Gradient Usage

```css
/* Radial glow behind hero headline — light mode: slightly stronger read on white */
.hero-left::before {
  content: '';
  position: absolute;
  z-index: -1;
  inset: -20% -5% 0 -5%;
  background: radial-gradient(
    ellipse 65% 55% at 45% 25%,
    rgba(224,109,0,0.14) 0%,
    transparent 65%
  );
  pointer-events: none;
}

/* Orange CTA button — only usage of orange gradient */
.btn-primary {
  background: linear-gradient(135deg, #E06D00 0%, #F07A00 100%);
}

/* Card inner top-edge shimmer — optional, very subtle */
.card-shimmer {
  border-top: 1px solid rgba(224,109,0,0.15);
}
```

**Gradient rules:**
- Maximum one radial background glow per page section
- No multi-color gradients (no blue-to-purple, no rainbow)
- On **light** backgrounds, hero glow opacity may be ~12–18% in the center; fade to transparent by ~65%.
- On dark backgrounds, keep glow at 5–10% opacity
- Orange gradient only appears on the primary CTA button

---

## 3. Typography System

### Font Stack

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400..800;1,400..800&family=Inter:ital,opsz,wght@0,14..32,400..700;1,14..32,400..700&family=JetBrains+Mono:ital,wght@0,400..600;1,400..600&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-data: 'JetBrains Mono', ui-monospace, monospace;
}

body { font-family: var(--font-body); }
h1, h2, h3, h4 { font-family: var(--font-display); }
h5, h6 { font-family: var(--font-body); }

/* Metrics, money, tables, phone mockup amounts */
.stat-num, .ap-stat-val, .ri-amt, .fc-val, .tr-amt, .ab-amount, .abr-val, .ph-count, table td .mono {
  font-family: var(--font-data);
}
```

**Icons:** Use [Lucide](https://lucide.dev) SVGs (stroke `currentColor`), centered in **40×40px** wells: `background: var(--orange-dim); border: 1px solid var(--orange-border); border-radius: 8px; color: var(--orange);`

### Type Scale

```css
h1 {
  font-size: clamp(40px, 5vw, 56px);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

h2 {
  font-size: clamp(28px, 3.5vw, 40px);
  font-weight: 600;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

h3 {
  font-size: clamp(20px, 2vw, 24px);
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.01em;
  color: var(--text-primary);
}

h4 {
  font-size: 17px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--text-primary);
}

p {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
  max-width: 60ch; /* Never allow body copy to run full width */
  margin-bottom: 1.5em;
}
p:last-child { margin-bottom: 0; }

.section-label {
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--orange);
  display: block;
  margin-bottom: 24px;
}

.text-mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: var(--text-secondary);
}
```

### Hierarchy Rules for Landing Pages

1. **One H1 per page** — hero only. It is the loudest thing on the page.
2. **Section headlines are H2** — never H1, never styled to look like H1.
3. **Section labels** (e.g., "HOW IT WORKS") always appear above the H2 in orange uppercase.
4. **Body copy max-width: 60ch** — never full-width paragraphs.
5. **Muted slate** for descriptions; **navy/slate** for headlines on light backgrounds.
6. **Monospace (`JetBrains Mono`)** for any numbers, metrics, or transaction data — signals precision.

---

## 4. Layout System

### Grid and Spacing

```css
:root {
  --max-w:  1200px;
  --pad-x:  24px;        /* Mobile horizontal padding */

  /* Spacing scale (8pt grid) */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  24px;
  --space-6:  32px;
  --space-7:  48px;
  --space-8:  64px;
  --space-9:  80px;
  --space-10: 120px;
}

/* Container */
.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--pad-x);
}

/* Section default — marketing landing */
section {
  padding: 120px var(--pad-x);
  max-width: var(--max-w);
  margin: 0 auto;
}
@media (max-width: 768px) {
  section { padding: 72px var(--pad-x); }
}
```

### Responsive Breakpoints

| Name | Width | Notes |
|------|-------|-------|
| Mobile | 375px | Single column, 16px padding |
| Tablet | 768px | 2-column grids unlock |
| Desktop | 1024px | Full layout, 3-col grids |
| Wide | 1440px | Max-width container centered |

```css
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### Column Layouts

```css
/* Feature grid — 3 col desktop, 2 tablet, 1 mobile */
.grid-features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}
@media (max-width: 1024px) { .grid-features { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px)  { .grid-features { grid-template-columns: 1fr; } }

/* Two-col split — text left, visual right */
.grid-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: center;
}
@media (max-width: 768px) { .grid-split { grid-template-columns: 1fr; } }

/* Bento-style asymmetric */
.grid-bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: 16px;
}
/* .span-2 { grid-column: span 2; } .span-row-2 { grid-row: span 2; } */
```

---

## 5. Components

### Navbar

```css
nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 900;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(0,0,0,0.06);
}

.nav-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--pad-x);
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-links a {
  font-size: 14px;
  font-weight: 400;
  color: var(--text-secondary);
  padding: 6px 12px;
  border-radius: 4px;
  transition: all 0.2s ease;
}
.nav-links a:hover {
  color: var(--text-primary);
  background: rgba(0,0,0,0.04);
}
```

**Rules:**
- Logo left, nav links center, CTA right
- On scroll: add `box-shadow: 0 1px 0 rgba(0,0,0,0.06)`
- Mobile: collapse to hamburger at 768px
- Never show more than 5 nav links

---

### Hero Section

Structure: Section label → H1 → subheading (max 52ch) → CTA row → product visual

```css
.hero {
  padding: calc(120px + 60px) var(--pad-x) 120px; /* section pad + nav offset */
  text-align: center;
  position: relative;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 50%;
  transform: translateX(-50%);
  width: 800px; height: 400px;
  background: radial-gradient(ellipse, rgba(224,109,0,0.07) 0%, transparent 70%);
  pointer-events: none;
}

.hero h1 {
  max-width: 16ch;
  margin: 0 auto 20px;
}

.hero p {
  max-width: 52ch;
  margin: 0 auto 36px;
  font-size: 18px;
}

.hero-cta-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}
```

**Rules:**
- H1 must be 6 words or fewer — ruthlessly short
- Subheading is the one sentence that earns the CTA click
- Hero CTA: one primary (orange), one secondary (ghost/outline)
- Social proof below CTA: "X companies" or logo strip — never testimonial quotes in hero

---

### Feature Grid Cards

```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  transition: background 0.2s ease, border-color 0.2s ease;
}
.card:hover {
  background: var(--bg-card-hover);
  border-color: rgba(0,0,0,0.1);
}

.card-icon {
  width: 40px; height: 40px;
  background: var(--orange-dim);
  border: 1px solid var(--orange-border);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 16px;
}
.card-icon svg {
  width: 20px; height: 20px;
  color: var(--orange);
}
```

**Rules:**
- Icon: always orange SVG (Lucide or Heroicons), never emoji
- Description: 2 sentences max in `--text-secondary`
- Optional: 2-3 bullet points with checkmark or dash prefix
- Cards never have a primary CTA inside them

---

### Buttons

```css
.btn {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 11px 20px; border-radius: 4px;
  font-size: 15px; font-weight: 500; cursor: pointer;
  border: none; text-decoration: none;
  transition: all 0.2s ease; white-space: nowrap;
}

/* Primary — one per section max */
.btn-primary { background: var(--orange); color: #fff; }
.btn-primary:hover { background: var(--orange-hover); transform: translateY(-1px); }

/* Outline — secondary actions */
.btn-outline { background: transparent; color: var(--orange); border: 1.5px solid var(--orange); }
.btn-outline:hover { background: var(--orange-dim); transform: translateY(-1px); }

/* Ghost — tertiary, nav, low-emphasis */
.btn-ghost { background: transparent; color: var(--text-secondary); border: 1.5px solid var(--border); }
.btn-ghost:hover { border-color: rgba(0,0,0,0.12); color: var(--text-primary); }

/* Sizes */
.btn-sm  { padding: 8px 16px;  font-size: 14px; }
.btn-lg  { padding: 14px 28px; font-size: 16px; font-weight: 600; }
```

**Rules:**
- `btn-primary` is orange — reserved for the most important action per section
- Never two `btn-primary` side by side — pair with `btn-outline` or `btn-ghost`
- Border-radius stays at 4px (sharp, fintech) — no pill buttons
- `translateY(-1px)` on hover — never scale transforms

---

### Tags and Labels

```css
.tag {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 500;
  letter-spacing: 0.06em; text-transform: uppercase;
  padding: 4px 10px; border-radius: 999px;
}
.tag-orange { background: var(--orange-dim); color: var(--orange); border: 1px solid var(--orange-border); }
.tag-green  { background: rgba(22,163,74,0.1); color: #16a34a; border: 1px solid rgba(22,163,74,0.22); }
.tag-blue   { background: rgba(59,130,246,0.1); color: #60a5fa; border: 1px solid rgba(59,130,246,0.2); }

.live-dot {
  width: 6px; height: 6px;
  background: #16a34a; border-radius: 50%;
  animation: livePulse 2s infinite;
}
@keyframes livePulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(22,163,74,0.35); }
  50%       { box-shadow: 0 0 0 5px rgba(22,163,74,0); }
}
```

**Usage:**
- `tag-orange` — product status, section badges, beta labels
- `tag-green` — "Live Now", "Active", "Available Now"
- `tag-blue` — informational labels
- Tags always appear above H2/H3 headlines, never inline in body copy

---

### How It Works — Step Cards

```css
.step-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  position: relative;
}

.step-grid::before {
  content: '';
  position: absolute;
  top: 24px;
  left: calc(16.67% + 24px);
  right: calc(16.67% + 24px);
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border), transparent);
}

.step-number {
  width: 48px; height: 48px;
  background: var(--orange-dim);
  border: 1px solid var(--orange-border);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 600;
  color: var(--orange);
  margin-bottom: 16px;
}
```

**Phase structure:** Use a labeled phase divider between "Available Now" and "Full Launch"
steps. The phase label text ("Available Now", "Full Launch") is removed from the inline
step content per copy notes — it moves to a standalone divider element above each group.

---

### Dashboard / Product Preview

```css
.dashboard-preview {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 24px 64px rgba(0,0,0,0.4);
}

.preview-chrome {
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border);
  padding: 10px 16px;
  display: flex; align-items: center; gap: 6px;
}
.chrome-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: var(--border);
}
```

**Rules:**
- Always include fake browser chrome header above screenshots
- Use `box-shadow: 0 24px 64px rgba(0,0,0,0.4)` for depth
- Crop to the most compelling UI region — never full-page screenshots
- Annotate with orange callout labels pointing to key features

---

### CTA Section and Forms

```css
.cta-section {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  text-align: center;
  padding: 120px var(--pad-x);
}
@media (max-width: 768px) {
  .cta-section { padding: 72px var(--pad-x); }
}

/* Optional dot grid background for CTA band */
.cta-section.with-grid {
  background-image: radial-gradient(var(--border) 1px, transparent 1px);
  background-size: 24px 24px;
}
```

**Forms section (#cta):** Three-column layout — App Users, POS Vendors, Investors.
Preserve this structure. Each column is a `form-card` component with its own heading,
description, and form or download action.

**Copy updates for CTA section:**
- "App Customers" label changes to "App Users"
- Remove "Free forever." line from App Users card (covered in the Consumers section above)
- POS Vendors: "No commitment, just a conversation." — no other changes

---

### Footer

```css
footer {
  border-top: 1px solid var(--border);
  padding: 32px var(--pad-x);
}

.footer-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}

.footer-links a {
  font-size: 14px;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s ease;
}
.footer-links a:hover { color: var(--text-secondary); }

.footer-legal {
  font-size: 12px;
  color: var(--text-muted);
}
```

**Rules:**
- Footer is minimal: logo, links, legal — never a repeat of full nav
- No CTA in footer (the `#cta` section above handles all conversions)

---

## 6. Visual Elements

### Gradient Summary

| Type | Usage | Opacity |
|------|-------|---------|
| Hero radial glow | Behind H1, orange, top-center | 5-8% |
| CTA button | Linear, orange to orange-hover | 100% |
| Card border shimmer | Top edge of key feature cards | 15% |
| Connector line | Between step cards | border color |

Never use: blue-purple gradients, rainbow, multi-stop color gradients, animated gradients.

### Background Textures

- Dot grid: `radial-gradient(var(--border) 1px, transparent 1px)` at `24px 24px`
- Use only in CTA band or infrastructure section — not on every section
- No geometric line art, no blob shapes, no wave SVG dividers
- Section dividers are `1px solid var(--border)` only

### Icons

- **Library:** Lucide Icons or Heroicons — stroke style, not filled
- **Size:** 20px in cards, 24px in feature heroes, 16px in buttons
- **Color:** `var(--orange)` for feature icons; `var(--text-secondary)` for UI chrome icons
- **Never:** emoji, multi-color icons, raster PNG
- **Container:** `40x40px`, `border-radius: 8px`, `background: var(--orange-dim)`, `border: 1px solid var(--orange-border)`

### Data and Metrics

- Stat numbers: JetBrains Mono, large size, white color, orange suffix/prefix
- Charts: dark card background, orange accent lines/bars, mono labels
- Receipt mockups: white card on dark background, realistic proportions, subtle shadow

---

## 7. Interaction Design

### Standard Transitions

```css
:root {
  --transition: 0.2s ease;
}
```

### Hover States

| Element | Hover Behavior |
|---------|---------------|
| Button primary | `background: var(--orange-hover)` + `translateY(-1px)` |
| Button outline | `background: var(--orange-dim)` + `translateY(-1px)` |
| Button ghost | `border-color: rgba(255,255,255,0.2)` + `color: white` |
| Card | `background: var(--bg-card-hover)` + `border-color: rgba(255,255,255,0.1)` |
| Nav link | `background: rgba(255,255,255,0.04)` + `color: white` |
| Footer link | `color: var(--text-secondary)` |

### Scroll Reveal

```css
.reveal {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
.reveal-d1 { transition-delay: 0.08s; }
.reveal-d2 { transition-delay: 0.16s; }
.reveal-d3 { transition-delay: 0.24s; }
.reveal-d4 { transition-delay: 0.32s; }
```

```js
// IntersectionObserver setup
const revObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); revObs.unobserve(e.target); }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.reveal').forEach(el => revObs.observe(el));
```

**Rules:**
- Stagger grid children with `reveal-d1` through `reveal-d4`
- Never stagger more than 4 elements — animate the container beyond that
- Wrap all animations in `@media (prefers-reduced-motion: no-preference) { }`

### Micro-interactions

- **Stat counters:** Count up from 0 on viewport entry (`threshold: 0.5`)
- **Live dot:** `livePulse` at 2s — keep as-is
- **Form submit:** Disable fields + show confirmation text in button — no toast or modal
- **Nav on scroll:** `box-shadow: 0 1px 0 rgba(255,255,255,0.05)` past 20px scroll

### What Not to Animate

- Infinite decorative animations (bouncing icons, floating shapes)
- Scale transforms on cards (use background shift — no layout jank)
- Hover-only states for mobile-critical interactions
- Page transitions

---

## 8. Design Tone — Anti-Generic Rules

### Hierarchy Rules

1. **Asymmetry in feature grids** — use one "anchor card" per grid that spans 2 columns
   or carries richer content. Never all-equal-height card rows.
2. **Section labels before everything** — every section starts with an orange uppercase label.
   This creates rhythm and scannability.
3. **Headlines do the work** — if the H2 doesn't sell the section, rewrite the H2, not the
   paragraph below it.
4. **Numbers are visual anchors** — stat figures in JetBrains Mono should be oversized and
   placed to break up text-heavy sections.

### Spacing Philosophy

- Section vertical rhythm: 80-120px desktop, 48-64px mobile
- Card internal padding: 24px — not 40px. Tight inside, generous between.
- Whitespace signals confidence. Compressed layouts signal desperation.

### Dark Background Discipline

- The page never reads as "dark mode aesthetic" — it reads as infrastructure.
  Avoid glows, neon, or anything that registers as gaming or crypto.
- Text contrast hierarchy: white (headlines) → `#8BA4B4` (body) → `#4A6478` (muted).
  Three levels only. Never introduce a fourth gray.
- Orange appears at most 3-4 times per viewport: section label + icon + button.
  If it appears more, something is wrong.

### Copy-Design Alignment

- Section labels match purpose exactly — "HOW IT WORKS" not "THE JOURNEY"
- CTA copy is an action: "Download on App Store" not "App Store"
- Prevent orphan words in headlines — adjust `max-width` or rewrite

---

## 9. Skill Search Commands

Run from project root. Requires Python 3.

```bash
# Full design system
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech SaaS dark minimal receipt automation" --design-system -p "PapeX"

# Style options
python3 .shared/ui-ux-pro-max/scripts/search.py "dark navy fintech trust" --domain style -n 3

# Landing page pattern
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech hero trust social proof CTA" --domain landing -n 3

# UX / interaction guidelines
python3 .shared/ui-ux-pro-max/scripts/search.py "hover animation dark mode web" --domain ux -n 3

# Typography
python3 .shared/ui-ux-pro-max/scripts/search.py "editorial modern fintech mono" --domain typography -n 2
```

---

## 10. Pre-Delivery Checklist

### Visual
- [ ] No emoji used as icons — Lucide/Heroicons SVG only
- [ ] Orange appears 3-4 times max per viewport
- [ ] No light/white background sections
- [ ] No pure `#000000` backgrounds
- [ ] Dashboard previews have browser chrome header
- [ ] Cards use `--bg-card` (`#071E2C`), not `--bg-primary`

### Typography
- [ ] One H1 per page, hero only
- [ ] Orange uppercase section label above every H2
- [ ] Body copy max-width: 60ch
- [ ] Metric numbers in JetBrains Mono
- [ ] No centered body copy wider than 60ch

### Interaction
- [ ] `cursor: pointer` on all clickable elements
- [ ] Hover states on all interactive elements
- [ ] `transition: all 0.2s ease` on all interactive elements
- [ ] Scroll reveal on all below-fold sections
- [ ] Animations wrapped in `prefers-reduced-motion` media query

### Contrast (WCAG AA)
- [ ] White on `#00121D`: passes (17:1)
- [ ] `#8BA4B4` on `#00121D`: passes (5.2:1)
- [ ] `#E06D00` on `#00121D`: use at large size only (3.1:1 — large text threshold)
- [ ] `#4A6478` on `#00121D`: muted only — never for body copy

### Responsive
- [ ] Tested at 375px / 768px / 1024px / 1440px
- [ ] Grids collapse correctly (3→2→1 columns)
- [ ] Nav collapses at 768px
- [ ] No horizontal scroll at any breakpoint
- [ ] CTA row wraps on mobile (`flex-wrap: wrap`)
