# Deep Research Prompt Engineering

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Research-backed framework for transforming casual questions into structured Deep Research prompts that produce readable, high-quality output - optimized for either foundational reference documents or domain learning |
| **Trigger** | Preparing a Deep Research prompt, wanting to learn a topic deeply, building a knowledge base document from scratch, turning a vague question into a structured research brief |
| **Scope** | Prompt construction methodology grounded in official platform guidance and academic research, output structure design for human reading flow, question decomposition, two use-case branches (reference doc vs. domain learning), before/after transformation examples, workflow best practices |
| **Not In Scope** | Domain-specific prompt templates (see [Deep Research: GTM Assessment Prompt](deep-research-gtm-assessment.md)), AI agent prompting, Claude Projects instructions, prompt engineering for structured JSON output, API-level prompt engineering for developers |
| **Dependencies** | AI knowledge document standards (not included), [Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md) |
| **Keywords** | Deep Research, prompt engineering, research prompt, question transformation, foundational document, domain learning, reading flow, executive overview, first principles, scope boundaries, output structure, reference document, primer, Claude, AI research, success criteria, source quality, reasoning models |
| **Maturity** | Working |
| **Last Reviewed** | 2026-02-15 |

---

## Overview

Deep Research tools (Claude, ChatGPT, Gemini) are powered by reasoning models that autonomously search, synthesize, and structure information. The prompt you write determines the quality of everything that follows.

This framework is grounded in what the companies that build these tools actually recommend, cross-referenced with academic research on what works. It covers:

1. **How to write the prompt** - the building blocks, ranked by evidence strength
2. **How to structure the output you ask for** - what makes DR output readable and useful for your purpose
3. **How to work with DR** - the workflow around the prompt, not just the prompt itself

Two primary use cases require different approaches:

- **Reference / Foundational Document** - A comprehensive resource for lookup, decisions, or an AI knowledge base. Optimized for retrieval and repeated use.
- **Domain Learning / Getting Up to Speed** - Deep understanding of a new topic. Optimized for reading front-to-back and building mental models.

Your prompt should make clear which one you need. They produce different output structures.

### Key principle: Guide, don't micromanage

Deep Research runs on reasoning models (Claude with extended thinking, OpenAI o3/o4, Gemini 2.5). These models perform better with high-level guidance than step-by-step prescriptions. Anthropic's own engineering team found that Claude "often performs better when told to 'just think deeply about a task' rather than given step-by-step prescriptive guidance, as the model's creativity in approaching problems may exceed a human's ability to prescribe the optimal thinking process." OpenAI's DR researchers echo this: "Too many details or overly rigid instructions can limit creativity and reduce accuracy and depth."

Your prompt should define *what* you need and *why*, then trust the reasoning model to figure out *how* to research it.

---

## Anatomy of a Great DR Prompt

These building blocks are ranked by evidence strength across official platform guidance, academic research, and practitioner testing. Not every prompt needs all of them - see "Quick Transformation" in the examples section.

### 1. Purpose & Success Criteria

Tell DR why you need this, how you'll use it, and what "done" looks like. Multiple sources identify success criteria as the single most under-used prompt element.

**Why it matters:** Without a purpose, DR defaults to "general encyclopedia overview." Without success criteria, it can't evaluate whether it's gone deep enough.

**Example:**
```
I need a comprehensive primer I can reference long-term when designing
CRM identity architectures for B2B clients. This will become a
foundational document in my knowledge base.

A complete answer covers: unique identifier mechanics for both company
and contact records, the architectural trade-offs between identity
approaches, and how enrichment pipelines interact with CRM uniqueness
constraints. If it doesn't cover those three dimensions thoroughly,
it's not done.
```

### 2. Your Context

Who you are, what you already know, and your professional angle. David Hershey (Anthropic Applied AI) puts it well: "It's so hard to untangle in your own brain all of the stuff that you know that Claude does not know, and write it down." Think of DR as a brilliant but new colleague with no context about your situation.

**Why it matters:** DR calibrates depth and technicality to the audience. Without context, it defaults to a general audience, spending space on things you already know and skimming things you actually need.

**Example:**
```
I'm a GTM data consultant working with Series A through Series C B2B
companies. I build data pipelines, enrichment workflows, and CRM
infrastructure in HubSpot and Salesforce.
```

### 3. First-Principles Grounding

Ask DR to explain *why* before *how*. This transforms output from surface-level descriptions into genuine understanding.

**Why it matters:** The difference between "HubSpot uses email as the unique identifier for contacts" and "Here's why CRMs need unique identifiers at all, what problems they solve, what goes wrong without them, and why email became the default choice despite its limitations." First-principles grounding produces the kind of output that stays useful as tools and platforms change.

**Example:**
```
Start from first principles. Before getting into CRM-specific
mechanics, explain WHY record identity and uniqueness matters. What
problems does it solve? What goes wrong without it? Build up from
there so someone without a database background understands the "why"
before the "how."
```

### 4. Structured Sub-Questions

Break your topic into 3-7 specific areas of inquiry. The framing "What I need to understand" works well because it signals comprehension goals rather than just information retrieval.

**Why it matters:** Without sub-questions, DR decides what's important. Your priorities and DR's defaults rarely align. Anthropic's own multi-agent research system works by decomposing complex queries into clearly bounded sub-tasks - your sub-questions give it a head start on this decomposition.

**Example:**
```
What I need to understand:

For company records:
- What fields serve as unique identifiers
- When domain is the right uniqueness key vs. when it breaks down
- How HubSpot and Salesforce handle company deduplication natively

For contact records:
- The fundamental trade-off between person-stable identifiers and
  employment-stable identifiers
- How this choice interacts with CRM architecture decisions
```

### 5. Scope Boundaries

Explicit "not in scope" / "what I don't need" statements. These prevent DR from filling space with adjacent topics that dilute the core output.

**Why it matters:** DR fills available space. Without boundaries, a CRM identity prompt will drift into marketing automation, GDPR compliance, and CRM selection. Exclusions are especially important for topics that border multiple domains.

**Example:**
```
What I don't need:
- Marketing automation or lead scoring
- GDPR/privacy compliance (I'll handle that separately)
- CRM selection advice
```

### 6. Depth Calibration & Signal Words

Tell DR where to go deep and where to skim. Also know that specific words in your prompt trigger different research intensity.

**Why it matters:** Claude's system prompt reveals that queries containing words like "comprehensive," "deep dive," or "analyze" trigger at least 5 tool calls (searches). Without these signals, DR may do a single search and stop. Conversely, you can use depth words strategically: use them on the dimensions that matter most, and use lighter language ("briefly cover," "touch on") for context sections.

**Example:**
```
Go deep on the trade-offs between person-stable and employment-stable
identifiers - this is the core architectural decision I face regularly.
Briefly cover the deduplication workflow - I mainly need to know what
tools exist and when to use them.
```

### 7. Output Format & Source Quality

How you want the output structured and what sources to prioritize. This is where the two use-case branches diverge (see next section).

Anthropic's engineering team discovered that their research agents initially chose SEO-optimized content farms over authoritative sources (academic papers, primary documentation, expert blogs). Asking for source quality explicitly helps.

**Why it matters:** DR's default output structure is a flat essay. If you need a reference document with comparison tables and decision frameworks, you have to ask for it. If you need authoritative sources rather than surface-level blog posts, say so.

**Example:**
```
Structure this as a reference document I can use long-term. Use tables
for comparisons. Be specific about both HubSpot and Salesforce field
names, objects, and API behavior. Prioritize primary sources and
official documentation over third-party blog posts. Flag areas where
the "right answer" depends on context.
```

### 8. Domain Grounding & Keywords

Industry context, typical scenarios, real-world constraints, and specific terminology. For DR tools that search the web, specific keywords (brand names, technical terms, product names) are directly used as search queries - providing them saves the model time and improves relevance.

**Example:**
```
Industry context:
- My clients are in private equity, capital markets, fintech, B2B SaaS
- Contact mobility is very high - people move between firms frequently
- Company structures are complex - PE firms have portfolio companies,
  subsidiaries, fund entities
- Typical CRM size: 10K-100K contacts, 2K-20K companies
- Key tools: HubSpot, Salesforce, Clay, Apollo, ZoomInfo
```

---

## The Output Structure That Works

Both use cases share the same opening. They diverge after the executive overview.

### Shared Opening

Every DR output should start with these two elements:

**1. What This Is (2-3 sentences)**

Orient the reader immediately. What topic, what angle, what's covered. A reader should know within 10 seconds whether this document answers their question.

**2. Executive Overview**

The key findings and the "so what." A reader who stops after this section should walk away with the core insight. This isn't a table of contents - it's a synthesis of the most important things DR found.

For reference docs, the executive overview answers: "What are the key things I need to know before diving into the details?"

For learning docs, the executive overview answers: "What's the landscape, and what's the most important thing to understand?"

### Branch A: Reference / Foundational Document

After the executive overview, optimize for **lookup and retrieval**. The reader will come back to this document many times, scanning for specific information.

**Structure pattern:**
- Detailed data sections organized by sub-topic (from your sub-questions)
- Comparison tables for platform/tool/approach differences
- Taxonomy sections (classifying and naming things)
- Decision frameworks ("when X vs. Y" guides)
- Edge cases and exceptions (where the general rule breaks down)
- Glossary of key terms (especially for domains with overloaded terminology)

**Writing style for reference:**
- Section headers should be scannable and descriptive - a reader skimming headers should understand the document's coverage
- Heavy use of tables for structured data
- When a topic has two valid approaches, present both with trade-offs rather than picking one
- Flag uncertainty explicitly: "This depends on context" with the factors that drive the decision
- Cross-reference between sections when concepts connect

**Ask for it like this:**
```
Structure this as a reference document I can use long-term. Organize
by [your sub-topics]. Use tables for comparisons. Flag areas where the
right answer depends on context. Include a glossary for terminology
that has multiple meanings in different contexts.
```

### Branch B: Domain Learning / Getting Up to Speed

After the executive overview, optimize for **reading front-to-back**. The reader will go through this once (maybe twice) to build understanding.

**Structure pattern:**
- Why this matters (first-principles foundation)
- Core concepts and vocabulary (so the reader can follow the rest)
- How it works (mechanics, with progressive depth)
- Key trade-offs and tensions (where reasonable people disagree)
- Common misconceptions (things most people get wrong)
- Mental models (frameworks for thinking about the topic going forward)
- Where this gets complicated (advanced nuance for later reference)

**Writing style for learning:**
- More narrative prose, fewer tables
- Build understanding layer by layer - each section should build on the previous one
- Use analogies when introducing unfamiliar concepts
- "The key insight is..." callouts for the ideas that matter most
- Separate "what most people think" from "what's actually true" when they differ
- End sections with the one thing to remember, not an exhaustive summary

**Ask for it like this:**
```
Structure this for someone getting up to speed. Start with why this
matters, then build from foundational concepts to nuance. Use
analogies where helpful. I want to read this front-to-back and come
away with strong mental models, not just facts. Call out common
misconceptions. End with the mental models I should carry forward.
```

### Output Type: Primer

A "primer" is a specific flavor of Branch B (Domain Learning) with stronger requirements on tone, first-principles depth, and practitioner orientation. When the prompt goal is a primer, apply these additional constraints on top of Branch B's structure:

**Tone: matter-of-fact practitioner voice.** No marketing-whitepaper language. No "unlock," "leverage," "empower," "transform," "harness," or consultant-speak hedging. State things directly. When something is broken, say it's broken and explain why. When a number exists, use the number. When research supports a claim, cite the research inline. The tone should read like a senior practitioner explaining the craft to another practitioner - direct, specific, opinionated where the evidence supports opinions.

**First-principles foundation must be extensive, not a brief intro.** A primer earns its name by building genuine understanding from the ground up. The "why this matters" and "core concepts" sections should be substantial - not a paragraph before jumping to tactics. The reader should understand the underlying mechanics well enough to reason about novel situations, not just follow a checklist.

**Practitioner best practices over theoretical frameworks.** Every section should answer "what does a practitioner actually do with this?" Include specific diagnostics, benchmarks, tooling, and methodology. Where benchmarks exist, include them with sources. Where formulas or measurement approaches exist, include them. The output should be usable in the field, not just intellectually interesting.

**Misconceptions section should address real-world pushback.** Not abstract misconceptions but the specific wrong beliefs that stakeholders, clients, or colleagues hold - and the evidence that contradicts them. Frame these as "what you'll hear" and "what's actually true."

**Quantify wherever possible.** Decay rates, benchmark ranges, cost estimates, time-to-impact, industry averages. Practitioners need numbers to scope work, set expectations, and justify recommendations.

**Ask for it like this:**
```
Write in a matter-of-fact practitioner tone. No marketing-whitepaper
language - state things directly, use specific numbers, cite research
inline. When something is broken, say it's broken and explain why.

Build an extensive first-principles foundation before tactics. I need
to understand the underlying mechanics well enough to reason about
edge cases, not just follow steps. The "why" sections should be
substantial.

Ground every section in practitioner best practices - specific
diagnostics, benchmarks with sources, measurement methodology,
tooling. This should be usable in the field, not just intellectually
interesting. Address the specific misconceptions practitioners
encounter from stakeholders, with the evidence that contradicts them.
Quantify wherever possible - decay rates, benchmarks, cost estimates,
industry averages.

Structure this as a front-to-back read that builds mental models
layer by layer. Call out common misconceptions. End with the
frameworks I should carry forward.
```

---

## Working With DR Output

The prompt is step one. How you work with DR after submitting the prompt matters just as much.

### Review the Research Plan

Both Claude and ChatGPT Deep Research show you a research plan before they start. Don't just click "Start" - read the plan, edit it if needed. Add competitor names, specific criteria, or topics you want prioritized. This is a free lever for improving output quality.

### The Self-Critique Loop

Ethan Mollick (Wharton) identifies this as one of the most effective techniques: after DR gives you an answer, ask it to critique its own response, identify gaps or weak points, then improve based on that critique. This produces stronger output than trying to write the perfect single prompt.

### Iterate, Don't Perfect

Mollick's finding that "having a conversation with the AI is 80% of making good prompts" is well-supported across sources. Your first prompt doesn't need to be perfect. Start with a solid structure, see what comes back, then refine through follow-up prompts to go deeper on specific threads.

### Verify Sources

All DR platforms still hallucinate. Anthropic, OpenAI, and Google all explicitly recommend verifying claims and citations yourself. Treat DR as a research partner, not an oracle.

### Delivering the Prompt

DR prompts are built to be pasted into external tools (Claude.ai, ChatGPT, Gemini). The delivery mechanism should minimize friction between generation and pasting:

- **Copy directly to clipboard** rather than displaying the full prompt in a terminal window where line breaks are unreliable and selecting text is awkward.
- **Show a brief summary** of what the prompt covers (topic, purpose type, sub-questions, word count) so the user knows what was built without reading the full text in terminal output.
- **Save a backup copy** to a known temp location in case the clipboard gets overwritten before pasting.
- **Show a macOS notification** confirming the prompt is ready, so the user can switch to their browser and paste immediately.

The goal: generation completes, the user switches to Claude.ai, hits Cmd+V, done.

---

## Question Transformation Method

How to go from "I want to understand X" to a structured prompt.

### Step 1: Identify the Purpose

**Am I building a reference doc or learning a domain?**

Reference doc signals: You'll come back to it multiple times. You need to look things up. It'll go into a knowledge base. It needs to compare options or platforms.

Learning signals: You're new to this topic. You need informed conversations about it. You want mental models, not just facts. You'll read it once and carry the understanding forward.

### Step 2: Set Your Context

Write 2-3 sentences: your professional role, what you already know about this topic, and why it matters to your work.

### Step 3: Decompose the Question

Break into 3-7 specific sub-questions. Ask: What are the distinct aspects? What decisions does this topic involve? What trade-offs exist? What am I most confused about?

If you can't decompose the question, that's fine - just use steps 1, 2, 4, and 5. DR will create its own structure.

### Step 4: Draw the Boundaries

Write 2-4 explicit exclusions. What adjacent topics will DR drift into? What do you already know well enough to skip? What's a separate research question for later?

### Step 5: Define Success & Output

What does "done" look like? Reference the appropriate output structure (Branch A or B). Add format-specific instructions.

---

## Before/After Examples

### Example 1: Domain Learning

**Before (casual question):**
> How do private equity fund sizes work?

**After (structured prompt):**
```
I'm a GTM data consultant who works with PE-backed B2B companies. I
encounter PE fund terminology constantly in prospect research -
"lower middle market fund," "growth equity," "$500M AUM" - but I don't
have a solid understanding of what these terms mean or how to interpret
them when evaluating a prospect's scale and sophistication.

I need to get up to speed so I can:
- Interpret fund size and type when researching prospects
- Understand what a PE firm's fund size implies about their portfolio
  companies' scale
- Speak credibly about PE structures in discovery calls

Start from first principles. Explain what a "fund" actually is before
getting into fund types and sizes. Build up from there.

What I need to understand:
- What AUM means and how it relates to actual investment capacity
- The taxonomy of fund sizes (mega, large, upper/lower middle market)
  and where the boundaries are
- How fund size connects to portfolio company characteristics
- The difference between fund size, deal size, and check size
- What "dry powder" means and why it matters

What I don't need:
- How to raise a fund or LP/GP mechanics beyond the basics
- Fund performance metrics (IRR, MOIC)
- Regulatory structure (SEC, exemptions)

Structure this for someone getting up to speed. Start with why this
matters, then build from foundational concepts to nuance. Use
analogies where helpful. Call out terminology that means different
things in different contexts. End with the mental models I should
carry forward when reading about PE firms.
```

### Example 2: Reference / Foundational Document

**Before (casual question):**
> How does record identity work in CRMs?

**After (structured prompt):**
```
I'm a GTM data consultant working with Series A through Series C B2B
companies. I build data pipelines, enrichment workflows, and CRM
infrastructure in HubSpot and Salesforce. I need a comprehensive
primer on how CRM record identity and uniqueness works - for both
company records and contact records. Cover both HubSpot and Salesforce
throughout - their mechanics differ and I need to understand both.

Start from first principles. Before getting into CRM-specific
mechanics, explain WHY record identity and uniqueness matters. What
problems does it solve? What goes wrong without it? Build up from
there so someone without a database background understands the "why"
before the "how."

What I need to understand:

For company records:
- What fields serve as unique identifiers (domain, company name,
  CRM-native IDs, LinkedIn company ID, etc.)
- When domain is the right uniqueness key vs. when it breaks down
  (subsidiaries, parent/child, holding companies)
- How HubSpot and Salesforce handle company deduplication natively

For contact records:
- What fields serve as unique identifiers (email, LinkedIn ID, phone,
  composite keys, CRM-native IDs)
- The fundamental trade-off between person-stable identifiers
  (LinkedIn - follows the person) and employment-stable identifiers
  (email - tied to the role/company)
- How this choice interacts with CRM architecture

The architectural questions I need answered:
- When to use single-record-per-person vs. multi-record-per-employment
- How enrichment pipelines (Clay, Apollo, ZoomInfo) interact with CRM
  uniqueness constraints
- What the deduplication workflow looks like in practice

Industry context:
- My clients are in private equity, capital markets, fintech, B2B SaaS
- Contact mobility is very high
- Company structures are complex (PE portfolio companies, subsidiaries)
- Typical CRM size: 10K-100K contacts, 2K-20K companies

What I don't need:
- Marketing automation or lead scoring
- GDPR/privacy compliance
- CRM selection advice

A complete answer covers the identity mechanics for both object types,
the architectural trade-offs, and enrichment pipeline interactions. If
it doesn't address those three dimensions, it's not done.

Structure this as a reference document I can use long-term. Use tables
for comparisons. Be specific about both HubSpot and Salesforce field
names, objects, and API behavior. Prioritize official documentation
and primary sources. Flag areas where the "right answer" depends on
context.
```

### Example 3: Quick Transformation

Not every prompt needs all building blocks. For simpler topics, purpose + context + first-principles + output format is enough. Research consistently shows that well-structured short prompts match or beat verbose ones.

**Before:**
> What's the deal with email deliverability?

**After:**
```
I'm a GTM consultant setting up cold email infrastructure for B2B
sales teams. I need to understand email deliverability from first
principles - not just "warm your domains" but why warming works, what
inbox providers are actually measuring, and how to reason about
deliverability problems when they arise.

Cover domain reputation, IP reputation, content signals, and sending
patterns. I don't need email marketing / newsletter deliverability -
this is purely cold outbound.

Structure this so I can read it front-to-back and come away with
strong mental models for diagnosing deliverability issues.
```

---

## Anti-Patterns

Common mistakes that produce mediocre DR output, with evidence for why they fail:

**"Tell me everything about X"** - No purpose, no boundaries, no context. DR produces a Wikipedia-style overview that's too broad to be useful. Every official guide (Anthropic, OpenAI, Google) lists this as the primary failure mode.

**Adding "think step by step"** - Deep Research runs on reasoning models that already reason internally. Wharton's GAIL research found that chain-of-thought instructions provide marginal improvement (2.9-3.1%) with 20-80% more processing time for reasoning models, and can actually increase error variability in non-reasoning models. Let the reasoning model think its own way.

**No context about who you are** - DR calibrates depth and technicality to the audience. Without context, it defaults to a general audience. David Hershey (Anthropic) describes the challenge: the model is "a brilliant but very new employee with amnesia who needs explicit instructions" about your situation.

**Over-constraining the research method** - OpenAI's DR researchers warn that "too many details or overly rigid instructions can limit creativity and reduce accuracy and depth." Specify what you need, not how DR should search for it. Anthropic's multi-agent system deliberately starts with broad queries and narrows - over-constraining fights this natural pattern.

**No exclusions** - DR fills available space. Without "what I don't need," it drifts into adjacent topics. This is especially important for topics that border multiple domains.

**No success criteria** - Without defining what "done" looks like, DR can't evaluate whether it's gone deep enough. "A complete answer covers X, Y, and Z" gives DR a target to aim for.

**Asking for both reference and learning simultaneously** - "Give me a comprehensive primer that's also a quick-reference document." These are different output structures with different reading flows. Pick one. You can always do a second DR pass for the other use case.

---

## Sources

### Official Platform Guidance

- [Using Research on Claude | Claude Help Center](https://support.claude.com/en/articles/11088861-using-research-on-claude)
- [Claude 4 Prompting Best Practices | Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [How We Built Our Multi-Agent Research System | Anthropic Engineering](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Effective Context Engineering for AI Agents | Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Best Practices for Prompt Engineering | Claude Blog](https://claude.com/blog/best-practices-for-prompt-engineering)
- [Highlights from the Claude 4 System Prompt | Simon Willison](https://simonwillison.net/2025/May/25/claude-4-system-prompt/)
- [OpenAI Deep Research FAQ](https://help.openai.com/en/articles/10500283-deep-research-faq)
- [Three Tips for Better AI-Assisted Inquiry | OpenAI Forum](https://forum.openai.com/public/blogs/exploring-deep-research-three-tips-for-better-ai-assisted-inquiry-2025-04-28)
- [GPT-5 Prompting Guide | OpenAI Cookbook](https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide)
- [Google Tips: How to Use Deep Research](https://blog.google/products/gemini/tips-how-to-use-deep-research/)
- [Perplexity Prompt Guide](https://docs.perplexity.ai/guides/prompt-guide)

### Anthropic Employee Advice

- David Hershey (Applied AI): [Fortune - 3 AI Prompts from Anthropic Engineers](https://fortune.com/2025/05/06/ai-prompt-tips-according-to-anthropic-experts-more-successful-at-work/)
- Zack Witten (Prompt Engineering): [Word.Studio - Explore Prompt Engineering with Anthropic](https://word.studio/explore-prompt-engineering-with-the-experts-from-anthropic/)
- Amanda Askell (Character Lead): [Startup Spells - Amanda Askell's Prompt Engineering Secrets](https://startupspells.com/p/amanda-askell-prompt-engineering-secrets)

### Academic Research

- Schulhoff et al., "The Prompt Report: A Systematic Survey of Prompt Engineering Techniques" - [arxiv 2406.06608](https://arxiv.org/abs/2406.06608) (reviewed 1,565 papers)
- Meincke, Mollick, Mollick, Shapiro, "The Decreasing Value of Chain of Thought in Prompting" - [Wharton GAIL](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/)
- STROT Framework: Structured Prompting and Feedback-Guided Reasoning - [arxiv 2505.01636](https://arxiv.org/html/2505.01636v1)

### Expert Practitioners

- Ethan Mollick: [Two Paths to Prompting](https://www.oneusefulthing.org/p/working-with-ai-two-paths-to-prompting) | [A Guide to Prompting AI](https://www.oneusefulthing.org/p/a-guide-to-prompting-ai-for-what)
- Aakash Gupta: [Prompt Engineering - What Actually Works (1,500+ papers)](https://www.news.aakashg.com/p/prompt-engineering)
- DreamHost: [We Tested 25 Claude Prompt Techniques: These 5 Actually Work](https://www.dreamhost.com/blog/claude-prompt-engineering/)

---

## Related Documents

- [Deep Research: GTM Assessment Prompt](deep-research-gtm-assessment.md) - Domain-specific DR prompt template (GTM assessment). Example of a fully developed prompt for a specific use case.
- AI Knowledge Document Standards (not included) - When DR output becomes a knowledge doc, use these standards for metadata and structure.
- [Filename Generation: Keyword Extraction and Retrieval Optimization](filename-generation-keyword-extraction-retrieval-optimization.md) - Naming conventions for documents created from DR output.
- Claude Projects Custom Instructions Best Practices (not included) - Related but different: instructions for Claude Projects, not DR prompts.
