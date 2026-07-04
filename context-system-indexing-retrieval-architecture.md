# Anatomy of a Context System: The Indexing Layer

> **Demo resource.** This describes the indexing layer of a working context system - the structured library of methodology, reference, and domain knowledge that an AI agent draws on to do real work. It is shared as inspiration. The specific codes and category names are conventions, not requirements. Steal the shape, not the labels.

An agent is only as good as the context it can reach at the moment it needs it. A pile of well-written documents is worthless if the agent never finds the right one. So the interesting engineering in a context system is not the documents. It is the **index**: the set of conventions and lookup steps that let an agent locate the single relevant document, out of hundreds, while spending almost no budget to do it.

This document explains how that index is built and how retrieval actually runs against it.

---

## The problem the index solves

Two failure modes kill a context system, and they pull in opposite directions:

1. **A document is found but not understood.** The agent retrieves it, but the content is ambiguous, unlabelled, or stale, so it can't be applied correctly.
2. **A document is understood but never found.** The content is perfect, but nothing in how it's named or indexed overlaps with the way the request was phrased, so it stays invisible.

The index has to solve both at once. Naming and metadata solve *findability*. Structure and maturity signals solve *interpretability*. A system that optimizes only one of the two will quietly fail on the other.

A third constraint sits on top: **every lookup costs context budget.** Reading the full index into the agent's working memory on every request is the naive solution, and it does not scale. Past a few dozen documents, the index itself is too big to load. So retrieval has to be *tiered*: try the cheap lookups first, and only escalate to expensive ones when the cheap ones miss.

Those three pressures - findability, interpretability, and cost - shape every element below.

---

## The constituent elements

The index is not one file. It is a set of cooperating conventions, each carrying part of the load.

### 1. The corpus: one fact per document

The library is a flat collection of markdown documents. The discipline that matters: **one document holds one coherent thing** - a methodology, a schema, a reference, a persona. Documents do not sprawl across topics, because a document about five things is findable for none of them and editable without breaking four others.

Markdown because it is plain text: diffable in version control, readable by humans, and parsed natively by every model.

### 2. A stable document code

Every document gets a permanent identifier, for example `DOC-1`, `REF-12`. The code never changes even when the file is renamed or the content is rewritten. This gives you a stable handle for cross-references: one document can point to another by code, and the link survives edits.

Codes also carry a **layer** distinction. Knowledge about *how you work* (methodology, procedures, standards) is kept separate from knowledge about *a domain* (industry structure, buyer types, market facts). The first is universal across engagements; the second is reusable only within its vertical. Deciding the layer before assigning a code keeps the two from contaminating each other.

### 3. The filename as a searchable record

This is the highest-leverage convention in the whole system. The filename is not a label. It is a **retrieval record**:

```
[document-code]_[CATEGORY]_[keyword-dense-descriptive-name].md
```

Example shape:

```
ref-12_PROCEDURE_client-onboarding-tech-stack-audit-stakeholder-access.md
```

Every word in that name is a retrieval hook. The discipline is **query anticipation**: before naming a file, predict the phrases someone would use to look for it, including synonyms, and pack as many of those terms into the name as the character budget allows. A file named `notes.md` is invisible. A file whose name overlaps the way requests are actually phrased gets found on the cheapest possible lookup - a filename glob - before any expensive step runs.

The principle generalizes to any retrieval system: the filename controls discovery, the content controls execution, and most files fail at discovery.

### 4. A category taxonomy

The `CATEGORY` segment of the filename classifies the document by *what kind of thing it is*, independent of topic. A small fixed vocabulary, for example:

| Category | What it holds |
|----------|---------------|
| `REFERENCE` | Stable factual lookup material |
| `SCHEMA` | Data structures, field definitions, JSON shapes |
| `FRAMEWORK` | Conceptual models and ways of thinking |
| `PROCEDURE` | Step-by-step how-to |
| `STANDARD` | Rules and conventions to follow |
| `PROFILE` / `PERSONA` | Descriptions of entities or buyer types |
| `TEMPLATE` | Reusable scaffolds |

The category is doing two jobs: it is a second retrieval filter (find me the *procedure* about onboarding, not the framework), and it sets expectations about how to read the document before it is opened.

### 5. Front-loaded metadata

The first ~20 lines of every document are a metadata block, so the agent can confirm relevance by reading a fraction of the file instead of the whole thing:

| Field | Job |
|-------|-----|
| **Purpose** | One line: what this document is for |
| **Trigger** | When to reach for it |
| **Scope** / **Not In Scope** | Boundaries, so adjacent documents don't get confused |
| **Dependencies** | What else this relies on |
| **Keywords** | Synonym surface for retrieval beyond the filename |
| **Maturity** | Reliability signal (see below) |
| **Last Reviewed** | Staleness signal |

Front-loading is a cost optimization. The agent reads the top of a candidate file, confirms it's the right one, and only then commits to the full read.

### 6. Maturity status

Not all knowledge is equally trustworthy, and the index says so explicitly. Each document carries a maturity level:

| Status | Meaning | How to use it |
|--------|---------|---------------|
| **Draft** | Early exploration | Reference with caveats |
| **Working** | Substantive but unvalidated | Current best thinking, open to contradiction |
| **Stable** | Validated through use | Prefer over general knowledge |
| **Canonical** | Authoritative, locked in | Treat as definitive, override general knowledge |
| **Obsolete** | Superseded | Do not use, kept for history |

This matters because an agent's default behavior is to treat everything it reads as equally authoritative. The maturity field lets a document say "I am the definitive answer, override your prior" or "I am a rough sketch, hold this loosely." Paired with a `Last Reviewed` date, it also surfaces staleness: a once-canonical document untouched for a year gets flagged when referenced.

### 7. The manifest: the index of record

A single manifest file lists every document with its code, filename, category, maturity, last-reviewed date, purpose, and keywords - one row each. It is the comprehensive, authoritative index.

It is also expensive to load, because it grows with the library. So the manifest is deliberately the **fallback**, not the first stop. Cheaper lookups (below) handle most requests; the manifest is read only when they miss. The source of truth for any field is always the document's own metadata - the manifest mirrors it for fast scanning.

### 8. The topic router: a synonym bridge

Filename keywords only work when the request uses words that overlap them. Real requests use casual language. Someone asks "is this person still at the company" when the relevant document is named with `employment`, `in-seat`, `job-change`. The router closes that gap:

```
User says:  "still there", "moved on", "left the company", "job change"
Maps to:    employment, in-seat, moved-on, contact-data-pipeline
```

It is a small, cheap-to-load translation table from how people talk to how files are named. When a glob on the literal request words returns nothing, the router translates the intent into the right keywords and the glob is retried.

### 9. The people directory: instant entity resolution

A tiny table mapping every named person to their organization and role, loaded on **every** session because it is small and constantly useful. When a request names a person, the agent resolves who they are and which engagement they belong to instantly, without any document lookup at all. This is the cheapest retrieval step in the system, which is why it runs first.

---

## The retrieval protocol: cheapest first

The elements above are inert without the algorithm that runs against them. This is the part that ties the system together, and it is the part most "just dump everything in a folder" approaches are missing.

Retrieval is a **tiered cascade**. Each step is more expensive than the last in context budget, so the agent stops at the first step that answers the request:

```
1. People directory        already in memory      ~free
2. Trigger phrases / skills direct workflow match  ~free
3. Filename glob           match request keywords  near-free
4. Topic router            translate, then glob    cheap
5. Front-loaded metadata   read top ~20 lines      cheap
6. Manifest search         scan the full index     expensive
7. Full-text grep          search inside contents  last resort
```

The logic:

- **Steps 1-2** cost nothing because that context is already loaded or is a direct trigger match. Most person-references and named-workflow requests resolve here.
- **Step 3** is the workhorse. Because filenames are engineered as keyword records, a glob on the request's nouns usually surfaces the right candidate immediately.
- **Step 4** catches the cases where casual phrasing missed the filename keywords - translate through the router, glob again.
- **Step 5** confirms a candidate cheaply by reading only its metadata header before committing to the full document.
- **Steps 6-7** are the safety net. They always work, but they are expensive, so they run only when everything above has failed.

The whole design is an exercise in **spending the least context to find the right knowledge.** A good index is measured not only by whether the right document can be found, but by how cheaply.

---

## Why it's built this way

A few principles fall out of the structure:

- **The filename does the heavy lifting.** More retrieval value sits in naming conventions than in any search tooling. Get naming right and most lookups never reach the expensive tiers.
- **The cheap path is the common path.** The system is tuned so the overwhelming majority of requests resolve in the first three steps. Expensive lookups exist, but they are the exception.
- **Trust is explicit, not assumed.** Maturity and staleness signals stop the agent from treating a draft as gospel or citing year-old material as current.
- **One fact per file.** Keeps documents findable, editable, and cross-referenceable without collateral damage.
- **The index is maintained as a first-class artifact.** When a document is added, renamed, or re-graded, the manifest, the router, and any cross-references are updated in the same pass. An index that drifts out of sync with the corpus quietly rots, and a rotted index is worse than none, because it is trusted.

---

## The point

Models will keep getting better at *doing things*. What they cannot supply on their own is the judgement of what good looks like for a specific business - the accumulated point of view that turns a capable agent into a useful one. That judgement lives in the context system. The indexing layer is what makes it retrievable at the moment of decision, cheaply enough to use on every request.

That is why a context system is infrastructure, not a folder of notes. The documents are the knowledge. The index is what makes the knowledge *operational*.

---

*From [Snowball Consult](https://snowball-consult.com), a GTM data infrastructure consultancy. Questions: andreas@snowball-consult.com*
