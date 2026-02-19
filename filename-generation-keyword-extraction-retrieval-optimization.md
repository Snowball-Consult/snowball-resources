# Filename Generation: Keyword Extraction and Retrieval Optimization

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Foundational methodology for converting any content into retrieval-optimized filenames through keyword extraction and query anticipation |
| **Trigger** | Naming any file for AI retrieval systems, building filename generation tools, optimizing existing file libraries |
| **Scope** | Filename architecture, character budgets, keyword extraction principles, query anticipation, anti-patterns—applicable to ALL file types |
| **Not In Scope** | Specific file type patterns (see dependent documents), document content structure, platform-specific RAG mechanics |
| **Dependencies** | None (foundational document) |
| **Keywords** | filename, file naming, keyword extraction, retrieval optimization, RAG, query anticipation, character budget, keyword density, searchability, discoverability |
| **Maturity** | Stable |
| **Last Reviewed** | 2026-02-01 |

---

## Core Principle

**The filename is not a label—it's a searchable metadata record.**

Every word in a filename is a potential retrieval hook. In RAG-based systems (Claude Projects, vector databases, search indexes), filenames directly influence whether the AI finds your document. A poorly named file with perfect content may never surface.

Filename generation is the process of **extracting keywords from content and compressing them into a retrieval-optimized string** within technical constraints.

---

## The Two-Phase Model

Every file must optimize for two sequential phases:

1. **Discovery** — Can the system find this file when it's relevant?
2. **Execution** — Once found, can the content be correctly interpreted?

The filename controls discovery. Content controls execution. **Most files fail at discovery** because their filenames contain zero overlap with the search queries users generate.

---

## Query Anticipation

The fundamental skill in filename generation is **query anticipation**—predicting what search terms will be used to find this content.

Ask yourself:
- What questions would someone ask that this file answers?
- What terms would they use in those questions?
- What synonyms or alternative phrasings might they use?

**Example:** A document about CRM data quality issues might be searched for using:
- "CRM data quality"
- "Salesforce data problems"
- "duplicate records"
- "data hygiene"
- "dirty data cleanup"

A retrieval-optimized filename would include several of these terms.

---

## Technical Constraints

### Filename Length

- **Maximum:** 255 characters (filesystem limit)
- **Minimum:** 1 character
- **Recommended:** 150-220 characters for maximum keyword density with buffer

### Forbidden Characters

Cannot use: `< > : " | ? * \ /` or unicode characters 0-31

Safe to use: Letters, numbers, hyphens, underscores, periods, parentheses, brackets, spaces (though hyphens/underscores preferred for cross-platform compatibility)

### Format Conventions

- **Kebab-case:** All lowercase, hyphens between words (`lead-scoring-fundamentals`)
- **Underscores for segment separation:** Use `_` to separate logical segments (`DATE_COMPANY_TYPE`)
- **No spaces:** Replace with hyphens for compatibility

---

## Character Budget Framework

Think of filename generation as **allocating a character budget** across semantic segments. The exact allocation varies by file type, but the principle is universal.

**General Framework (255 characters max):**

| Segment | Characters | Purpose |
|---------|------------|---------|
| **Primary identifier** | 10-40 | What is this? (category, date, entity) |
| **Secondary identifiers** | 10-40 | Who/what else? (people, companies, subtypes) |
| **Core concepts** | 50-100 | Main topics, capabilities, frameworks |
| **Contextual keywords** | 30-80 | Outcomes, use cases, related terms |
| **Extension** | 3-5 | File type (`.md`, `.txt`, `.pdf`) |

**The goal:** Maximize keyword density within the budget. Every character should contribute to discoverability.

---

## Keyword Selection Strategy

### High-Value Keywords (Always Include)

- **Primary subject** — The main entity, tool, concept, or domain
- **Type indicator** — What kind of content (discovery, demo, deep-dive, guide, spec)
- **Key capabilities or concepts** — Main features, frameworks, methods covered
- **Unique identifiers** — Names, dates, project codes that enable precise retrieval

### Medium-Value Keywords (Include When Space Permits)

- **Related tools or integrations** — Secondary systems mentioned
- **Use cases** — What tasks or questions this addresses
- **Industry or vertical** — If domain-specific
- **Outcomes or status** — Results, decisions, next steps

### Low-Value Keywords (Skip These)

- **Generic words:** "document," "file," "notes," "info," "data"
- **Filler words:** "the," "and," "for," "about," "with"
- **Redundant context:** Don't repeat what's obvious from file type or location
- **Category words in name:** If prefix says `METHODOLOGY_`, don't add "methodology" again

---

## Keyword Extraction Process

When converting content into a filename:

### Step 1: Identify the Primary Subject
What is this file fundamentally about? This becomes the anchor of your filename.

### Step 2: Extract Key Concepts
Scan for:
- Named entities (people, companies, products, projects)
- Technical terms and frameworks
- Problems and pain points discussed
- Outcomes and decisions

### Step 3: Anticipate Queries
For each concept, ask: "Would someone search for this term to find this file?"

### Step 4: Prioritize by Retrieval Value
Rank keywords by how likely they are to appear in search queries. Lead with highest-value terms.

### Step 5: Compress to Budget
Fit prioritized keywords into available character space. Use abbreviations sparingly and only when universally understood.

---

## Synonym Coverage

When character budget allows, include alternative phrasings for key concepts:

- Both full name AND abbreviation (`salesforce` and `sfdc`)
- Both formal term AND colloquial term (`customer relationship management` vs `crm`)
- Both problem AND solution framing (`data-quality-issues` and `data-cleanup`)

**Example:** A file about CRM integration patterns might warrant both "crm" and "salesforce" and "hubspot" if all are relevant, since users might search any of these terms.

---

## Filename Anti-Patterns

### Too Generic
❌ `notes.txt` or `document.md`
- Zero retrieval signal
- Impossible to distinguish from other files
- Wastes entire character budget

### Redundant Words
❌ `meeting-notes-from-call-transcript-document.txt`
- "meeting," "notes," "call," "transcript," "document" all say the same thing
- Could be: `2026-01-08_acme-corp_discovery_pain-points-data-quality.txt`

### Missing Key Concepts
❌ `salesforce.md`
- What about Salesforce? Configuration? Integration? Troubleshooting?
- Could be: `TECHNICAL_salesforce-integration-patterns-data-sync-field-mapping.md`

### Inconsistent Formatting
❌ `Meeting Notes - Acme Corp (Jan 8).txt`
- Spaces cause cross-platform issues
- Inconsistent separators
- Date not sortable
- Could be: `2026-01-08_acme-corp_meeting_discovery.txt`

### Keyword Stuffing Without Structure
❌ `crm-sales-marketing-data-quality-integration-automation-workflow-pipeline.md`
- Keywords without logical grouping
- No indication of what the file actually covers
- Structure helps both retrieval AND human understanding

---

## Validation Checklist

Before finalizing any filename:

- [ ] Primary subject is clearly identifiable
- [ ] 5-10 meaningful keywords are included
- [ ] Keywords match terms someone would actually search
- [ ] No generic filler words consuming character budget
- [ ] No redundant words saying the same thing
- [ ] Format is consistent (kebab-case, proper separators)
- [ ] Total length is within recommended range (150-220 chars)
- [ ] No forbidden characters
- [ ] File would be findable by someone who doesn't know it exists

---

## Application to Specific File Types

This document provides foundational principles. For file-type-specific patterns, see:

- `METHODOLOGY_ai-knowledge-document-standards.md` — Knowledge base documents (TECHNICAL, SCHEMA, METHODOLOGY, PERSONA, CONTEXT categories)
- `METHODOLOGY_claude-project-files-call-transcripts.md` — Call transcripts and meeting notes (date, company, participants, call-type patterns)

Each dependent document applies these principles to its specific context with tailored keyword extraction frameworks and examples.

---

## Related Documents

- `METHODOLOGY_ai-knowledge-document-standards.md` — Applies these principles to knowledge base documents
- `METHODOLOGY_claude-project-files-call-transcripts.md` — Applies these principles to call transcripts

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-17 | Initial version — extracted foundational filename principles from ai-knowledge-document-standards and claude-project-files-retrieval-optimization |

