# How a Title-Only Disqualification Filter Gets Built (A-Z)

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

> **Companion piece:** [The filter itself (spec + prompt)](title-only-disqualification-filter-ai-column.md). This document is the *story of how it was built* in a single working session - the reasoning, the pushback, the dead-ends-avoided, and the validation. If you want the artifact, read the companion. If you want to see how the sausage is made, you're in the right place.

---

This is a real example of building a small, sharp AI tool from real data in one session. The point isn't the filter - it's the *process*. The same arc works for almost any "screen the obvious junk out of an automated list" problem.

The worked example (anonymized): a B2B software vendor whose buyer is the person at a **private equity sponsor firm** who handles **capital markets / debt financing** on deals. An automated sourcing system pulls candidate contacts by keyword search and forwards a lot of obviously-wrong people. The ask: a cheap gate that catches the obvious garbage.

---

## A. The trigger: a clear, modest pain

The client had already built an automated contact-sourcing ("hydration") system because it was a clear ask. It worked - and it forwarded a meaningful share of contacts that were, in the client's words, "very clearly not the right persona." Office managers. IT staff. Lender-side credit people. Interns. Fundraising staff. The keyword search was doing what keyword searches do: matching strings, not judgment.

The ask was deliberately **modest**: not "build the world's best persona model," just "catch the obvious garbage before it lands." A floor, not a brain.

**Lesson:** name the smallest version of the problem first. "Catch the obvious wrongs" is a different, far cheaper project than "decide who's right." Don't let the second one smuggle itself into the first.

---

## B. The brief: lock the design constraints before touching anything

Before any building, the design was pinned down with the stakeholder:

- **Title-only.** The filter reads the job title and nothing else - no profile, no company, no enrichment. That's what makes it cheap and deterministic.
- **Exclusion-only.** It only ever removes. It never selects, ranks, or scores. Selection is someone else's job.
- **Asymmetric, biased toward keeping.** It fires "exclude" only when a title is *obviously* wrong. Anything ambiguous passes. A false exclusion (killing a possibly-good contact) is treated as worse than a false pass.
- **Binary.** Yes or no. No "unclear" bucket - by rule, doubt resolves to "keep."
- **One segment.** Optimize for the segment the source actually targets (here, PE sponsors, especially smaller ones), not for every adjacent segment.

**Lesson:** these aren't implementation details - they're the whole design. Decide them explicitly and write them down. "Which error is worse" in particular shapes everything downstream.

---

## C. Don't start from zero: harvest the labeled evidence you already have

The filter is not a greenfield model. Two sources of real evidence existed:

1. **An SME's per-record verdicts.** A subject-matter expert had previously sat down and hand-classified a batch of candidate contacts as fit / not-fit, with written reasoning for each. Every "not-fit" is a labeled training example - a known-wrong contact with a known reason.
2. **The verbatim titles the system actually returned.** The real output of the keyword search - the exact title strings, including the junk. This is what the filter will actually see in production.

So before writing a word of prompt, the work was: read the persona definition, read every SME verdict and its reasoning, and pull the real titles the system forwarded.

**Lesson:** most "build me a classifier" problems already have labeled data lying around - a sales rep's rejections, a CRM field someone maintained by hand, a spreadsheet of past decisions. Find it first. It's both your few-shot set and your test set.

---

## D. The subtle, critical insight: SME labels are not always the labels you need

Here's the step that separates a good filter from a broken one.

The SME judged each contact on **title + bio + company + segment**. But this filter only sees the **title**. Those are different inputs - so the SME's verdicts can't be copied over as title-only labels.

The proof was right there in the data: the bare title **"Principal"** appeared three times. The SME called one a fit, and two non-fits - and every one of those calls was decided by the **bio** (one bio said capital markets → fit; another said private credit → not-fit; another said sales → not-fit). The *title* "Principal" is identical across all three.

If you naively few-shot "Principal → exclude" off one of those non-fits, you teach the filter to kill every bare "Principal" - which, at smaller firms, is exactly the right person. That's the over-reach the whole design is trying to avoid.

So the SME verdicts had to be **re-projected** onto the title-only question: *"given only this string, is it obviously wrong?"* The clean cases (a title that says "Private Credit," "Secondaries," "Fund Accounting," "Executive Assistant") survive the projection. The bio-dependent cases (bare "Principal," a cross-asset Investor Relations title, an "ESG" title) get relabeled to **pass**.

**Lesson:** before you reuse someone's labels, check what they were looking at. If they judged on more than your model will see, re-project their decisions onto your actual input - or you'll import judgments your model can't reproduce, and it'll over-reach with confidence.

---

## E. Critique the stakeholder's first instincts (politely, with evidence)

The stakeholder offered some quick examples of what to exclude. Most were spot-on. One wasn't - and catching it mattered.

> "Investor Relations - rather not, exclude those."

The evidence pushed back. The single most valuable confirmed *fit* in the dataset was an **Investor Relations** title - the SME had flipped it to "fit" because the bio showed the person covered deal-side work across asset classes. And the SME's own finding was explicit: IR splits two ways (deal-side IR = fit; pure fundraising IR = not-fit), **and the title alone cannot tell them apart.** So "exclude all IR" would kill a known fit and violate the filter's own "only exclude the obvious" rule - IR is ambiguous, not obvious.

The resolution: **IR passes.** The ambiguous middle is exactly what this filter is supposed to let through.

There was also a **landmine** worth surfacing: that confirmed-fit IR contact's verbatim title contained "Capital Raising," "Global Client Solutions," *and* "Capital Formation" - three phrases that look like pure fundraising and would naively be on any exclude list. A flat keyword exclude would have killed a known fit. That became a deliberate guard in the prompt.

**Lesson:** your client's gut is usually right, but "usually" is the dangerous word. When the labeled data contradicts an instinct, say so - with the specific example. The exceptions are where the filter gets its precision (or loses it).

---

## F. Lock the decisions

With the critique done, the forks resolved cleanly:

- **Investor Relations passes** (ambiguous on title alone; the heavier check decides).
- **Lender-side credit tokens** (Private Credit, Private Debt, Direct Lending, Secondaries, Diversified Credit) **are excluded** - the most predictive non-fit signal in the data, with zero collisions against confirmed fits - **but with a guard**: if the title *also* carries a capital-markets / financing word, it passes (that's the right person on the wrong-looking title). This rule is only safe because the source is pre-filtered to the right segment.
- **High-capability model**, so the prompt stays principle-based + few-shot rather than an exhaustive rulebook.

**Lesson:** present the genuine forks as decisions, with a recommendation and the tradeoff, and let the owner decide. Don't silently bake in the risky call.

---

## G. Build the prompt: principles + a tight, evidence-grounded few-shot set

The filter is one AI column: a job title in, a binary keep/exclude out. The prompt has four parts - a system prompt (the role + the principles, organized by exclusion category, each with its guard), a user prompt (the decision steps), a minimal output schema (a two-value enum), and the few-shot examples.

The few-shots are the highest-leverage part. They're drawn from **real titles** the system returned, and they're chosen to teach the *guards*, not just the easy cases. The most valuable ones are paired opposites:

- the confirmed-fit IR title (with all its fundraising-looking words) → **keep**, vs a *pure* "Global Client Solutions" title → **exclude**. This teaches the buyer-signal guard.
- a bare "Principal" → **keep**, vs "Principal - Leading Institutional Capital Raising" → **exclude**. This teaches that seniority alone never disqualifies; the *function* does.
- a credit-flavored "Capital Markets & Structuring" title → **keep**. This teaches the capital-markets guard overriding the lender-side lean.

**Lesson:** spend your few-shot budget on the boundary, not the obvious. The examples that earn their place are the ones that look like they should go one way and actually go the other.

---

## H. Validate against the labeled data - and report the error that matters

The filter was run (on paper) against the SME's verdicts, re-projected to title-only:

- **~79% agreement** with the SME on the verdicted contacts.
- **0% over-exclusion of confirmed fits** - the failure mode that actually hurts never happened.
- **Every disagreement was a conservative pass** - a contact the SME rejected on *bio* grounds whose *title* is bare, correctly passed along to the next reviewer instead of being killed.

That second number is the one that matters. For a keep-biased floor, "how often did it wrongly kill a known-good contact?" is the real test - not raw accuracy. Zero is the target, and it hit zero.

On the live tail (contacts the system returned that the SME never reviewed), the filter excluded about half - and about three-quarters of those excludes were the single highest-value category. Without that one rule, the filter would have caught only a sliver of the junk. That quantifies exactly where a title-only floor does and doesn't earn its keep.

**Lesson:** pick the metric that maps to your asymmetric design choice and lead with it. "Accuracy" hides the error you actually care about.

---

## I. Ship it with its caveat

A title-only exclusion filter is cheap, reversible, and low-risk. Worth building. But it's a precision tweak on a *selection axis* the evidence sometimes questions: in this engagement, the replies came disproportionately from a **relationship** axis (shared connection, prior-employer overlap, shared school), not from a title match - the one reply in a sampled batch came from an off-persona contact a title search would never surface.

So the filter ships scoped honestly: a modest floor that stops obvious garbage from riding along, **not** the fix for sourcing quality. The fix for quality is sourcing on relationship signals; this is hygiene on top of whatever the automation pulled.

**Lesson:** ship the tool with the frame. The most useful thing you can hand a client is the honest scope - "this does X, it does not do Y, and here's the evidence for both."

---

## The whole arc, in one line each

1. **Trigger** - name the smallest version of the problem (catch obvious wrongs ≠ decide who's right).
2. **Brief** - lock the design constraints, especially *which error is worse*.
3. **Evidence** - harvest the labeled data you already have; it's your few-shots and your test set.
4. **Re-projection** - the SME's labels were made on more than your input carries; re-project them or you'll over-reach.
5. **Critique** - push back on instincts the data contradicts; the exceptions are where precision lives.
6. **Decisions** - present the real forks with a recommendation; don't bake in the risky one silently.
7. **Build** - principles + a few-shot set that teaches the *boundaries* and *guards*, on real examples.
8. **Validate** - report the asymmetric error that matters (here, over-exclusion of confirmed fits = 0%).
9. **Ship with the caveat** - the honest scope is part of the deliverable.
