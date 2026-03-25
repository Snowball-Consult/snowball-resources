# Snowball Consult Design Language

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Foundational design language governing all Snowball Consult visual output - color system, typography, spacing, layout principles, and brand application rules across all mediums |
| **Trigger** | Creating any visual output (HTML pages, diagrams, slides, client deliverables, branded artifacts, website pages); reviewing design consistency; onboarding a designer or developer |
| **Scope** | Brand identity principles, color system (dark and light modes with warm undertones), typography (font selection, scale, rules), spacing system, layout principles, texture philosophy, logo usage, deliverable header/footer patterns, do's and don'ts, CSS custom properties reference |
| **Not In Scope** | HTML diagram animations and SVG connections (see HTML Diagrams standard), Google Slides API specifics (see Google Slides standard), Google Sheets formatting specifics (see Google Sheets Formatting standard), content strategy, copywriting voice (see LinkedIn Voice & Style Guide) |
| **Dependencies** | Service Offering profile - brand positioning context (not included), LinkedIn Profile standard - verbal identity (not included) |
| **Keywords** | design language, brand, visual identity, color palette, typography, Inter, JetBrains Mono, dark mode, light mode, warm, Apple Warm, spacing, layout, CSS custom properties, design system, blue, orange, Apple, premium, deliverables, branded |
| **Maturity** | Working |
| **Last Reviewed** | 2026-03-12 |

---

## Brand Identity Overview

Snowball Consult is a solo GTM data infrastructure consultancy serving Series A-C revenue teams. The design language exists to make every visual touchpoint - client deliverables, website, diagrams, presentations, branded artifacts - look like it came from a 20-30 person RevOps consultancy. Not by pretending to be bigger, but by presenting work at a level of visual care and consistency that most solo practitioners don't invest in.

The brand should feel designed, not decorated. Every choice should look intentional.

---

## Design Principles

1. **Apple-influenced, technical second.** Clean surfaces, generous whitespace, precision in every detail. Technical credibility comes through in the content and the monospace accents - not through busy interfaces.

2. **Quietly premium.** Understated elegance. The design should feel expensive but not loud. Let the work speak. No flash, no gratuitous effects.

3. **Restraint as sophistication.** Blue and orange are vibrant complementary colors. They feel sophisticated because everything around them is calm. The ratio is ~80% neutral surface, ~15% blue accents, ~5% orange accents. The restraint makes the colors pop.

4. **Designed, not decorated.** Every element earns its place. No ornamental gradients, no decorative icons, no patterns that don't serve information. If removing something doesn't hurt comprehension, remove it.

5. **Warm surfaces, not cold compositions.** Warm undertones across the entire palette - warm darks, warm grays, warm whites. This makes technical content feel approachable and distinguishes Snowball from cold developer-tool aesthetics. Whitespace is the primary compositional tool. Depth comes from hierarchy and color, not from shadows and effects.

---

## Color System

### Brand Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| **Snowball Blue** | `#0019FF` | 0, 25, 255 | Primary brand color - links, section accents, highlights, document codes |
| **Snowball Orange** | `#FF9000` | 255, 144, 0 | Accent color - CTAs, trigger elements, progress indicators, connection lines |

These are complementary colors chosen deliberately. They are distinctive and not overused in the B2B SaaS/consulting space. Keep them vibrant - the sophistication comes from how sparingly they're applied, not from muting them.

The entire palette carries warm undertones - warm darks, warm grays, warm whites. This gives Snowball a human, approachable quality that distinguishes it from cold developer-tool aesthetics.

### Dark Mode Palette

Use for: internal materials, marketing content, diagrams, content pieces, dark-themed web pages.

**Surfaces:**

| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#111110` | Page background - warm dark, visibly lifted from black |
| `--surface` | `#1a1918` | Primary container backgrounds |
| `--surface-raised` | `#232220` | Elevated elements (cards, panels) |

**Borders:**

| Token | Value | Role |
|-------|-------|------|
| `--border` | `#2e2d28` | Default - warm, visible |
| `--border-emphasis` | `#3b3a34` | Active/highlighted state |

**Text:**

| Token | Value | Role |
|-------|-------|------|
| `--text-primary` | `#f0ede6` | Primary - warm cream-white, high contrast |
| `--text-secondary` | `#a09b90` | Secondary - warm stone gray, comfortable reading |
| `--text-tertiary` | `#6b675e` | Tertiary - labels, decorative, timestamps |

**Brand color variants (dark mode):**

| Token | Value | Role |
|-------|-------|------|
| `--brand-blue` | `#0019FF` | Full blue |
| `--brand-blue-dim` | `#0014cc` | Darker variant for strokes |
| `--brand-blue-muted` | `rgba(0, 25, 255, 0.25)` | Transparent for glows/shadows |
| `--brand-orange` | `#FF9000` | Full orange |
| `--brand-orange-dim` | `#cc7300` | Darker variant for strokes |
| `--brand-orange-muted` | `rgba(255, 144, 0, 0.12)` | Transparent for ambient effects |

### Light Mode Palette

Use for: client deliverables (ICP PDFs, briefing pages, stakeholder documents), printable artifacts, light-themed web pages.

**Surfaces:**

| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#faf9f6` | Page background - warm off-white |
| `--surface` | `#ffffff` | Primary container (cards, panels) |
| `--surface-raised` | `#f6f5f1` | Elevated/accent areas - warm |

**Borders:**

| Token | Value | Role |
|-------|-------|------|
| `--border` | `#e5e2dc` | Default - warm gray |
| `--border-emphasis` | `#d4d0c8` | Active/highlighted |

**Text:**

| Token | Value | Role |
|-------|-------|------|
| `--text-primary` | `#1c1b17` | Warm near-black |
| `--text-secondary` | `#6b6862` | Warm gray |
| `--text-tertiary` | `#a09b92` | Warm light gray |

**Brand color variants (light mode):**

| Token | Value | Role |
|-------|-------|------|
| `--brand-blue` | `#0019FF` | Full blue - links, accents, highlights |
| `--brand-blue-light` | `rgba(0, 25, 255, 0.06)` | Tinted backgrounds |
| `--brand-orange` | `#FF9000` | Full orange - badges, CTAs |
| `--brand-orange-light` | `rgba(255, 144, 0, 0.08)` | Tinted backgrounds |

### Semantic Colors

These are functional, not brand colors. Do not substitute Snowball Orange for warning amber.

| Role | Light Mode | Dark Mode |
|------|-----------|-----------|
| Success | `#059669` | `#34d399` |
| Warning | `#d97706` | `#fbbf24` |
| Error | `#dc2626` | `#f87171` |

### Color Application Rules

- **Blue for structure:** links, section markers, agenda numbers, document codes, navigation accents
- **Orange for energy:** CTAs, trigger/action elements, progress indicators, connection lines, interactive highlights
- **Ratio:** ~80% neutral surfaces, ~15% blue accents, ~5% orange accents
- **Never** place both brand colors at full saturation directly adjacent
- **Header gradients:** use very dark derivatives of blue (e.g., `#000b33` to `#001452`) - the only place gradients are acceptable
- **Always** define colors as CSS custom properties - never inline hex values

---

## Typography

### Font Stack

| Role | Font | Fallback | Usage |
|------|------|----------|-------|
| Sans-serif (primary) | Inter | `-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif` | All body text, titles, labels, UI elements |
| Monospace | JetBrains Mono | `'SF Mono', 'Fira Code', monospace` | Code, document codes, technical labels, terminal elements |

Load via Google Fonts:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

**Why Inter:** Free (Google Fonts, also bundled in many systems), 9 native weights including semibold and condensed, variable font option, designed for screens, excellent readability. Used by Linear, Vercel, GitHub. Professional and neutral - it doesn't draw attention to itself.

**When Inter is unavailable** (Google Slides, Google Sheets, system-constrained contexts): fall back to the system font stack. The system stack is acceptable - Inter is preferred, not required.

### Type Scale

| Token | Size | Weight | Usage |
|-------|------|--------|-------|
| `--text-display` | 36-44px | 700 | Page titles, hero text |
| `--text-heading-1` | 24-28px | 700 | Section headings |
| `--text-heading-2` | 18-20px | 600 | Subsection headings |
| `--text-heading-3` | 15-16px | 600 | Card titles, group labels |
| `--text-body` | 14-15px | 400 | Body text |
| `--text-small` | 12-13px | 400-500 | Captions, metadata |
| `--text-micro` | 11px | 500 | Document codes, badges |

Ranges allow contextual sizing - use the lower end for dense layouts, higher end for spacious ones.

### Typography Rules

- **Section labels:** uppercase, letter-spacing 0.12-0.22em, `--text-small` size, secondary or tertiary text color
- **Document codes:** monospace, Snowball Blue, reduced opacity (0.7 in dark mode, full in light mode)
- **Headings:** tight letter-spacing (-0.01 to -0.025em)
- **Body text:** line-height 1.5-1.65
- **Compact contexts** (cards, lists): line-height 1.3-1.4
- **Minimum size:** 12px. Never go below this.
- **Maximum two weights per surface.** Pick a body weight and a heading weight. Don't mix three or four weights on one card or section.

---

## Spacing System

Base unit: 4px. All spacing should be a multiple of 4.

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 4px | Tight gaps, inline spacing |
| `--space-sm` | 8px | Related element gaps |
| `--space-md` | 16px | Standard padding, card internal spacing |
| `--space-lg` | 24px | Section padding |
| `--space-xl` | 32px | Major section gaps |
| `--space-2xl` | 48px | Page-level spacing |
| `--space-3xl` | 64px | Hero/display spacing |

---

## Layout Principles

- **Max content width:** 900px for documents/text-heavy pages, 1060px for diagrams and wide layouts
- **Centered in viewport** with flex or auto margins
- **Card border-radius:** 10-12px
- **Button border-radius:** 8-10px
- **Pill border-radius:** 20px
- **Badge border-radius:** 6px
- **Container padding:** 16-32px horizontal minimum
- **Button padding:** 12px 28px minimum for primary/secondary buttons
- **Card borders:** 1px solid `--border`. No drop shadows in dark mode. Subtle warm shadow in light mode: `box-shadow: 0 1px 3px rgba(28, 27, 23, 0.06)`
- **Secondary buttons (dark mode):** subtle surface fill + visible border, not transparent with thin outline
- **Whitespace is generous.** When in doubt, add more space, not less.

---

## Texture and Effects

The brand texture is clean and flat. This applies globally.

- **No gradients on surfaces** (exception: dark header bars use very dark blue derivatives for subtle depth)
- **No grid overlays** on general surfaces (grid is diagram-specific, see HTML Diagrams standard)
- **No glow effects** on general surfaces (glow is diagram-specific, see HTML Diagrams standard)
- **No drop shadows** in dark mode. Subtle warm shadow in light mode: `box-shadow: 0 1px 3px rgba(28, 27, 23, 0.06)`
- **No decorative patterns, textures, or noise overlays**
- **Whitespace is the primary compositional tool** - use it to create hierarchy, group elements, and direct attention

---

## Logo Usage

**Files:**
- Icon mark file (PNG)
- Wordmark file (PNG)

**Placement:**
- Wordmark for document headers, footers, website navigation
- Icon mark for favicons, small placements, social media avatars

**Sizing:**
- Standard: 28-40px height, width auto
- Minimum: 20px height

**Opacity:**
- On dark backgrounds: 60-90% opacity (subtle, not dominant)
- On light backgrounds: 85-100% opacity

**Clear space:** Equal to the logo height on all sides minimum.

**Never:** stretch, rotate, apply effects, place on busy backgrounds without sufficient contrast.

---

## Deliverable Header/Footer Pattern

### Header (Client-Facing Deliverables)

Dark bar with brand gradient background (`#000b33` to `#001452`). This is the one place gradients are used.

Contents:
- Left: Snowball wordmark + document title
- Right: Version, date, confidentiality note (if applicable)
- Client logo may appear alongside Snowball logo depending on deliverable type

```css
.header {
  background: linear-gradient(135deg, #000b33 0%, #001452 100%);
  color: white;
  padding: 14px 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Footer

Minimal. Not every artifact needs one.

- "Prepared by Snowball Consult" or wordmark only
- Tertiary text color, small size
- Page numbers if multi-page

---

## Do's and Don'ts

### Do

- Use white/warm-white surfaces as the canvas; let color be the punctuation
- Use blue for structural/navigational accents (links, section markers, document codes)
- Use orange sparingly for energy/action (CTAs, trigger elements, progress indicators)
- Maintain generous whitespace - Apple-level breathing room
- Stick to two font weights per surface
- Define all colors as CSS custom properties
- Keep warm undertones consistent - warm darks, warm grays, warm whites
- Test in the actual delivery context (browser, PDF print, screen share)

### Don't

- Don't use both brand colors at full saturation adjacent to each other
- Don't apply glow/grid/animation effects outside diagram contexts (those belong in the HTML Diagrams standard)
- Don't use gradients on card or page surfaces
- Don't go below 12px font size
- Don't use more than 2 font families on one surface (Inter + JetBrains Mono is the maximum)
- Don't substitute brand orange for semantic warning amber
- Don't use approximate brand colors (e.g., `#f0983e` instead of `#FF9000`) - use exact hex values
- Don't add decorative elements (icons, illustrations, patterns) unless they serve information
- Don't use inline hex values - always use CSS custom properties
- Don't use cool blue-gray or purple-gray tones - all neutral grays should be warm
- Don't use `--text-tertiary` for content the user needs to read (deliverable lists, status items, checklist labels). Tertiary is for timestamps, decorative labels, and metadata only. Use `--text-primary` or `--text-secondary` for anything the reader should actually engage with.

---

## CSS Custom Properties Reference

Copy-paste-ready blocks for new HTML artifacts.

### Dark Mode

```css
:root {
  /* Brand */
  --brand-blue: #0019FF;
  --brand-blue-dim: #0014cc;
  --brand-blue-muted: rgba(0, 25, 255, 0.25);
  --brand-orange: #FF9000;
  --brand-orange-dim: #cc7300;
  --brand-orange-muted: rgba(255, 144, 0, 0.12);

  /* Surfaces */
  --bg: #111110;
  --surface: #1a1918;
  --surface-raised: #232220;

  /* Borders */
  --border: #2e2d28;
  --border-emphasis: #3b3a34;

  /* Text */
  --text-primary: #f0ede6;
  --text-secondary: #a09b90;
  --text-tertiary: #6b675e;

  /* Typography */
  --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Semantic */
  --success: #34d399;
  --warning: #fbbf24;
  --error: #f87171;
}
```

### Light Mode

```css
:root {
  /* Brand */
  --brand-blue: #0019FF;
  --brand-blue-light: rgba(0, 25, 255, 0.06);
  --brand-orange: #FF9000;
  --brand-orange-light: rgba(255, 144, 0, 0.08);

  /* Surfaces */
  --bg: #faf9f6;
  --surface: #ffffff;
  --surface-raised: #f6f5f1;

  /* Borders */
  --border: #e5e2dc;
  --border-emphasis: #d4d0c8;

  /* Text */
  --text-primary: #1c1b17;
  --text-secondary: #6b6862;
  --text-tertiary: #a09b92;

  /* Typography */
  --sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* Semantic */
  --success: #059669;
  --warning: #d97706;
  --error: #dc2626;
}
```

---

## Relationship to Medium-Specific Documents

This document is the authority. Medium-specific documents specialize within this foundation - they don't override it.

| Document | Relationship |
|----------|-------------|
| HTML Diagrams standard | Specializes for animated dark-theme diagrams. Adds animation system, SVG connections, canvas sizing, grid/glow effects. Those effects are diagram-specific, not brand-wide. |
| Google Slides standard | Specializes for Slides API constraints. System fonts are acceptable given platform limits. Color roles map to this doc's token system. |
| Google Sheets Formatting standard | Specializes for Sheets formatting. Subdued palette operates within the light mode framework. |
| LinkedIn Profile standard | Verbal identity context. Visual identity for LinkedIn (banner, layout) draws from this design language. |
| Service Offering profile | Brand positioning context. The design language expresses this positioning visually. |
