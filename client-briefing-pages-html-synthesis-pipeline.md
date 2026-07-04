# Client Briefing Pages

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Procedure for generating polished local HTML "Briefing Pages" from synthesized call transcripts and rollup documents - the final presentation layer for stakeholder update calls |
| **Trigger** | Preparing for a budget holder/CEO check-in, creating a client-facing update page, "create a briefing page", "make the update website" |
| **Scope** | The full pipeline from transcripts to rendered HTML; content selection, visual design standards, the relationship between source artifacts; Slack output format for pre-call rich agenda; two-punch pattern |
| **Not In Scope** | Transcript processing methodology (Call Transformation standard), rollup synthesis (future extension), prep sheet content strategy (Budget Holder Prep Sheet), Fathom ingestion (Transcript Ingestion procedure) |
| **Dependencies** | Transcript Ingestion procedure (not included), Call Transformation standard (not included), Budget Holder Prep Sheet (not included), Decision Tracking standard (not included) |
| **Keywords** | briefing page, HTML, local website, stakeholder update, CEO update, client presentation, synthesis, rollup, project update, browser, visual, call prep, rich agenda, slack, two-punch, pre-call primer |
| **Maturity** | Working |
| **Last Reviewed** | 2026-02-12 |

---

## What is a Briefing Page?

A **Briefing Page** is a polished, self-contained local HTML file designed to be opened in a browser during a stakeholder call. It turns synthesized project work into a visual, scannable document you can follow along with on screen.

Briefing Pages are not shared with the client. They are for the consultant - a prepared, professional reference that makes you look sharp and keeps the conversation on track.

**Why HTML instead of markdown?**
Markdown in a browser looks like raw text. HTML renders with typography, color, spacing, and structure. The visual quality signals preparation and professionalism - even if only you see it.

---

## The Pipeline

Briefing Pages are the final output of a multi-stage pipeline. Each stage has its own source of truth document.

```
Fathom Calls
    |
    v
Transcript Ingestion
    |  Raw transcripts saved to {project}/transcripts/
    v
Call Transformation (Three-Layer)
    |  AI extraction -> AI synthesis -> human narrative
    |  Saved to {project}/calls/
    v
Cross-Call Rollup (manual or future extension)
    |  Synthesize patterns across multiple calls
    |  Saved to {project}/calls/ROLLUP_*.md
    v
Budget Holder Prep Sheet (Markdown)
    |  Content selection, framing, talking points, rich agenda
    |  Saved to {project}/
    v
[This document] Two outputs:
    |--- Rich Agenda (Slack message) -- sent before call
    |--- Briefing Page (HTML) -- used during call
    |  Both saved to / generated from {project}/
```

**Key principle:** Each layer builds on the previous. The Briefing Page does not go back to raw transcripts - it renders the prep sheet into HTML. If the prep sheet is missing content, fix the prep sheet first.

---

## The Two-Punch Pattern

A budget holder call produces two presentation artifacts, not one. Both draw from the prep sheet (Budget Holder Prep Sheet) but serve different purposes at different moments.

| Artifact | When | Channel | What It Does |
|----------|------|---------|-------------|
| Rich Agenda | 2-4 hours before the call | Slack DM | Primes the stakeholder. "Last time we discussed X. This week: Y." |
| Briefing Page | During the call | Browser | Visual deep-dive. Progress tables, pipeline diagrams, cost comparisons. |

**The agenda primes. The briefing page delivers.** The agenda is the movie trailer - enough to build anticipation, not enough to spoil the experience. The briefing page is the movie itself - depth, structure, visual impact.

**Content relationship:** The Rich Agenda is a curated 4-7 item view of the prep sheet. The Briefing Page is a visual rendering of the full prep sheet. They share source material but differ in depth and format. The Budget Holder Prep Sheet defines how to compose the rich agenda content. This document defines how to format it for Slack.

A third delivery channel has been added: **direct HTML via send.co MCP**. The same HTML that renders locally can be pushed to send.co in a single API call, giving the document a shareable URL with access controls (domain-restricted email verification), view tracking, and professional presentation - while the consultant retains full control over design and content through Claude Code.

---

## Slack Output Format Specification

The Rich Agenda is sent as a Slack DM. Slack uses its own markup format (mrkdwn), which differs from standard markdown.

### Slack mrkdwn Rules

| Element | Slack Syntax | Standard Markdown |
|---------|-------------|-------------------|
| Bold | `*bold*` | `**bold**` |
| Italic | `_italic_` | `*italic*` |
| Strikethrough | `~strike~` | `~~strike~~` |
| Bullet list | `- item` | `- item` |
| Line break | Single newline | Double newline |
| Links | `<url\|text>` | `[text](url)` |
| Headings | Not supported - use bold | `# Heading` |
| Tables | Not supported - use bullets | `\| col \|` |

### Rich Agenda Template

```
*[Client] - [Name] Check-in | [Day, Date]*
_Last time:_ [1-2 sentence recap of the previous call. Factual, brief.]

*This week:*
- *[Topic 1]* - [one-liner: why it matters or what changed]
- *[Topic 2]* - [one-liner]
- *[Topic 3]* - [one-liner]
- *[Topic 4]* - [one-liner]
- *[Topic 5]* - [one-liner]

*Looking ahead:* [One sentence about what's coming next]
```

### Formatting Guidance

- **Bold the topic** within each bullet. The explanation after the dash stays unbolded.
- **4-7 items.** Fewer feels thin. More than 7 means you haven't curated enough.
- **One screen on desktop.** If the message requires scrolling, it's too long. Aim for under 15 lines.
- **One sentence per item.** Max two if needed. No paragraphs under bullets.
- **No salutation.** Slack DMs don't need "Hi [name]." Just start.
- **No emojis** unless the team culture uses them. For most executive audiences, keep it clean.
- **Copy-paste ready.** The consultant composes it in the prep artifact's Section 7, then copies into Slack verbatim.

### Anti-Patterns

| Don't | Why | Instead |
|-------|-----|---------|
| Walls of text | Executives scan, they don't read Slack novels | Bullet points, one line each |
| Full paragraphs per item | This is a primer, not a brief | One sentence explains why it matters |
| Numbered sub-items | Adds visual complexity without value | Flat bullet list |
| Revealing the punchline | "We saved 120x on LinkedIn" is a spoiler | "Major cost breakthrough on LinkedIn data - excited to walk through the numbers" |
| Double asterisks for bold | `**text**` renders as literal asterisks in Slack | Use single `*text*` |
| Markdown links | `[text](url)` won't render in Slack | Use `<url\|text>` if linking |

---

## When to Create a Briefing Page

- Before a recurring CEO/budget holder check-in (per the Budget Holder Prep Sheet)
- Before a milestone review or phase transition call
- When presenting synthesized discovery findings
- Any call where you want to follow along with a visual reference

Not every call needs one. Quick syncs and working sessions don't. Use them when the call is more "presenting" than "collaborating."

---

## Content Source Mapping

The Briefing Page pulls content from specific source artifacts. Don't duplicate effort - pull, don't recreate.

| Output | Source Artifact | What to Pull |
|-----------------------|-----------------|--------------|
| Rich Agenda (Slack) | Prep sheet Section 7 (Budget Holder Prep Sheet) | Curated 4-7 items with one-liner framing, last-time recap |
| Opening/framing | Prep sheet (Budget Holder Prep Sheet) | Framing statement, stats |
| Progress table | Prep sheet + Asset Index standard | Deliverable list, statuses |
| Key insights | Rollup documents | Meta-learnings, patterns |
| Decision log | Decision Tracking standard | Decision summaries |
| Artifact readbacks | Client folder root docs (ICP, persona, etc.) | Readback paragraphs, summary tables |
| Sustainability/maintenance | Prep sheet talking points | Maintenance message, recurring items |
| What's next | Prep sheet | Immediate, then, coming |
| Future opportunities | Prep sheet + rollups | Ideas with timeline |

---

## Visual Design Standards

### Principles

1. **Clean, not flashy.** Subdued colors, professional typography, plenty of whitespace.
2. **Scannable.** Headers, cards, badges, and tables - not walls of text.
3. **Follow-along friendly.** Sections map to the call agenda so you can scroll as you talk.
4. **Self-contained.** Single HTML file, no external dependencies. Works offline.

### Layout Structure

```
[Header]         Dark background, consultant logo, title, subtitle, meta (date, duration, call count)
[Agenda Strip]   Horizontal bar with numbered sections - prominent numbers, scannable labels
[Content]        Sections matching the agenda, each with section header
[Footer]         Minimal - source attribution if needed
```

### Typography

- System font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Max content width: 900px, centered
- Body text: 14px, line-height 1.6-1.7
- Section headers: 20px, bold 700
- Agenda strip numbers: 22px, bold 800, accent color - these must be prominent and scannable from a distance
- Agenda strip labels: 14px, bold 600
- Toggle summary headers: 20px, bold 700 - large enough to be the primary visual element when collapsed
- Toggle content: 14px, indented 24px
- Muted text: `#6b7280`

### Color Palette

Keep subdued. Use color for status and emphasis, not decoration. These are the **defaults** - when brand colors are available (see Branding below), override accent and amber with brand primary/secondary.

| Purpose | Color | Default Hex | Notes |
|---------|-------|-------------|-------|
| Background | Light gray | `#fafafa` | |
| Cards | White | `#ffffff` | |
| Text | Near-black | `#1a1a2e` | |
| Muted text | Gray | `#6b7280` | |
| Borders | Light gray | `#e5e7eb` | |
| Accent/links | Blue | `#2563eb` | Override with brand primary |
| Accent light | Light blue bg | `#eff6ff` | Derive from brand primary at 5-10% |
| Success/complete | Green | `#059669` | Semantic - keep regardless of brand |
| Success light | Light green bg | `#ecfdf5` | |
| Warning/building | Amber | `#d97706` | Override with brand secondary |
| Warning light | Light amber bg | `#fffbeb` | Derive from brand secondary at 5-10% |
| Error | Red | `#dc2626` | Semantic - keep regardless of brand |
| Error light | Light red bg | `#fef2f2` | |
| Secondary accent | Purple | `#7c3aed` | |
| Secondary light | Light purple bg | `#f5f3ff` | |

### Component Library

These are the reusable building blocks. Combine as needed.

**Cards** - White background, 1px border, 10px border-radius, 24px padding. Use for any content block.

**Highlight cards** - Card with a 4px left border in accent color and tinted background. Use for key framing statements or important callouts.

**Agenda strip** - Horizontal grid of numbered items showing call flow. Numbers are 22px bold 800 in accent color. Labels are 14px bold 600. Must be scannable from a distance - this is the visual roadmap for the call.

**Stats row** - Grid of 4 boxes showing key numbers (calls completed, hours, decisions, etc.). Use in the opening section.

**Tables** - Standard bordered tables with header row, uppercase small-caps headers. Use for structured data (progress, criteria, signals).

**Insight list** - Icon + title + short description rows. Use for learnings/findings.

**Readback blocks** - Card with a 4px top border (blue for ICP, purple for persona). Contains a tag label and blockquote. Use for artifact summaries.

**Persona grid** - 3-column card grid with colored top borders. Use for persona type comparison.

**Cost comparison** - Two boxes with "vs" between them. Old price struck through in gray, new price in green. Use for agent cost savings.

**Status badges** - Small inline labels. Green for complete, amber for building, blue for drafted.

**Section badges** - Small pill next to section header. Use sparingly for labels like "Artifact" or "What I learned."

### Branding

Always include consultant branding. The logo and brand colors are found in the inbox or project root.

- **Logo:** Place in the header before the title. Wordmark at 36px height. Slightly muted opacity (0.85-0.9) against dark header backgrounds. Embed as base64 data URI for self-contained files.
- **Brand colors:** Override CSS custom properties (`--accent`, `--accent-light`, `--amber`, `--amber-light`) with brand colors. Primary brand color (`#0019FF`) for accent (links, agenda numbers, highlights). Header gradient uses a very dark derivative of the primary. Secondary brand color (`#FF9000`) for amber/warning tones (in-progress badges, big number highlights). Light variants at 5-10% saturation.
- **Header gradient:** Use a very dark derivative of the brand primary color (e.g., `#000b33` to `#001452`), not generic gray.
- **Don't overdo it.** The design should remain subdued and professional. Brand colors enhance, they don't dominate. Green and red remain semantic (success/error) regardless of brand.

### Collapsible Toggles

Use HTML `<details>/<summary>` elements for sections with detail text that should be hidden during presentation. The consultant sees topic headers and clicks to expand when needed.

**When to use:** Strategic callouts, future opportunities, risk items, or any section where you want to control information flow during a call. Keeps the stakeholder focused on the speaker rather than reading ahead.

**Styling:** Style the `<summary>` as a large bold clickable header (20px, bold 700) with a triangle indicator (accent colored). The summary must be large enough to be the primary visual element when collapsed - it's what the stakeholder sees. Style `.toggle-content` as 14px body text, indented 24px. Use subtle bottom borders between multiple toggles. Hide the default `<details>` marker with `::-webkit-details-marker { display: none }` and use custom unicode triangles.

**Principle:** The briefing page is a follow-along tool, not a reading document. Toggles let the consultant reveal information at the right moment in the conversation rather than having it all visible at once.

### Quote Usage

Quotes can be powerful in briefing pages but must be used with care.

**Default: Don't quote stakeholders.** Re-quoting someone's words back to them (or to their colleagues) ruffles feathers and can feel performative. Paraphrase instead - especially in the "Last Time" section.

**Exception: Quotes that validate the engagement.** A quote is appropriate when it demonstrates that the stakeholder sees the value of the work - when it underlines that what's being done together is meaningful. These are "we're aligned and this matters" moments.

**Rules:**
- Every quote must be a verified actual quote from a transcript, not paraphrased or reconstructed
- The quote must be directly pertinent to the section it appears in
- Include attribution (name, role)
- Use sparingly - one or two per briefing page maximum
- Never quote the budget holder back to themselves in the "Last Time" recap

### Responsive

Include basic responsive styles for narrower screens (tables scroll, grids collapse to single column). Not critical since these are for desktop browser viewing, but avoids broken layouts.

---

## Creation Process

### Step 1: Verify Prerequisites

Before creating a Briefing Page, these must exist:

- [ ] Transformed call summaries in `{project}/calls/`
- [ ] At least one rollup document synthesizing patterns
- [ ] A prep sheet (per the Budget Holder Prep Sheet) with content selection done
- [ ] Any artifacts to showcase (ICP, persona, decision log, etc.)

### Step 2: Build the HTML

1. Start from the design standards above - header, agenda strip, sections
2. Pull content from source artifacts (see Content Source Mapping)
3. Keep text concise - shorter than the prep sheet. The prep sheet is your full reference; the Briefing Page is the visual version
4. Apply status badges, stats, and visual components to make data scannable
5. Test in browser - verify it looks clean and scrolls naturally

### Step 3: Save and Open

- Save as `{project}/{call-context}.html` (e.g., `ceo-checkin-feb10.html`)
- Open with `open {filepath}` to launch in default browser
- Keep the prep sheet markdown alongside it as the full-detail reference

---

## Naming Convention

```
{stakeholder-name}-{call-type}-{date-or-period}.html
```

Examples:
- `ceo-checkin-feb10.html`
- `ceo-quarterly-review-q1.html`
- `gtm-lead-discovery-findings.html`

---

## Relationship to Other Artifacts

| Artifact | Role | Format | When |
|----------|------|--------|------|
| Prep sheet (Budget Holder Prep Sheet) | Full content, talking points, private notes | Markdown | Prep (private) |
| Rich Agenda (Budget Holder Prep Sheet Section 7) | Pre-call primer sent to stakeholder | Slack message | Before the call |
| Briefing Page (this doc) | Visual follow-along for the call | HTML | During the call |
| Follow-up summary (Decision Tracking standard) | Post-call client-facing summary | Markdown/email | After the call |

The prep sheet is the **source of truth** for what to say. The Briefing Page is the **visual layer** for how it looks on screen. They are always created as a pair.

---

## Iteration

After the first Briefing Page for a client:
- Reuse the HTML structure - update content, keep the layout
- The visual template stabilizes quickly; only the content changes week to week
- Keep previous Briefing Pages for reference (shows progression over time)

## Changelog

| Date | Change |
|------|--------|
| 2026-03-20 | Added send.co MCP integration as third delivery channel - direct HTML publishing with domain-restricted access controls and view tracking |
| 2026-03-12 | Updated visual design standards to reference centralized design language - CSS custom properties, warm color palette, Inter + JetBrains Mono typography stack |
| 2026-02-28 | Added meeting briefing variant for multi-party technology vendor introductions - distinct from recurring stakeholder updates |
| 2026-02-22 | Refined quote usage rules - default to not quoting stakeholders back to themselves; quotes should validate the engagement, not perform it |
| 2026-02-12 | Added Two-Punch Pattern, Slack rich agenda format specification with mrkdwn syntax rules, and pre-call primer template |
| 2026-02-12 | Added collapsible toggle guidance, branding standards (logo embedding, brand color overrides), and quote usage policy |
| 2026-02-08 | Expanded content source mapping - formalized which output sections pull from which source artifacts to reduce duplication between prep sheet and briefing page |
| 2026-02-05 | Initial version - extracted from first stakeholder check-in preparation |
