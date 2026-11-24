# AI Context Document Standards: Structure, Naming, and Retrieval Optimization

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Complete framework for structuring AI context documents - covers taxonomy, maturity, naming conventions, retrieval optimization, and cross-referencing |
| **Trigger** | Creating new context documents, structuring an AI-friendly knowledge base, setting up Claude Code or Claude Projects, optimizing file discoverability |
| **Scope** | Document architecture, taxonomy, maturity levels, content structure, filename generation, keyword extraction, retrieval optimization, cross-referencing |
| **Not In Scope** | Specific technical content (CRMs, enrichment tools, etc.), prompt engineering for conversations, fine-tuning, platform-specific RAG mechanics |
| **Dependencies** | [Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md) - Foundational filename principles this document builds on (also published in this repo) |
| **Keywords** | markdown, documentation, RAG, retrieval, Claude Code, Claude Projects, knowledge base, taxonomy, document structure, metadata tables, maturity, filename generation, keyword extraction, query anticipation, naming conventions, live source, snapshot, versioned sections |
| **Maturity** | Stable |
| **Last Reviewed** | 2026-11-24 |

---

## Why This Exists

After months of working with Claude Code daily, the single highest-leverage investment has been putting every knowledge artifact into a homogeneous, structured format. The payoff isn't in any individual document - it's in how documents link together as a graph.

When every piece of knowledge wears the same uniform - same metadata table, same naming convention, same maturity framework, same cross-referencing pattern - three things happen:

1. **Retrieval becomes effortless.** The AI never has to guess what a document is about. The filename, metadata table, and front-loaded content make discovery unambiguous.
2. **Documents compose naturally.** Because they all follow the same structure, they cross-reference cleanly. A procedure can point to a framework, which points to a reference doc, and the AI navigates this graph without friction.
3. **The system is resilient.** Even if you started with no structure at all, the uniform format means you can always restructure later. The structure is overly rigid by design - that makes it extremely reusable and machine-parseable while remaining human-readable.

This document captures the full system. It's designed so you can adapt it to your own domain and start using it immediately.

---

## Applicability

This document defines a **general framework** for structuring context documents optimized for AI retrieval and execution. While examples are drawn from GTM and revenue operations, the principles apply universally to any domain:

- **The nine categories are examples** - Adapt or replace them based on your domain's needs (e.g., engineering might use ARCHITECTURE, REFERENCE, RUNBOOK; research might use LITERATURE, HYPOTHESIS, PROTOCOL)
- **The structural patterns are universal** - Metadata tables, front-loading, negative scope, and cross-references work across all knowledge types
- **The naming conventions are adaptable** - The `{CATEGORY}_{name}.md` pattern works for any taxonomy you define

The goal is retrieval optimization and execution clarity, regardless of subject matter.

---

## Core Principle

Every context document must optimize for two sequential phases:

1. **Discovery** - Can the AI find the right document when relevant?
2. **Execution** - Once found, can the AI correctly interpret and apply it?

Most documentation fails at discovery. Clear naming, explicit scope boundaries, and front-loaded metadata solve this.

**The filename is not a label - it's a searchable metadata record.** Every word in a filename is a potential retrieval hook. In RAG-based systems (Claude Projects, vector databases, search indexes), filenames directly influence whether the AI finds your document. A poorly named file with perfect content may never surface.

---

## What a Document Holds: Taste and Learnings, With Vendor Data Pulled Live

A context document holds the layer that sits on top of what vendors publish: your taste, your decisions and the reasons for them, your methods and standards, and what real builds taught you. What a vendor publishes and changes (prices, limits, model lineups, how the product behaves) stays on the vendor's own pages and is pulled live when a task needs it. The same rule applies to `CLAUDE.md` files.

**Why:** a value copied into a document goes stale while the document keeps its maturity label. A Stable or Canonical document outranks general knowledge, so the AI treats its stale values as definitive.

### Never stored in a document

- Prices and costs
- Plan tiers, quotas and limits
- Model lineups, rankings, benchmark scores, context-window sizes
- Vendor statistics and case-study figures
- Restatements of vendor documentation

### Write the live source in place of the value

Name where the current value lives: the vendor page URL, a documentation lookup tool, or the CLI command that reads it. Example: "current model prices: the vendor's pricing page, looked up at the time of use" in place of a price table.

### What belongs in a document

- **Taste and decisions:** which option you prefer and why, in category language ("the cheapest model that passes the test rows")
- **Methods and standards:** how to choose, test, build and review
- **Dated operator learnings:** what a tool did in a named build, with the date, to be re-verified before relying on it
- **Build records:** which model, prompt or setting a specific build was configured and tested with
- **Dated payload snapshots:** the JSON shape a vendor returned on a named date, opening with "Snapshot as of <date>. Current shape: <live source>."
- **Gaps in vendor docs:** which pages disagree, and on what

### Exception: research snapshots

A document whose subject is research about a market or a practice may hold figures. It states a snapshot date and a refresh-by date, and every figure carries its source, data period and definition. After the refresh-by date, figures are quoted only as dated history. Such a document never reaches Canonical.

### The test

For each sentence that states a fact about a third-party product, ask: would this sentence be wrong if the vendor changed its page? If yes, replace it with the live source. If it records what happened in a dated build, keep it with its date.

---

## Document Maturity Framework

Documents progress through five maturity levels that signal reliability to AI systems.

**Source of truth:** The document itself. Each document's metadata table contains its `Maturity` and `Last Reviewed` fields. A manifest (index file) reflects these values for quick lookup but is not authoritative - always trust the document.

### Maturity Levels

| Status | Definition | AI Behavior |
|--------|------------|-------------|
| **Draft** | Early exploration, may be incomplete or wrong | Reference only when directly asked. Preface with "This is still being developed." |
| **Working** | Substantive thinking complete, not yet validated in practice | Use as current best thinking, but don't treat as authoritative. Open to contradiction from other sources. |
| **Stable** | Validated through use, still being refined | Use confidently. Prefer over general knowledge. Flag significant contradictions rather than silently overriding. |
| **Canonical** | Definitive position, locked in | Treat as authoritative. Override general knowledge. Only superseded by explicit revision or newer canonical doc. |
| **Obsolete** | Superseded or no longer relevant | Do not use. Retained for historical reference. If referenced, note it is obsolete and point to any replacement. |

### Promotion Rules

- **Draft to Working:** When the thinking is substantive and coherent (automatic as document develops)
- **Working to Stable:** When validated through real-world use and refined based on feedback
- **Stable to Canonical:** Only by explicit decision ("make this canonical") - indicates locked-in, authoritative status
- **Any to Draft:** When major revision is underway
- **Any to Obsolete:** When a newer document fully supersedes it or it is no longer relevant. Name the replacement in the document.

### Staleness

- Track "Last Reviewed" date for all documents
- AI should note when stable/canonical documents haven't been reviewed in 6+ months
- Even canonical documents may warrant re-evaluation if context has shifted significantly

### New Document Default

New documents start as **Working** unless explicitly marked as Draft (for early explorations) or Stable (for documents created from existing validated material).

---

## Document Taxonomy

All documents fall into one of nine functional categories. Each corresponds to a distinct type of question the AI might need to answer.

**Decision rule:** When a document could fit multiple categories, ask: "What question is someone most likely asking when they need this document?" The answer determines the category.

### REFERENCE - Platform Documentation

**Purpose:** How you work with a tool, platform, or system: where its vendor documents it, plus the recipes, patterns and operator knowledge from your own builds. How the tool itself behaves, what it costs and what its limits are stay in the vendor's docs and are looked up at task time.

**Retrieval triggers:**
- "What's our formula for cleaning a URL?"
- "Where do I check how X handles Y?"
- "How did we format this last time?"

**Structure:**
- Where the vendor documents the tool
- Recipes and patterns from real builds, organized by task
- Traps and anti-patterns seen in real builds, dated
- Known gaps and conflicts in the vendor's docs

---

### SCHEMA - Format Specifications

**Purpose:** Define what structured outputs should look like. Data shapes, JSON formats, field definitions.

**Retrieval triggers:**
- "What fields should this include?"
- "What should the output JSON look like?"
- "What's the schema for company enrichment?"
- "How should I structure this data?"

**Structure:**
- Schema overview (what this format is for)
- Complete field reference (every field, type, valid values)
- Required vs. optional fields
- Example outputs (valid and invalid)
- Validation rules

---

### FRAMEWORK - Conceptual Models

**Purpose:** Explain how to think about a problem domain. Mental models, first principles, strategic foundations.

**Retrieval triggers:**
- "How should I approach lead scoring?"
- "What's the right way to think about deduplication?"
- "Help me understand phone number scoring"
- "What are the fundamentals of X?"

**Structure:**
- Problem framing (why this matters, what problem it solves)
- Core concepts and definitions
- Decision frameworks and heuristics
- Trade-offs and considerations
- Common mistakes

**Decision guidance:** If a document primarily teaches you how to think about something (mental models, principles), it belongs in FRAMEWORK. If it primarily teaches you how to do something (steps, sequences), it belongs in PROCEDURE.

---

### PROCEDURE - Operational Workflows

**Purpose:** Step-by-step execution guides, sequential processes, action-oriented documentation.

**Retrieval triggers:**
- "Walk me through ICP discovery"
- "What are the steps for stakeholder interviews?"
- "How do I create a proposal?"
- "What's the process for validating a data build?"

**Structure:**
- Purpose and when to use this procedure
- Prerequisites and inputs
- Step-by-step instructions
- Decision points and branches
- Expected outputs
- Common issues and troubleshooting

**Decision guidance:** If a document could be followed as a checklist or workflow, it belongs in PROCEDURE. The presence of conceptual framing within the document does not disqualify it - categorize by primary retrieval purpose.

---

### STANDARD - Rules and Constraints

**Purpose:** Style guides, naming conventions, constraints, codified taste. Documents that define how things should be done.

**Retrieval triggers:**
- "Edit this in my LinkedIn voice"
- "What should I name this file?"
- "Is this formatted correctly?"
- "What are the rules for document metadata?"

**Structure:**
- What this standard governs
- The rules (explicit, unambiguous)
- Examples of correct usage
- Examples of incorrect usage (anti-patterns)
- Exceptions and edge cases

**Decision guidance:** If a document exists to enforce consistency, express taste, or establish rules that constrain future work, it belongs in STANDARD. These are normative documents - they say how things should be.

---

### PROFILE - Self-Reference

**Purpose:** Self-referential business documentation. Who you are, what you offer, positioning, engagement models.

**Retrieval triggers:**
- "What do I offer?"
- "What's my engagement model?"
- "Describe my services"
- "What's my positioning?"

**Structure:**
- Overview (who you are, what you do)
- Value proposition and differentiators
- Service/product details
- Engagement models and pricing logic
- Positioning and competitive landscape

---

### PERSONA - Stakeholder Intelligence

**Purpose:** Mental models for specific buyer/stakeholder types. Role-specific primers and buyer intelligence.

**Retrieval triggers:**
- "What does a CRO care about?"
- "How does a VP Sales think about this?"
- "What language resonates with RevOps leaders?"

**Structure:**
- Role overview (responsibilities, reporting structure)
- Primary concerns and priorities
- How they measure success (KPIs they care about)
- Language patterns (terminology they use)
- Pain points and frustrations
- Messaging that resonates vs. falls flat

---

### CHEATSHEET - Tip Collections

**Purpose:** Collections of discrete, actionable tips, shortcuts, and commands for tools and workflows. Unlike REFERENCE documents (which are authored as a whole and organized by task), CHEATSHEET documents grow incrementally through a capture process - tips are added one at a time and normalized into a uniform format.

**Retrieval triggers:**
- "What are the shortcuts for X?"
- "Give me the Claude Code tips"
- "How do I do Y in Z?"
- "What's the command for X?"
- "Add this tip"

**Structure:**
- Organized by tip category (e.g., Keyboard Shortcuts, Slash Commands, CLI Flags)
- Three-column tables: Command/Shortcut | What It Does | Notes
- Entries sorted by usefulness within sections
- New entries appended to the appropriate section

**What distinguishes this from REFERENCE:**
- REFERENCE documents hold vendor sources plus recipes and traps from your own builds, organized by task
- CHEATSHEET documents are collections of discrete tips that grow incrementally through capture
- REFERENCE answers "How do we do X in this tool?" - CHEATSHEET answers "What are the quick tips for X?"

---

### TEMPLATE - Reusable Document Templates

**Purpose:** Canonical versions of recurring business documents that get customized per use. Contracts, SOW boilerplate, proposal templates, email templates - fill-in-the-blank artifacts that maintain standard terms while allowing per-engagement customization.

**Retrieval triggers:**
- "What's my standard service agreement?"
- "Draft a contract for a new client"
- "What template should I use for X?"
- "Where's the boilerplate for Y?"

**Structure:**
- Overview (what this template is for, when to use it)
- Customization guide (what fields to fill, what's fixed vs. negotiable)
- The template content itself (with fill-in markers)
- Key clause/section analysis (rationale for important provisions)
- Related documents

**What distinguishes this from STANDARD:**
- STANDARD documents define rules about how things should be done (normative)
- TEMPLATE documents are the actual reusable artifacts that get filled in per use (generative)
- STANDARD answers "What are the rules for X?" - TEMPLATE answers "Give me the boilerplate for X"

---

## Knowledge Layers

The knowledge library can be organized into distinct layers, each serving a different purpose. This is optional - a flat structure works fine for smaller collections - but layers help when your knowledge base grows beyond 20-30 documents.

### Operational Infrastructure

**Purpose:** How you do your work - methodology, procedures, standards, and operational knowledge.

**Characteristics:**
- Universal across clients/projects
- Defines how work is done (methodologies, procedures)
- Codifies taste and constraints (standards)
- Tool recipes and operator learnings (references)
- Buyer/stakeholder intelligence (personas)

### Domain Expertise

**Purpose:** What you know about industries and markets - specialized domain knowledge that may originate from client work but applies broadly.

**Characteristics:**
- Industry-specific facts and structures
- May originate from a project or engagement
- Reusable across projects in that domain
- Organized with domain tags for filtering

### Custom Applications

**Purpose:** Specifications for personal tools and custom applications - design systems, architecture, features, and extension patterns.

**Characteristics:**
- Describes a tool or app built for personal use
- Captures design decisions so future sessions can extend consistently
- Includes architecture, color schemes, component patterns, data flow

### Which Layer?

| If the document... | Layer |
|-------------------|-------|
| Describes how to do your work | Operational Infrastructure |
| Defines standards/conventions for output | Operational Infrastructure |
| Documents a tool or platform | Operational Infrastructure |
| Contains industry-specific facts | Domain Expertise |
| Explains domain terminology/structures | Domain Expertise |
| Could apply to multiple projects in a vertical | Domain Expertise |
| Specifies a personal tool or custom app | Custom Applications |
| Captures design decisions for a built tool | Custom Applications |

### Domain Document Metadata

Domain documents use the same metadata table as infrastructure docs, with two additional optional fields:

| Field | Description |
|-------|-------------|
| **Domain Tags** | Industry/vertical tags for filtering (e.g., `private-equity, PE, fund sizes`) |
| **Originating Client** | Project or engagement where this knowledge was developed |

---

## Naming Conventions

### The Filename as a Searchable Record

Filename generation is the process of extracting keywords from content and compressing them into a retrieval-optimized string within technical constraints. The goal: maximize keyword density within the budget so every character contributes to discoverability.

### Query Anticipation

The fundamental skill in filename generation is **query anticipation** - predicting what search terms will be used to find this content.

Ask yourself:
- What questions would someone ask that this file answers?
- What terms would they use in those questions?
- What synonyms or alternative phrasings might they use?

### Pattern

```
{document-code}_{CATEGORY}_{primary-subject}_{key-concepts}.md
```

The document code (e.g., `doc-26`) comes first for index sorting and quick lookup.

### Character Budget

| Segment | Characters | Examples |
|---------|------------|----------|
| **Document code** | 10-15 | `doc-26_`, `doc-4_` |
| **Category prefix** | 8-12 | `REFERENCE_`, `SCHEMA_`, `FRAMEWORK_`, `PROCEDURE_`, `STANDARD_`, `PROFILE_`, `PERSONA_`, `CHEATSHEET_`, `TEMPLATE_` |
| **Primary subject** | 10-30 | `clay-platform`, `lead-scoring`, `cro-buyer` |
| **Key concepts** | 30-80 | `enrichment-waterfall-api-integrations`, `fit-intent-matrix-tiers` |
| **Extension** | 3 | `.md` |

**Target:** 80-150 characters in the name portion (after document code and category prefix).

### Naming Rules

1. **Category prefix in ALL CAPS** - Enables sorting and instant type recognition
2. **Kebab-case name** - All lowercase, hyphens between words
3. **Category matches content type** - Use taxonomy definitions to select correct prefix
4. **Specific enough to disambiguate** - If two docs could share a name, they're probably scoped wrong

### Keyword Selection Strategy

**High-Value Keywords (Always Include):**
- Primary subject (tool, concept, or domain)
- Document type indicator (deep-dive, guide, primer, reference, spec)
- Key capabilities or frameworks covered
- Unique identifiers (names, dates, project codes)

**Medium-Value Keywords (Include When Space Permits):**
- Related tools or integrations
- Use cases this document addresses
- Industry or vertical
- Outcomes or status

**Low-Value Keywords (Skip These):**
- Generic words: "document," "file," "notes," "info," "data"
- Filler words: "the," "and," "for," "about," "with"
- Redundant context: don't repeat what's obvious from file type or location
- Category words in name: if prefix says `FRAMEWORK_`, don't add "framework" again

### Keyword Extraction Process

1. **Identify the Primary Subject** - What is this file fundamentally about? This becomes the anchor.
2. **Extract Key Concepts** - Named entities, technical terms, problems discussed, outcomes and decisions.
3. **Anticipate Queries** - For each concept: "Would someone search for this term to find this file?"
4. **Prioritize by Retrieval Value** - Rank by likelihood of appearing in search queries. Lead with highest-value terms.
5. **Compress to Budget** - Fit prioritized keywords into available character space. Use abbreviations sparingly and only when universally understood.

### Examples

| Keyword-Rich (Good) | Too Sparse (Bad) | Why |
|---------------------|------------------|-----|
| `doc-20_REFERENCE_clay-formula-cookbook-url-cleaning-text-patterns.md` | `doc-20_REFERENCE_clay.md` | Captures what someone would search for |
| `doc-15_SCHEMA_clay-enriched-company-structure.md` | `doc-15_SCHEMA_company.md` | Specifies entity type and data categories |
| `doc-14_PERSONA_cro-buyer-primer.md` | `doc-14_PERSONA_cro.md` | Includes concerns that trigger retrieval |
| `doc-13_FRAMEWORK_phone-number-scoring-guide.md` | `doc-13_FRAMEWORK_phone.md` | Adds key concepts for better matching |

### Multi-Domain Documents

When a document covers multiple tools or domains:

- `doc-N_REFERENCE_crm-integration-patterns-salesforce-hubspot-data-sync.md` (covers both CRMs)
- `doc-N_FRAMEWORK_waterfall-enrichment-strategy-clearbit-zoominfo-apollo.md` (covers multiple providers)

If truly split, create separate documents with cross-references.

### Naming Anti-Patterns

**Wrong Category:**
- `doc-N_REFERENCE_how-to-think-about-lead-scoring.md`
- "How to think about" signals FRAMEWORK, not REFERENCE
- Better: `doc-N_FRAMEWORK_lead-scoring-fundamentals-fit-intent-prioritization.md`

**Category Word Repeated:**
- `doc-N_PROCEDURE_procedure-for-scoring-leads.md`
- "procedure" already in prefix
- Better: `doc-N_PROCEDURE_lead-scoring-workflow-qualification-tiers.md`

**Inconsistent Format:**
- `Reference_Clay_Platform.md` or `reference-clay-platform.md`
- Category must be ALL CAPS, name must be all lowercase kebab-case, document code first
- Better: `doc-N_REFERENCE_clay-platform-enrichment-waterfall-api-integrations.md`

**Too Generic:**
- `notes.txt` or `document.md`
- Zero retrieval signal, impossible to distinguish

**Keyword Stuffing Without Structure:**
- `crm-sales-marketing-data-quality-integration-automation-workflow-pipeline.md`
- Keywords without logical grouping - structure helps both retrieval AND human understanding

---

## Document Structure Template

Every document should follow this structure, adapted to its category.

### Required Header Block

```markdown
# {Document Title}

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | One sentence describing what this document provides |
| **Trigger** | When should this document be retrieved? What questions/tasks? |
| **Scope** | What topics this document covers |
| **Not In Scope** | Explicit exclusions - what this document does NOT cover |
| **Dependencies** | Other documents that should be read alongside this one |
| **Keywords** | Synonyms, related terms, alternative phrasings that should trigger retrieval |
| **Maturity** | Draft / Working / Stable / Canonical / Obsolete |
| **Last Reviewed** | YYYY-MM-DD |
| **Source** | Where this came from: the session, call, research run or URL. Several allowed. |

---
```

**Source is required.** It lets you, or the AI, return to the conversation a rule came from. Strip it when you publish a document, as I do here.

### Body Structure

After the header block:

1. **Overview/Core Concept** - 2-3 paragraphs maximum. What is this, why does it matter?
2. **Main Content Sections** - Organized logically for the document type
3. **Quick Reference** - Tables, checklists, or summaries for fast lookup
4. **Cross-References** - Explicit links to related documents
5. **Changelog** (optional but recommended) - Track document evolution over time

### Changelog Convention

Documents that evolve over time should include a changelog section at the end. This serves two purposes: it helps humans understand how the document has developed, and it signals to the AI that certain sections may have been recently revised (and should be treated as current thinking rather than stale content).

**Format:**

```markdown
---

## Changelog

| Date | Change |
|------|--------|
| 2026-03-11 | Most recent change described here |
| 2026-02-15 | Earlier change described here |
| 2026-01-08 | Initial version |
```

**Rules:**
- New entries go at the top (most recent first)
- Use ISO dates (YYYY-MM-DD) for unambiguous sorting
- Keep descriptions concise - one line per change, focused on what changed and why
- If a document doesn't have a changelog but receives significant edits, add one
- The changelog is a lightweight audit trail, not a substitute for version control - no need to log every typo fix

### Section Header Guidelines

- Use H2 (`##`) for major sections
- Use H3 (`###`) for subsections
- Keep headers descriptive and searchable - "Phone Number Quality Tiers" not "Tiers"
- Front-load important words - "Salesforce Field Architecture" not "How to Structure Fields in Salesforce"

---

## Versioned Section Headers

Some documents hold text that gets copied into another tool, for example an agent prompt. Give such a section a version and date in its header: `## System Prompt (v4 - 2026-04-24)`. The header is a claim about the text below it, because it is what you read while copying.

**When anything under a versioned header changes, in this order:**

1. Wrap the existing version, header and body, in a collapsed `<details>` block.
2. Write the new version above it, with a bumped version number and today's date.
3. Add a short **What changed from vN** note under the new header.
4. Update `Last Reviewed`, `Source` and the changelog.

Even a one-word edit follows these steps. It prevents a header that says v4 above text that has already been patched, with no copy of v4 left.

---

## Retrieval Optimization

### Front-Loading

The first 200 words of a document have outsized importance for retrieval. The metadata table and overview section should contain all primary search terms.

### Self-Contained Sections

Each major section should be understandable without reading the entire document. Repeat critical context where necessary. Retrieval systems may pull only a section, not the full document.

### Explicit Negative Scope

Always state what a document does NOT cover. This prevents false-positive retrieval and helps the AI know when to keep searching.

```markdown
**Not In Scope:** This document covers HubSpot workflow automation. For HubSpot custom objects,
see the custom objects reference. For Salesforce workflows, see the Salesforce flow builder guide.
```

### Keyword Density

Include synonyms and alternative phrasings naturally in the text. If users might search for "enrichment waterfall," "data waterfall," or "cascading enrichment," all three should appear somewhere in the document.

### Cross-Reference Format

Use explicit, standardized cross-reference blocks:

```markdown
---

## Related Documents

- Platform capabilities reference
- Expected output format schema
- Scoring framework this builds on

---
```

---

## Claude Code Specifics

Claude Code reads files directly rather than using RAG chunking. This changes the optimization strategy.

### Directory Structure

Use a flat folder. The category lives in the filename, so one pattern (`knowledge/*SCHEMA*.md`) finds every document of a kind. Subfolders separate layers only.

```
knowledge/
├── MANIFEST.md                 # Index of record, read as a fallback
├── TOPIC-ROUTER.md             # How people talk -> filename keywords
├── doc-4_STANDARD_context-document-standards.md
├── doc-12_PROCEDURE_icp-persona-process-discovery.md
├── doc-14_PERSONA_cro-buyer-primer.md
├── [...]
├── domain/                     # Domain expertise layer, own manifest
└── custom-apps/                # Custom applications layer, own manifest
```

### Retrieval: Cheapest Step First

The root `CLAUDE.md` tells the AI in which order to look:

| Step | Mechanism | Cost |
|------|-----------|------|
| 1 | People directory: resolve a name | Near-free |
| 2 | Trigger phrase or skill match | Near-free |
| 3 | Filename search (`knowledge/*keyword*.md`) | Near-free |
| 4 | Topic router, then filename search again | Low |
| 5 | First 20 lines of candidate files | Low |
| 6 | Full manifest | High, fallback |
| 7 | Search inside file contents | Last resort |

The full description is in [Anatomy of a Context System](context-system-indexing-retrieval-architecture.md).

### Always-Consult Documents

A few documents apply to most tasks of a kind. Name them in the root `CLAUDE.md`, next to the workflow they govern ("for agent prompts, follow doc-19"), and leave the content in the document.

### Skills Point to Documents

A skill says what to do and in which order. The document holds how. Several skills can then follow the same standard, and the standard changes in one place.

---

## Common Pitfalls

### Over-Fragmentation

**Problem:** 50 small documents instead of 15 well-organized ones.

**Solution:** Consolidate until retrieval or cognitive load suffers. If two documents are always needed together, merge them.

### Scope Overlap

**Problem:** Two documents both seem relevant; AI picks the wrong one or misses information split across both.

**Solution:** Explicit negative scope, clear cross-references, or consolidation.

### Stale Cross-References

**Problem:** Document A references Document B, but B was renamed or removed.

**Solution:** Periodic audits, or use relative references that will break visibly if invalid.

### Context Buried Deep

**Problem:** Critical information is on page 5; retrieval grabs only page 2.

**Solution:** Front-load, use self-contained sections, repeat key context in relevant sections.

### Mixing Document Types

**Problem:** A "methodology" doc that also contains schema definitions and persona notes.

**Solution:** Split or clearly section with explicit internal routing.

---

## Document Checklist

Before finalizing any context document:

### Filename Checklist

- [ ] Category prefix is ALL CAPS and matches document type (REFERENCE, SCHEMA, FRAMEWORK, PROCEDURE, STANDARD, PROFILE, PERSONA, CHEATSHEET, TEMPLATE)
- [ ] Category word is NOT repeated in the name portion
- [ ] Primary subject clearly identifies the tool, concept, or domain
- [ ] 3-6 key concept keywords capture capabilities/frameworks covered
- [ ] Target length: 80-150 characters in name portion (after prefix)
- [ ] No generic filler words consuming character budget
- [ ] Keywords match terms someone would actually search
- [ ] File would be findable by someone who doesn't know it exists

### Content Checklist

- [ ] Metadata table is complete (Purpose, Trigger, Scope, Not In Scope, Dependencies, Keywords, Maturity, Last Reviewed, Source)
- [ ] No volatile vendor data; each value is replaced by its live source
- [ ] Maturity level is appropriate (Draft/Working/Stable/Canonical/Obsolete)
- [ ] First 200 words contain all primary search terms
- [ ] Negative scope is explicitly stated
- [ ] Sections are reasonably self-contained
- [ ] Cross-references use exact filenames
- [ ] Headers are descriptive and searchable
- [ ] No orphaned content that belongs in a different document

---

## Related Documents

- [Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md) - Foundational filename principles this document applies
- [Anatomy of a Context System](context-system-indexing-retrieval-architecture.md) - How documents built this way are found
- [Three Foundations of a Context OS](context-os-three-foundations.md) - Where to start
- Call transcript and meeting note naming conventions - Applies filename principles to call transcripts

---

## Changelog

| Date | Change |
|------|--------|
| 2026-11-24 | Brought up to date with the version in daily use: what a document holds (vendor data pulled live), Obsolete maturity level, Source field, REFERENCE category rewritten, versioned section headers, flat folder and retrieval order |
| 2026-03-11 | Renamed from "AI Knowledge Document Standards" to "AI Context Document Standards" for public clarity |
| 2026-03-11 | Added Changelog Convention section with format rules and guidance; added this changelog |
| 2026-03-11 | Initial public version - combined document standards and filename generation into a single self-contained resource |
