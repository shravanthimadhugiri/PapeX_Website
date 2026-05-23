# PapeX Design Context Framework

Use this framework before designing any screen, feature, onboarding flow, or webpage for PapeX. The goal is to ensure every design decision ties back to the product vision, user behavior, and business goals — not just aesthetics.

---

## 1. Identify the Message

### Core Product Message

PapeX helps people instantly access, organize, share, and manage receipts digitally from the moment they pay.

The app is not just “receipt storage.” It is about reducing friction after payment:

- No lost receipts
- No paper clutter
- No searching galleries for screenshots
- No manual expense organization
- No messy bill splitting
- No forgetting receipts needed for taxes or returns

### Product Vision

PapeX aims to become the post-purchase financial layer between payment and financial completion.

This includes:

- Digital receipts
- Receipt organization
- Shared family receipts
- Bill splitting
- Returns
- Taxes & expense tracking
- Coupons
- Warranties
- Future integrations with POS systems

### Primary Emotional Goals

Users should feel:

- Organized
- In control
- Relieved
- Efficient
- Trusting
- Less mentally burdened

The product should never feel:

- Complicated
- Corporate
- Cluttered
- Heavy
- Spreadsheet-like
- Stressful

### Design North Star

**“Make post-purchase financial management feel effortless.”**

Every screen should support this.

---

## 2. Identify the User and Their Context

### Primary Users

#### 1. 1099 Contractors & Self-Employed Workers

Examples: freelancers, realtors, gig workers, consultants, small business owners.

**Their problems**

- Need receipts for taxes
- Lose receipts often
- Save receipts in camera roll
- Forget to organize expenses
- Spend hours during tax season sorting receipts

**Their constraints**

- Busy
- Mobile-first
- Often multitasking
- Need speed
- Do not want extra manual work

**What they care about**

- Reliability
- Organization
- Searchability
- Fast access
- Exporting/sharing

#### 2. Families & Shared Households

**Their problems**

- Shared purchases
- Bill splitting confusion
- Keeping track of household expenses
- Sharing receipts manually in chats

**What they care about**

- Simplicity
- Shared visibility
- Easy collaboration
- Transparency

#### 3. Everyday Consumers

**Their problems**

- Lose receipts for returns
- Forget warranties
- Paper clutter
- Cannot find receipts later

**What they care about**

- Convenience
- Speed
- Ease of use

### Secondary Users

#### POS Vendors

Need to understand:

- Why businesses would adopt PapeX
- How it improves customer experience
- How it modernizes checkout

The product must appear: modern, scalable, professional, integration-ready.

#### Investors

Need confidence that:

- This solves a real problem
- The product can scale
- There is retention potential
- There is ecosystem expansion potential

Design should communicate: product maturity, clear thinking, strong systems, long-term vision.

---

## 3. Translate the Message Into UI Principles

### Core UI Direction

#### Simplicity First

Receipts are already mentally boring. The UI should reduce cognitive load as much as possible.

**This means:**

- Minimal layouts
- Strong spacing
- Few competing actions
- Clear hierarchy
- Obvious navigation

#### Speed & Accessibility

The product should feel fast to scan and easy to use one-handed.

**This means:**

- Large touch targets
- Minimal typing
- Bottom-sheet interactions
- Clear CTA placement
- Search-first experiences

#### Calm Financial Design

The UI should feel modern and trustworthy without looking overly corporate.

**Visual direction — inspired by:**

- Brex
- Ramp
- Mercury
- Stripe
- Square
- Affirm

**Characteristics:**

- White/light interfaces
- Soft gradients
- Clean typography
- Mellow accent colors
- Rounded cards
- Minimal shadows
- Spacious layouts

#### Organization & Clarity

The user should always know:

- What receipt they’re looking at
- Where things are stored
- What actions are available

**This means:**

- Strong categorization
- Smart grouping
- Search prominence
- Receipt previews
- Metadata visibility

---

## 4. Product Principles for PapeX

### 1. Reduce User Effort

Users should never feel like they are “doing work.”

**Good:** automatic organization, autofill, smart suggestions.

**Bad:** long forms, too many setup steps, complex categorization.

### 2. Design for Existing Behavior

Users already save receipts in their camera roll. PapeX must be faster, easier, and more useful. The product cannot rely on users changing habits purely out of discipline.

### 3. Every Feature Must Answer

**“Why would someone return to this app?”**

Retention-driving features: shared receipts, family groups, bill splitting, search, tax readiness, expense exports.

### 4. The Product Must Feel Connected

Features should not feel isolated. Everything should connect:

**Payment → Receipt → Organization → Sharing → Taxes → Returns**

---

## 5. What to Include in Every Cursor / Claude Prompt

Before generating UI, always include:

### A. Feature Context

What feature is this?

> Example: “This is the receipt detail screen where users view, edit, share, split, or categorize receipts.”

### B. User Context

Who is using this and why?

> Example: “The user is a self-employed contractor trying to quickly find a receipt for taxes while on mobile.”

### C. Emotional Direction

How should it feel?

> Example: “Calm, modern, organized, trustworthy, and fast.”

### D. UX Priorities

What matters most?

> Example: fast scanning, easy sharing, clear hierarchy, minimal friction.

### E. Design System Direction

Reference visual direction.

> Example: “Use a visual style inspired by Ramp, Mercury, Stripe, and Brex with white backgrounds, soft gradients, rounded cards, subtle shadows, and clean typography.”

### F. Constraints

> Example: mobile-first, accessibility-friendly, minimal onboarding friction, one-handed use, iOS-native feeling, scalable design system.

---

## 6. UX Review Checklist

Before approving any screen, ask:

### Clarity

- Is the main purpose obvious in 3 seconds?
- Is the hierarchy clear?

### Simplicity

- Can anything be removed?
- Is the screen overloaded?

### User Effort

- Does this reduce or increase friction?
- Are we making users think too much?

### Retention

- Why would users come back?
- Is this feature habit-forming?

### Product Vision

- Does this support the larger ecosystem vision?
- Does it feel connected to the rest of PapeX?

---

## 7. PapeX Design Philosophy

PapeX is not designing “receipt storage.”

It is designing:

- Peace of mind after payment
- A cleaner financial workflow
- Shared financial organization
- A digital replacement for paper-based chaos

The goal is to make receipts disappear into the background while making the experience around them seamless, accessible, and useful.

---

## Related specs

| Document | Scope |
|----------|--------|
| `design-context-framework.md` | Product vision, users, principles — **why** we design |
| `design-system-v2.md` | v3 marketing site tokens, layout, components — **how** the website looks |
| `papex-v3.html` / `papex-v3.css` | Current consumer marketing implementation |

**Note:** In-app UI follows calm fintech patterns (Brex, Ramp, dark mode in mockup). The v3 marketing site uses a white Flighty-inspired layout for consumer acquisition; both should still feel organized, effortless, and trustworthy per this framework.
