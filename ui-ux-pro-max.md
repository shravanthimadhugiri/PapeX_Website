---
name: ui-ux-pro-max
description: >
  Comprehensive design intelligence for PapeX's fintech SaaS marketing website.
  Contains 67 UI styles, 161 color palettes, 57 font pairings, 99 UX guidelines,
  and 25 chart types. Searchable database with BM25 + regex hybrid ranking.
  Tuned for Stripe / Ramp / Mercury / Brex / Block aesthetic references.
---

# ui-ux-pro-max — PapeX Design Intelligence Skill

Searchable design database for web UI. Use this skill whenever generating or reviewing
any UI component, page section, or visual decision for PapeX.

---

## Prerequisites

```bash
python3 --version || python --version
```

Install Python if missing:

```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3

# Windows
winget install Python.Python.3.12
```

---

## Search Commands

All commands run from the **project root**. Scripts live in `.shared/ui-ux-pro-max/scripts/`.

### Full Design System (start here)

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<product_type> <keywords>" --design-system -p "PapeX"
```

**Example for PapeX:**
```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech SaaS payments minimal clean trust" --design-system -p "PapeX"
```

Returns: pattern, style, color palette, typography, effects, anti-patterns, pre-delivery checklist.

---

### Domain Searches (drill into one dimension)

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| Product patterns | `product` | `--domain product "fintech B2B SaaS"` |
| UI style | `style` | `--domain style "glassmorphism minimal white"` |
| Color palettes | `color` | `--domain color "fintech clean navy"` |
| Font pairings | `typography` | `--domain typography "modern editorial sans"` |
| Landing structure | `landing` | `--domain landing "hero trust social proof"` |
| Chart types | `chart` | `--domain chart "dashboard analytics KPI"` |
| UX guidelines | `ux` | `--domain ux "animation accessibility hover"` |
| AI prompt keywords | `prompt` | `--domain prompt "minimalism fintech"` |

---

### Stack-Specific Guidelines

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<query>" --stack <stack>
```

PapeX default stack: `nextjs` or `react`

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech dashboard components" --stack nextjs
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `astro`, `vue`, `svelte`, `shadcn`

---

### Persist Design System Across Sessions

```bash
# Create master + page-specific override
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech SaaS minimal" --design-system --persist -p "PapeX" --page "homepage"
```

Creates:
- `design-system/MASTER.md` — Global source of truth
- `design-system/pages/homepage.md` — Page-level overrides

**Retrieval prompt for Cursor:**
```
I am building the [Page Name] page for PapeX.
Read design-system/MASTER.md first.
Check if design-system/pages/[page-name].md exists.
If it does, its rules override the Master.
Now generate the code.
```

---

## PapeX Preset — Recommended Design System

> Pre-searched result for `"fintech SaaS payments minimal clean"`. Re-run search to override.

### Pattern
**Trust & Authority + Conversion**
- Section order: Hero → Social proof (logos/stats) → Product overview → Feature grid → CTA
- Primary CTA: Above fold + after features
- Color strategy: White canvas, navy/slate structure, single brand accent for CTA only
- Conversion: Trust badges, transparent pricing, low-friction demo CTA

### Style
**SaaS High-Tech Boutique** (light mode primary)
- White canvas: `#FAFAFA`
- Cards: `#FFFFFF` with `1px #E2E8F0` border, `box-shadow: 0 4px 24px rgba(0,0,0,0.06)`
- Border radius: `12–16px` on cards, `8px` on inputs, `999px` on pill CTAs
- Hover: `scale(1.01–1.02)` + shadow lift, `150–250ms ease-out`

### Colors

```css
/* PapeX Design Tokens */
--color-background:   #FFFFFF;
--color-surface:      #FAFAFA;
--color-surface-alt:  #F1F5F9;
--color-foreground:   #0F172A;
--color-muted:        #64748B;
--color-border:       #E2E8F0;

--color-primary:      #0052FF;   /* Electric blue — CTAs, links */
--color-primary-dark: #003DBD;   /* Hover state */
--color-primary-end:  #4D7CFF;   /* Gradient end */
--color-accent:       #10B981;   /* Success, positive metrics */
--color-destructive:  #EF4444;   /* Errors */

/* Gradients */
--gradient-cta:       linear-gradient(135deg, #0052FF 0%, #4D7CFF 100%);
--gradient-section:   linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
--gradient-hero:      radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,82,255,0.08) 0%, transparent 70%);
```

### Typography

```css
/* Font Pairing: Calistoga (display) + Inter (body) + JetBrains Mono (data) */
@import url('https://fonts.googleapis.com/css2?family=Calistoga:ital@0;1&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

--font-display: 'Calistoga', serif;    /* Hero headlines, section titles */
--font-body:    'Inter', sans-serif;   /* All body, UI, labels */
--font-mono:    'JetBrains Mono', monospace; /* Metrics, code, numbers */

/* Scale */
--text-hero:   clamp(3rem, 7vw, 6rem);   /* font-weight: 400 (Calistoga is inherently bold) */
--text-h1:     clamp(2rem, 4vw, 3.5rem);
--text-h2:     clamp(1.5rem, 3vw, 2.25rem);
--text-h3:     1.25rem;
--text-body:   1rem;         /* line-height: 1.7 */
--text-small:  0.875rem;
--text-label:  0.75rem;      /* font-weight: 600, letter-spacing: 0.08em, uppercase */
```

### Key Effects

```css
/* Hero radial glow */
.hero-glow {
  background: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,82,255,0.08) 0%, transparent 70%);
}

/* Card */
.card {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  transition: box-shadow 200ms ease, transform 200ms ease;
}
.card:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.10);
  transform: translateY(-2px);
}

/* Primary CTA */
.btn-primary {
  background: linear-gradient(135deg, #0052FF 0%, #4D7CFF 100%);
  color: #FFFFFF;
  border-radius: 999px;
  font-weight: 600;
  padding: 14px 28px;
  transition: opacity 200ms ease, transform 150ms ease;
}
.btn-primary:hover {
  opacity: 0.92;
  transform: translateY(-1px);
}

/* Section separator */
.section-divider {
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
}
```

### Anti-Patterns — Avoid for PapeX

- ❌ Purple/pink gradients (generic AI SaaS)
- ❌ Dark mode as primary (use for accent sections only)
- ❌ Emoji as icons — use Lucide or Heroicons SVG
- ❌ Body text under `1rem` / line-height under `1.6`
- ❌ Centered body copy blocks wider than `65ch`
- ❌ Stock photo hero imagery — use product UI screenshots or abstract geometry
- ❌ Full-bleed gradients behind text without sufficient contrast

---

## Landing Page Workflow for PapeX

### Step 1 — Analyze the section
Identify: page type, section purpose, hierarchy level, content density.

### Step 2 — Generate design system
```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech SaaS minimal trust" --design-system -p "PapeX"
```

### Step 3 — Supplement with targeted searches
```bash
# Style deep-dive
python3 .shared/ui-ux-pro-max/scripts/search.py "clean minimal glassmorphism" --domain style -n 2

# Typography confirmation
python3 .shared/ui-ux-pro-max/scripts/search.py "editorial modern fintech" --domain typography -n 2

# UX validation
python3 .shared/ui-ux-pro-max/scripts/search.py "animation hover accessibility" --domain ux -n 3
```

### Step 4 — Build with stack guidelines
```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "fintech dashboard" --stack nextjs
```

---

## Pre-Delivery Checklist

### Visual Quality
- [ ] No emojis as icons (Lucide / Heroicons SVG only)
- [ ] Consistent icon family and stroke weight
- [ ] Color tokens used — no hardcoded hex values in components
- [ ] Hover states: `150–250ms ease-out` transitions on all interactive elements
- [ ] `cursor-pointer` on all clickable elements

### Typography
- [ ] Hero uses Calistoga display font
- [ ] Body copy: Inter, `1rem`, `line-height: 1.7`
- [ ] Data/metrics: JetBrains Mono
- [ ] No centered body text wider than `65ch`
- [ ] Heading hierarchy is unambiguous (only one H1 per page)

### Color & Contrast
- [ ] Body text contrast ≥ 4.5:1 on all backgrounds
- [ ] CTA button contrast ≥ 4.5:1
- [ ] Muted text (`#64748B` on white) checked — passes 4.6:1
- [ ] No color as the sole indicator of state

### Layout
- [ ] Max content width: `1200–1280px`, centered
- [ ] Section vertical padding: `80–120px` desktop, `48–64px` mobile
- [ ] Grid: 12-col desktop, 4-col mobile
- [ ] Responsive breakpoints tested: 375px / 768px / 1024px / 1440px
- [ ] `prefers-reduced-motion` respected — no forced animations

### Accessibility
- [ ] All images have `alt` text
- [ ] Focus states visible (`:focus-visible` ring)
- [ ] Form fields have associated `<label>` elements
- [ ] Keyboard navigation works for all interactive elements

---

## Quick Reference — Common UI Patterns

### Hero Section
- Radial gradient glow behind headline (subtle, `rgba(0,82,255,0.06–0.10)`)
- Headline: Calistoga, `clamp(3rem, 7vw, 6rem)`, tight `letter-spacing: -0.02em`
- Subheading: Inter 400, `1.125–1.25rem`, `#64748B`, max `52ch`
- CTA: Pill button, gradient, 48–56px height, secondary ghost button alongside
- Social proof: Logo strip or "X companies trust PapeX" in `text-label` style
- Dashboard mockup or product screenshot below fold, subtle drop shadow

### Feature Grid
- 3-col desktop, 2-col tablet, 1-col mobile
- Card-based with icon (24px, `--color-primary`), headline H3, 2-sentence description
- Bento variant: asymmetric spans (`2x1`, `1x2`) for visual interest
- Section background: alternate `#FFFFFF` / `#F8FAFC` for rhythm

### Navbar
- `max-width: 1280px`, `padding: 0 24px`
- Transparent on hero → `background: rgba(255,255,255,0.85)` + `backdrop-filter: blur(12px)` on scroll
- Logo left, nav links center (desktop), CTA right
- Active link: `--color-primary` underline, `2px`, `border-radius: 1px`

### CTA Section
- Full-width, `background: --gradient-cta` or deep navy `#0F172A`
- Large centered headline (Calistoga), white text
- Two buttons: white filled + white ghost
- Optional: subtle background grid or dot pattern at `opacity: 0.08`

### Footer
- `background: #0F172A`, white text
- 4-col grid: Logo/tagline | Product links | Company links | Legal
- Bottom bar: copyright + social icons (Lucide)
- Divider: `1px solid rgba(255,255,255,0.1)`
