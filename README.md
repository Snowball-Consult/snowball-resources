# Snowball Resources

Methodologies, prompt templates, and frameworks from [Snowball Consult](https://snowball-consult.com) - a GTM data infrastructure consultancy.

These are shared as demos and inspiration. They come from a working consulting practice, not a textbook. Some reference internal dependencies that aren't included here.

Questions or want to chat? Reach out at andreas@snowball-consult.com

## Skills

Plug-and-play skills for Claude Code. Copy to `~/.claude/skills/` and use immediately.

- **[ASCII Block Art](skills/ascii/)** - Render any word or phrase as large, bold ASCII block art, auto-fitted to terminal width. Supports A-Z, 0-9, punctuation, emoji, word-wrapping. Install and use with `/ascii hello world`.

- **[Quiz Me: Q&A Learning Log](skills/qa-log/)** - Capture-first spaced-repetition learning loop for Claude Code. `/learned` turns any good answer into a recall card, `/quiz` reviews due cards with free recall and semantic grading, and a session-start hook reminds you when cards are due. SM-2-lite scheduling, plain markdown cards, standard library only.

## Contents

- **[Don't Ask Me. Ask Claude Code - and Get It *Built* Instead of Explained](ask-claude-code-instead-of-me-get-it-built-not-explained.md)** - Start here if you're new to working with an AI coding agent. A small, real question ("how did you get bold text into that Slack message?") used to teach the move that matters: asking a person gets you a description of a solution, asking Claude Code gets you the solution, running. Walks the four escalating prompts from help-center answer to commissioned tool, the three approaches that failed on the way to the right one, the five habits underneath, and - as the punchline - the raw, rambling, dictated prompt that produced the document itself.

- **[Deep Research: GTM Assessment Prompt](deep-research-gtm-assessment.md)** - Market-first prompt template for assessing prospect companies before discovery calls. Covers category dynamics, competitive landscape, customer world data characteristics, and engagement fit filtering.

- **[Deep Research Prompt Engineering](deep-research-prompt-engineering.md)** - Research-backed framework for transforming casual questions into structured Deep Research prompts, with building blocks ranked by evidence strength, two output branches (reference doc vs. domain learning), and before/after examples.

- **[Anatomy of a Context System: The Indexing Layer](context-system-indexing-retrieval-architecture.md)** - How a working context system indexes itself so an agent can find the right document out of hundreds while spending almost no budget. Names every constituent element (codes, filenames-as-records, taxonomy, front-loaded metadata, maturity, manifest, topic router, people directory) and walks the cheapest-first retrieval cascade that ties them together. The umbrella over the two documents below.

- **[AI Context Document Standards](ai-context-document-standards.md)** - Complete framework for structuring AI context documents - covers taxonomy (9 categories), maturity levels, naming conventions, retrieval optimization, and cross-referencing. The system that makes Claude Code's knowledge base work.

- **[Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md)** - Methodology for converting content into retrieval-optimized filenames through keyword extraction and query anticipation. Applicable to any file type in RAG-based systems.

- **[Claygent JSON Prompting Guide](claygent-json-prompting-guide.md)** - Canonical structure for building Clay AI agent prompts with JSON output schemas. Three-part format (main prompt, separated schema, variables block), web-access vs local-data prompt splitting, Clay-specific schema constraints, and the most common failure modes. The reference used to build every Claygent worth shipping.

- **[CRM Company Record Selection Agent](crm-company-record-selection-agent-domain-lookup-parent-child-disambiguation.md)** - AI agent spec for selecting the correct CRM company record when a domain lookup returns multiple results (parent companies, subsidiaries, business units). Three-tier selection logic (name match, title context, activity scoring), dual-lookup architecture, 6 test cases with real PE/financial services data patterns.

- **[Title-Only Disqualification Filter (AI Column)](title-only-disqualification-filter-ai-column.md)** - A cheap, deterministic quality floor that screens an enriched/keyword-sourced contact list from the job title alone, returning a binary keep/exclude. Exclusion-only, biased toward keeping, with explicit guards against killing the right person on a wrong-looking title. Full prompt (system + user + schema + 30 evidence-grounded few-shot examples), threshold table, calibration approach, and validation results.

- **[How a Title-Only Disqualification Filter Gets Built (A-Z)](title-only-disqualification-filter-build-walkthrough.md)** - The companion walkthrough: the step-by-step story of building the filter above from a raw idea to a validated tool in one working session. The reasoning, the pushback on first instincts, the subtle "SME labels aren't the labels you need" trap, the landmines, and how to validate on the error that actually matters. Process inspiration, not a recipe.

- **[Meeting Briefing Demo](meeting-briefing-demo.html)** - A real meeting briefing that aligned four stakeholders across three organizations and led to a pilot decision in 30 minutes. Sanitized from an actual client engagement. Shows the output of the briefing page system below.

- **[Client Briefing Pages: HTML Synthesis Pipeline](client-briefing-pages-html-synthesis-pipeline.md)** - The procedure document that instructs how meeting briefings and stakeholder updates are built - from transcript ingestion to polished HTML. The system behind the meeting briefing demo above.

- **[Design Language: Brand Identity Visual System](design-language-brand-identity-visual-system.md)** - The foundational design system governing all visual output - color palette (dark + light mode), typography (Inter + JetBrains Mono), spacing, layout principles, CSS custom properties. The brand layer that makes every deliverable look consistent.

- **[Ideal Buyer Persona Definition - Application Delivery Infrastructure](ideal-buyer-persona-definition-application-delivery-infrastructure.md)** - Complete buyer persona definition for a B2B infrastructure company selling application delivery / traffic management into Fortune 500 enterprises. Includes a "read aloud" narrative, primary/secondary/emerging personas, champion archetypes, signal ranking, buying process roles, and industry segmentation. Demonstrates the structure and depth of a research-backed persona document.

- **[Claude Code Session Menu Bar](claude-code-session-menu-bar-swiftbar-auto-titling.md)** - Architecture for a macOS menu bar plugin that browses and resumes Claude Code sessions with auto-generated titles. Covers the SessionEnd hook pattern for auto-titling via Haiku, where Claude Code stores session data, dark mode support, and performance caching. Built with SwiftBar + zero pip dependencies.

- **[Prioritize Events Against Your Context](prioritize-events-against-your-context.md)** - A drop-in Claude Code recipe that turns any messy event calendar into a context-fit, opinionated priority list. Built originally for NY Tech Week 2026; the same shape works for any "many candidates, limited time" decision driven by personal context. Conversational flow, ranking schema, output template, worked example included.
