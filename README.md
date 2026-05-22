# Snowball Resources

Methodologies, prompt templates, and frameworks from [Snowball Consult](https://snowball-consult.com) - a GTM data infrastructure consultancy.

These are shared as demos and inspiration. They come from a working consulting practice, not a textbook. Some reference internal dependencies that aren't included here.

Questions or want to chat? Reach out at andreas@snowball-consult.com

## Skills

Plug-and-play skills for Claude Code. Copy to `~/.claude/skills/` and use immediately.

- **[ASCII Block Art](skills/ascii/)** - Render any word or phrase as large, bold ASCII block art, auto-fitted to terminal width. Supports A-Z, 0-9, punctuation, emoji, word-wrapping. Install and use with `/ascii hello world`.

## Contents

- **[Deep Research: GTM Assessment Prompt](deep-research-gtm-assessment.md)** - Market-first prompt template for assessing prospect companies before discovery calls. Covers category dynamics, competitive landscape, customer world data characteristics, and engagement fit filtering.

- **[Deep Research Prompt Engineering](deep-research-prompt-engineering.md)** - Research-backed framework for transforming casual questions into structured Deep Research prompts, with building blocks ranked by evidence strength, two output branches (reference doc vs. domain learning), and before/after examples.

- **[AI Context Document Standards](ai-context-document-standards.md)** - Complete framework for structuring AI context documents - covers taxonomy (9 categories), maturity levels, naming conventions, retrieval optimization, and cross-referencing. The system that makes Claude Code's knowledge base work.

- **[Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md)** - Methodology for converting content into retrieval-optimized filenames through keyword extraction and query anticipation. Applicable to any file type in RAG-based systems.

- **[Claygent JSON Prompting Guide](claygent-json-prompting-guide.md)** - Canonical structure for building Clay AI agent prompts with JSON output schemas. Three-part format (main prompt, separated schema, variables block), web-access vs local-data prompt splitting, Clay-specific schema constraints, and the most common failure modes. The reference used to build every Claygent worth shipping.

- **[LinkedIn Profile Verification Agent - PE/Capital Markets](linkedin-profile-verification-pe-capital-markets.md)** - Production AI agent prompt (system + user + JSON output schema) for verifying enriched LinkedIn profiles against CRM contacts. Primed for PE/capital markets with 13 test cases covering domain aliases, career changes, name variants, and data provider errors.

### Private Equity Knowledge Set

These three documents form a coherent PE knowledge stack: market structure, buyer persona, and contact targeting. They pair with the LinkedIn verification agent above and were built from a working PE engagement.

- **[Private Equity Fund Sizes and Structures Reference](private-equity-fund-sizes-structures-terminology.md)** - Comprehensive reference for identifying, categorizing, and extracting PE fund size information from unstructured sources. Covers flagship fund taxonomy, fund size terminology (committed capital vs AUM vs NAV), market segment thresholds, vintage year conventions, data sources, and disambiguation of non-PE vehicles (credit, real estate, infrastructure, VC, BDCs, SPACs).

- **[PE Capital Markets Professional - Buyer Primer](pe-capital-markets-professional-buyer-primer.md)** - 11-dimension buyer persona for the ~2,500 PE capital markets VPs and MDs who structure debt across private equity portfolios. Maps daily reality, career arc, problem landscape, knowledge domains (LMEs, NAV lending, private credit), information ecosystem, relationship dynamics, technology stack, macro trends, professional identity, and unmet needs. Demonstrates the depth of a research-backed buyer persona for a niche professional audience.

- **[PE Job Title Decomposition Taxonomy](pe-job-title-decomposition-taxonomy.md)** - PE-specific overlay for parsing job titles into Function and Seniority. Covers the canonical PE title hierarchy, geographic variation (US, UK, Germany, France, Nordics, Asia, Middle East), function classification codes, C-suite/partnership overlap, edge cases, and decision-tree classification rules. Built from 16K+ manually classified PE contacts plus wall-street research synthesis.

- **[CRM Company Record Selection Agent](crm-company-record-selection-agent-domain-lookup-parent-child-disambiguation.md)** - AI agent spec for selecting the correct CRM company record when a domain lookup returns multiple results (parent companies, subsidiaries, business units). Three-tier selection logic (name match, title context, activity scoring), dual-lookup architecture, 6 test cases with real PE/financial services data patterns.

- **[Meeting Briefing Demo](meeting-briefing-demo.html)** - A real meeting briefing that aligned four stakeholders across three organizations and led to a pilot decision in 30 minutes. Sanitized from an actual client engagement. Shows the output of the briefing page system below.

- **[Client Briefing Pages: HTML Synthesis Pipeline](client-briefing-pages-html-synthesis-pipeline.md)** - The procedure document that instructs how meeting briefings and stakeholder updates are built - from transcript ingestion to polished HTML. The system behind the meeting briefing demo above.

- **[Design Language: Brand Identity Visual System](design-language-brand-identity-visual-system.md)** - The foundational design system governing all visual output - color palette (dark + light mode), typography (Inter + JetBrains Mono), spacing, layout principles, CSS custom properties. The brand layer that makes every deliverable look consistent.

- **[Ideal Buyer Persona Definition - Application Delivery Infrastructure](ideal-buyer-persona-definition-application-delivery-infrastructure.md)** - Complete buyer persona definition for a B2B infrastructure company selling application delivery / traffic management into Fortune 500 enterprises. Includes a "read aloud" narrative, primary/secondary/emerging personas, champion archetypes, signal ranking, buying process roles, and industry segmentation. Demonstrates the structure and depth of a research-backed persona document.

- **[Claude Code Session Menu Bar](claude-code-session-menu-bar-swiftbar-auto-titling.md)** - Architecture for a macOS menu bar plugin that browses and resumes Claude Code sessions with auto-generated titles. Covers the SessionEnd hook pattern for auto-titling via Haiku, where Claude Code stores session data, dark mode support, and performance caching. Built with SwiftBar + zero pip dependencies.

- **[Prioritize Events Against Your Context](prioritize-events-against-your-context.md)** - A drop-in Claude Code recipe that turns any messy event calendar into a context-fit, opinionated priority list. Built originally for NY Tech Week 2026; the same shape works for any "many candidates, limited time" decision driven by personal context. Conversational flow, ranking schema, output template, worked example included.
