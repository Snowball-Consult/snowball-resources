# Snowball Resources

Methodologies, prompt templates, and frameworks from [Snowball Consult](https://snowball-consult.com) - a GTM data infrastructure consultancy.

These are shared as demos and inspiration. They come from a working consulting practice, not a textbook. Some reference internal dependencies that aren't included here.

Questions or want to chat? Reach out at andreas@snowball-consult.com

## Contents

- **[Deep Research: GTM Assessment Prompt](deep-research-gtm-assessment.md)** - Market-first prompt template for assessing prospect companies before discovery calls. Covers category dynamics, competitive landscape, customer world data characteristics, and engagement fit filtering.

- **[Deep Research Prompt Engineering](deep-research-prompt-engineering.md)** - Research-backed framework for transforming casual questions into structured Deep Research prompts, with building blocks ranked by evidence strength, two output branches (reference doc vs. domain learning), and before/after examples.

- **[AI Context Document Standards](ai-context-document-standards.md)** - Complete framework for structuring AI context documents - covers taxonomy (9 categories), maturity levels, naming conventions, retrieval optimization, and cross-referencing. The system that makes Claude Code's knowledge base work.

- **[Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md)** - Methodology for converting content into retrieval-optimized filenames through keyword extraction and query anticipation. Applicable to any file type in RAG-based systems.

- **[LinkedIn Profile Verification Agent - PE/Capital Markets](linkedin-profile-verification-pe-capital-markets.md)** - Production AI agent prompt (system + user + JSON output schema) for verifying enriched LinkedIn profiles against CRM contacts. Primed for PE/capital markets with 13 test cases covering domain aliases, career changes, name variants, and data provider errors.

- **[CRM Company Record Selection Agent](crm-company-record-selection-agent-domain-lookup-parent-child-disambiguation.md)** - AI agent spec for selecting the correct CRM company record when a domain lookup returns multiple results (parent companies, subsidiaries, business units). Three-tier selection logic (name match, title context, activity scoring), dual-lookup architecture, 6 test cases with real PE/financial services data patterns.

- **[Meeting Briefing Demo](meeting-briefing-demo.html)** - A real meeting briefing that aligned four stakeholders across three organizations and led to a pilot decision in 30 minutes. Sanitized from an actual client engagement. Shows the output of the briefing page system below.

- **[Client Briefing Pages: HTML Synthesis Pipeline](client-briefing-pages-html-synthesis-pipeline.md)** - The procedure document that instructs how meeting briefings and stakeholder updates are built - from transcript ingestion to polished HTML. The system behind the meeting briefing demo above.

- **[Design Language: Brand Identity Visual System](design-language-brand-identity-visual-system.md)** - The foundational design system governing all visual output - color palette (dark + light mode), typography (Inter + JetBrains Mono), spacing, layout principles, CSS custom properties. The brand layer that makes every deliverable look consistent.

- **[Ideal Buyer Persona Definition - PE/Capital Markets](ideal-buyer-persona-definition-pe-capital-markets.md)** - Complete buyer persona definition for a B2B SaaS company selling into Private Equity. Includes a "read aloud" narrative, primary/secondary/emerging personas, signal ranking, buying process roles, and skip rules. Demonstrates the structure and depth of a real persona document built from 7+ stakeholder discovery calls.

- **[Claude Code Session Menu Bar](claude-code-session-menu-bar-swiftbar-auto-titling.md)** - Architecture for a macOS menu bar plugin that browses and resumes Claude Code sessions with auto-generated titles. Covers the SessionEnd hook pattern for auto-titling via Haiku, where Claude Code stores session data, dark mode support, and performance caching. Built with SwiftBar + zero pip dependencies.
