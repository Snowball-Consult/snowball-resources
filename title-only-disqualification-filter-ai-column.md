# Title-Only Disqualification Filter (AI Column)

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

> **Companion piece:** [How this filter was built (A-Z walkthrough)](title-only-disqualification-filter-build-walkthrough.md) - the step-by-step story of going from a raw idea to a validated filter in one working session. Read that for the *process*; read this for the *artifact*.

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Specify a title-only AI screening column that removes obviously-wrong contacts from an enriched / keyword-sourced contact list, biased toward keeping (false exclusions are treated as worse than false passes). One binary `keep_contact` decision made from the job-title string alone. |
| **Trigger** | An automated contact-sourcing system is forwarding a meaningful share of obviously-wrong people, and you want a cheap, deterministic quality gate that catches the obvious garbage before it lands - without trying to be a full persona model. |
| **Scope** | The screening agent (system prompt, user prompt, output schema, variable, few-shot examples), the decision threshold (obvious non-fit vs ambiguous pass), the guards that prevent over-exclusion, the calibration approach. |
| **Not In Scope** | Bio-aware / full-profile classification (a heavier check that reads the whole enriched profile - not included), contact *selection* or ranking (this filter never selects), the upstream people-search recall filter, outbound messaging. |
| **Dependencies** | An ideal-buyer persona definition for the segment (not included); a per-record SME verdict log used as labeled training data (not included); a heavier profile-aware AI classifier this runs *in front of* (not included); a JSON prompting standard for AI agent columns (see the [Claygent JSON Prompting Guide](claygent-json-prompting-guide.md) in this repo). |
| **Keywords** | title-only filter, disqualification, exclusion filter, quality floor, AI column, keep/exclude, obvious non-fit, bias toward keep, asymmetric threshold, few-shot, enrichment QA |
| **Last Reviewed** | 2026-06-06 |

---

## The worked example (anonymized)

Throughout, the example is a B2B software vendor whose buyer is **the person at a private equity (PE) *sponsor* firm who handles capital markets / debt financing on deals** - often a "partial hat," so their title is frequently a bare VP / Principal / Director / MD / Partner with no functional label. The vendor's automated sourcing pulls contacts by keyword search and forwards many obviously-wrong people (admin, IT, lender-side credit roles, interns, fundraising staff). The filter below is the cheap floor that removes those.

The specifics (PE, capital markets, "sponsor vs lender") are the demo's worked example. The *method* transfers to any segment where you have (a) a persona, (b) some SME-labeled examples, and (c) an automated source that over-includes.

---

## What this filter is (and what it is not)

| It IS | It is NOT |
|---|---|
| A quality **floor** - removes obvious garbage | A selection mechanism - it never picks who is right |
| **Exclusion-only** - it only ever removes | A ranker or scorer - no scoring, no tiers |
| **Title-only** - its sole input is the job-title string | A profile reader - no bio, no company, no enrichment |
| **Asymmetric, biased to keep** - fires `"no"` only on obvious non-fits | Symmetric - it does not try to confirm fits |
| Tuned for one segment (here: PE sponsor side) | General across every adjacent segment |

**The whole game is the threshold.** The line this filter draws is between "the keyword search obviously returned the wrong human" (exclude) and "this could plausibly be the right person" (pass). Critically, it is drawn from **real NO-evidence** (what an SME actually rejected, plus the verbatim titles the system actually returned), **not** by inverting the persona definition. Inverting "ideal" would over-exclude the entire ambiguous middle this filter is built to pass - "obviously wrong" is a narrower, different input than "not ideal."

**It can only remove the bottom, not thin the middle.** Where the right person carries a bare title (e.g. a generalist VP whose debt-financing responsibility lives only in their bio), a title-only filter cannot do positive identification - and it does not try. It earns its keep by killing keyword false positives (an "FP&A Manager," an "Office Manager, Finance," a back-office or product role a search on "capital" / "finance" dragged in), not by judging the bare-title middle.

---

## Design decisions

1. **Title is the ONLY input.** No bio, no company, no enrichment. Deliberate - it's what makes the filter cheap and deterministic, and it's the point of difference from the heavier profile-aware check this runs in front of.
2. **Binary, not three-way.** Output is `"yes"` or `"no"` only. There is no `"unclear"` bucket - by design, doubt resolves to `"yes"`. A `"yes"` does **not** claim the person is a fit; it claims the title is *not obviously disqualifying*. The asymmetric rule (uncertain → keep) is explicit, so the binary output is a stated decision rule, not fabricated certainty.
3. **Bias to keep.** A false `"no"` (dropping a possible fit) is treated as worse than a false `"yes"` (passing a borderline title to the next reviewer).
4. **Guards against over-exclusion.** Some words that *look* disqualifying appear in the titles of confirmed fits. The prompt carries explicit guards so those titles pass (see "Known landmines" below).
5. **High-capability model → simple prompt.** Deployed on a strong model, so the prompt is principle-based + few-shot rather than exhaustively rule-enumerated.

---

## The threshold (what to exclude vs pass, title-only)

| **Output `"no"` (obvious non-fit on title alone)** | **Output `"yes"` (ambiguous or right - gravitate here)** |
|---|---|
| Lender-side credit function: Private Credit, Private Debt, Direct Lending, Credit (as the role), Debt Investments, Secondaries, Diversified Credit *(guard: passes if a capital-markets / financing word is also present)* | Bare seniority: VP, Vice President, Principal, Director, Managing Director, Partner, Managing Partner, SVP, **Associate, Analyst, AVP / Assistant Vice President** |
| Fundraising / LP distribution / enterprise sales: Institutional Capital Raising, Global Client Solutions, Capital Formation, LP Relations, Fund Marketing, Sales, Enterprise Sales, Sales Development, Customer Success *(guard: passes if Investor Relations / IR / capital-markets / investment signal present)* | Any core-function word: Capital Markets, DCM, Leveraged Finance, Financing, Debt Financing, Debt Advisory, Treasury |
| Back-office / non-investment: accounting, fund accounting, fund finance operations, financial management, audit, tax, compliance, legal, counsel, general counsel, HR / talent / recruiting, IT / technology, marketing / communications / PR / content, operations, facilities | Senior leadership: CEO, President, CFO, COO, CIO, Founder, Co-Founder, Managing Partner |
| Admin / support: Executive Assistant, Administrative Assistant, Office Manager, Receptionist, Coordinator | **Investor Relations / IR** on its own (the profile decides cross-asset vs sales; the title cannot) |
| Product / operating-side: Product Specialist / Development / Strategy, Head of Product; Operating Partner, Operating Advisor, Executive in Residence, Value Creation, Portfolio Operations | Business Development / BD |
| Retail / private wealth: Private Wealth, Wealth Solutions, Wealth Management, Retail | Bare strategy / sector roles with no disqualifying function |
| Below-threshold / non-operating: Intern, Summer Analyst/Associate, Incoming, Trainee; Non-Executive Director, Board Observer, board-only directorships | Anything you are not sure about |

**Geography is noise.** Region / language qualifiers (Benelux, EMEA, Continental Europe, Asia, North America) carry no screening signal. The model judges the functional core and ignores them.

---

## The prompt

The screening agent is a single AI column. Input variable: `{job_title}`. Web access: OFF (local data - the title string is the only input). Model: a high-capability tier.

### System prompt

```json
{
  "role": "You are a screening analyst for a software company that sells to private equity SPONSOR firms - PE firms that buy and own companies using equity. The product helps the people at those firms who arrange the DEBT FINANCING on their deals (capital markets, leveraged finance, debt financing work). You are given ONE thing: a person's job title, as a plain string. You see no bio, no company, no other context - only the title. From the title alone you make a binary screening decision: 'yes' (keep this contact) or 'no' (this title obviously belongs to someone the firm would not want to talk to). This is a coarse quality FLOOR that runs in front of a richer review. Your only job is to catch the obvious non-fits. You are deliberately biased toward 'yes': you output 'no' only when the title by itself makes it clear the person could not plausibly be a sponsor-side capital-markets or debt-financing buyer. A 'yes' does not claim the person IS a buyer - it only says the title is not obviously disqualifying. Anything you are unsure about gets 'yes'.",
  "constraints": [
    "Your ONLY input is the job title string. Do not assume or invent a company, seniority, bio, or any context the title does not state. Judge the title exactly as written.",
    "Default to 'yes'. Output 'no' ONLY when the title is an obvious non-fit on its face. If a title is bare, generic, or ambiguous, output 'yes'. Dropping a possible buyer (a false 'no') is worse than passing a borderline title to the next reviewer (a false 'yes').",
    "The right buyer's title is usually unremarkable. At most sponsor firms - especially smaller ones - the person who handles debt financing does it as a partial responsibility and carries a plain seniority title with no functional label. So bare seniority titles ALWAYS pass, on their own, every time: Vice President, VP, Principal, Director, Managing Director, MD, Partner, Managing Partner, Senior Vice President, SVP, Associate, Senior Associate, Analyst, Assistant Vice President, AVP.",
    "Do not screen out senior leaders. CEO, President, CFO, COO, Chief Investment Officer (CIO), Founder, Co-Founder, and Managing Partner all pass - senior people at a sponsor firm can be buyers.",
    "Capital-markets and debt-financing titles are the core target and always pass: Capital Markets, Debt Capital Markets, DCM, Leveraged Finance, LevFin, Financing, Debt Financing, Debt Advisory, Treasury. If any of these appear, output 'yes' even if a lender-side or fundraising word is also present.",
    "LENDER-SIDE CREDIT FUNCTIONS ARE THE WRONG SIDE. The firms we sell to are sponsors (equity buyers), not lenders. A title whose function is lending or credit is an obvious non-fit: Private Credit, Private Debt, Direct Lending, Credit as the role's function (for example Head of Credit, Credit Investments, Diversified Credit), Debt Investments, Secondaries, Special Situations lending. Output 'no' for these. GUARD: if the same title ALSO contains a capital-markets or financing word (Capital Markets, DCM, Leveraged Finance, Financing, Debt Capital Markets), output 'yes' instead - that is the sponsor-side capital-markets person, not a lender.",
    "FUNDRAISING, LP-DISTRIBUTION, AND ENTERPRISE-SALES ROLES ARE THE WRONG JOB. These people sell the fund to investors; they do not arrange deal financing. Obvious non-fits: Institutional Capital Raising, Capital Raising as the role's function, Global Client Solutions, Client Solutions, Capital Formation as the role's function, LP Relations, Limited Partner Relations, Fund Marketing, Sales, Enterprise Sales, Sales Development, Customer Success. Output 'no'. GUARD: Investor Relations or IR on its own PASSES - some IR people cover deal-side work and the title alone cannot tell which, so never screen out a plain IR title. Only output 'no' when the title is clearly pure fundraising or distribution with NO Investor Relations, capital-markets, financing, or private-equity-investment signal in it.",
    "NON-INVESTMENT AND BACK-OFFICE FUNCTIONS ARE OUT. Output 'no' for titles whose function is accounting, fund accounting, fund finance operations, financial management, financial controller, audit, tax, compliance, legal, counsel, general counsel, human resources, HR, people, talent, recruiting, IT, technology, engineering, marketing, communications, PR, content, design, facilities, operations as a back-office function, or administration. Also output 'no' for support and admin titles: Executive Assistant, Administrative Assistant, Office Manager, Receptionist, Coordinator.",
    "PRODUCT AND OPERATING-SIDE ROLES ARE OUT. Output 'no' for Product Specialist, Product Development, Product Strategy, Head of Product, Product Manager; and for operating roles that sit at the owned companies rather than the PE firm: Operating Partner, Operating Advisor, Executive in Residence, EIR, Value Creation, Portfolio Operations.",
    "RETAIL AND PRIVATE WEALTH IS OUT. Output 'no' for Private Wealth, Wealth Solutions, Wealth Management, Retail - this is individual-investor wealth management, not institutional private equity.",
    "BELOW-THRESHOLD AND NON-OPERATING ROLES ARE OUT. Output 'no' for interns and pre-hires (Intern, Summer Analyst, Summer Associate, Incoming, Trainee, Apprentice) and for board-only roles (Non-Executive Director, Board Observer, a board-only directorship with no operating or investment function). Note: Associate and Analyst are NOT below threshold - they pass.",
    "Ignore geography, region, and language qualifiers in the title (for example Benelux, EMEA, Continental Europe, Asia, North America, US, UK). They carry no screening signal. Judge the functional core of the title. Translate non-English titles before judging.",
    "Output exactly one value: 'yes' or 'no'. Nothing else."
  ],
  "examples": [
    {"job_title": "Vice President, Capital Markets", "keep_contact": "yes"},
    {"job_title": "Principal - Financing", "keep_contact": "yes"},
    {"job_title": "Partner - Financing", "keep_contact": "yes"},
    {"job_title": "Head of Capital Markets", "keep_contact": "yes"},
    {"job_title": "Managing Director", "keep_contact": "yes"},
    {"job_title": "Vice President", "keep_contact": "yes"},
    {"job_title": "Principal", "keep_contact": "yes"},
    {"job_title": "Managing Partner", "keep_contact": "yes"},
    {"job_title": "Assistant Vice President", "keep_contact": "yes"},
    {"job_title": "Chief Investment Officer", "keep_contact": "yes"},
    {"job_title": "Director, Capital Raising & Investor Relations – Global Client Solutions | Capital Formation", "keep_contact": "yes"},
    {"job_title": "Investment Director - Financing", "keep_contact": "yes"},
    {"job_title": "Vice President, CLO Capital Markets & Structuring", "keep_contact": "yes"},
    {"job_title": "Director, Business Development", "keep_contact": "yes"},
    {"job_title": "Co-Head of Private Credit, Managing Director", "keep_contact": "no"},
    {"job_title": "Managing Director, Direct Lending", "keep_contact": "no"},
    {"job_title": "Private Credit", "keep_contact": "no"},
    {"job_title": "Principal - Credit Secondaries", "keep_contact": "no"},
    {"job_title": "Investment Director - Debt Investments", "keep_contact": "no"},
    {"job_title": "Assistant Vice President, Private Credit Benelux", "keep_contact": "no"},
    {"job_title": "Associate Director, Global Client Solutions", "keep_contact": "no"},
    {"job_title": "Principal - Leading Institutional Capital Raising in Continental Europe", "keep_contact": "no"},
    {"job_title": "Vice President, Private Wealth Solutions", "keep_contact": "no"},
    {"job_title": "Senior Associate, Digital Content Manager", "keep_contact": "no"},
    {"job_title": "Director, Product Development", "keep_contact": "no"},
    {"job_title": "Senior Private Credit Operations Analyst", "keep_contact": "no"},
    {"job_title": "Operating Partner", "keep_contact": "no"},
    {"job_title": "Executive Assistant", "keep_contact": "no"},
    {"job_title": "Private Credit Summer Intern", "keep_contact": "no"},
    {"job_title": "Non-Executive Director", "keep_contact": "no"}
  ]
}
```

### User prompt

```json
{
  "goal": "Decide, from the job title alone, whether to keep this contact ('yes') or screen them out as an obvious non-fit ('no'). Default to 'yes'; output 'no' only when the title by itself clearly belongs to someone a PE sponsor firm's debt-financing buyer would not be.",
  "task_steps_to_perform": [
    "1. Read {job_title}. Strip out geography, region, and language qualifiers. Identify the FUNCTIONAL core of the title - the kind of work it names - separate from its seniority.",
    "2. If the title is bare seniority with no function (Vice President, Principal, Director, Managing Director, Partner, Managing Partner, Associate, Analyst, AVP), OR names capital-markets / debt-financing / treasury work, OR is a senior leadership role (CEO, CFO, COO, CIO, Founder, Managing Partner): output 'yes'.",
    "3. Otherwise check whether the functional core is an obvious non-fit: lender-side credit (Private Credit, Private Debt, Direct Lending, Credit, Debt Investments, Secondaries, Diversified Credit); fundraising / LP-distribution / enterprise-sales (Institutional Capital Raising, Global Client Solutions, Capital Formation, LP Relations, Sales, Customer Success); back-office / non-investment (accounting, audit, tax, compliance, legal, HR, IT, marketing, communications, operations, admin / EA); product or operating-side (Product, Operating Partner, EIR, Value Creation, Portfolio Operations); retail / private wealth; intern / pre-hire; or board-only. If so, lean 'no'.",
    "4. Apply the guards before finalizing 'no'. If the title also contains a capital-markets or financing word, output 'yes'. If the title contains Investor Relations / IR or a private-equity-investment signal, do not treat it as fundraising - output 'yes'.",
    "5. If after all of the above you are still unsure, output 'yes'. Return exactly one value: 'yes' or 'no'."
  ]
}
```

### Output schema

```json
{
  "type": "object",
  "properties": {
    "keep_contact": {
      "type": "string",
      "enum": ["yes", "no"],
      "description": "yes = keep (default); no = obvious non-fit, screen out."
    }
  },
  "required": ["keep_contact"]
}
```

### Variable

```
{job_title}: variable
```

Bind `{job_title}` to the job-title column. Bind nothing else - this filter sees only the title. Downstream: remove / quarantine rows where `keep_contact = "no"`; everything `"yes"` flows on to the heavier profile-aware check or to human review.

---

## Calibration basis (build it from NO-evidence, not from the persona)

The exclusion categories and few-shot examples are drawn from real evidence, not invented:

- **An SME's per-record verdicts.** A subject-matter expert had hand-classified a batch of candidate contacts as fit / not-fit with written reasoning. Every "not-fit" is a labeled non-fit example. In this case one signal (lender-side credit titles) accounted for the large majority of the rejections with zero collisions against the confirmed fits - the single most predictive exclusion.
- **The verbatim titles the system actually returned.** The few-shot examples use real title strings from the live keyword-sourced output, so the model is calibrated on what the source actually produces, not on hypotheticals.
- **A title-only re-projection of the SME verdicts.** This is the subtle, important step. The SME judged on title **+ bio + segment**, so their verdicts are NOT usable as title-only labels directly. The bare title "Principal" was a fit for one person, a non-fit for another, and a non-fit for a third - all decided by the *bio*. So the few-shot labels are the answer to a *different* question: "given only this string, is it *obviously* wrong?" Bio-dependent cases get relabeled to "pass."

---

## Known landmines the few-shots are designed to defuse

| Landmine | Why it is dangerous | How the prompt handles it |
|---|---|---|
| A confirmed fit whose title reads like a disqualified role | One confirmed-fit contact's verbatim title contained "Capital Raising," "Global Client Solutions," AND "Capital Formation" - three tokens that look like pure fundraising/distribution | Paired few-shots: that title → keep (an Investor-Relations / capital-formation signal is present); a *pure* "Associate Director, Global Client Solutions" → exclude. The difference is the buyer signal, enforced by the fundraising guard. |
| Bare seniority titles | The SME rejected specific "Principal" / "AVP" people using their *bios*; importing those as title-only labels would teach the filter to kill the ambiguous middle | Bare seniority titles (incl. AVP) are explicit always-pass; a title is only excluded for a *functional* reason, never for bare seniority. |
| A core-function person at an off-segment-flavored firm | "VP, CLO Capital Markets & Structuring" reads credit-side but carries "Capital Markets" | The capital-markets guard overrides the lender-side lean → keep. |

---

## How it tested

Re-projecting the SME's verdicts through the title-only lens and comparing:

| Measure | Result | Why it matters |
|---|---|---|
| Agreement with the SME (on verdicted contacts) | ~79% | strong for title-only |
| **Over-exclusion of confirmed fits** | **0%** | the failure mode that would actually hurt never happened |
| Disagreements | all conservative passes | every one is a bio-driven rejection whose *title* is bare and correctly passes to the next reviewer |

On the live tail (the contacts the system returned that the SME never reviewed), the filter excluded roughly half, and about three-quarters of those excludes were the single highest-value category (here: lender-side credit titles). Without that one rule, the filter would have caught only a small fraction of the bad tail - proof of where a title-only floor does and doesn't earn its keep.

---

## The honest caveat (ship the filter with it)

A title-only exclusion filter is a cheap, reversible, low-risk clean-up gate. Build it. But it is a precision improvement on a *selection axis* that the evidence sometimes questions. In this engagement, the replies came disproportionately from a **relationship** axis (shared connection, prior-employer overlap, shared school) rather than from a title match - the one reply in a sampled batch came from an off-persona contact a title/persona search would never have surfaced. So this filter is correctly scoped as a modest floor on auto-sourced contacts, not as the answer to sourcing quality. The fix for *quality* is sourcing on relationship signals; this just stops obvious garbage from riding along. Don't oversell it.

---

## Transferable principles

1. **Build the disqualifier from NO-evidence, not by inverting the persona.** "Obviously wrong" is a narrower input than "not ideal," and inverting the persona over-excludes the ambiguous middle.
2. **Make the threshold asymmetric and say so.** Decide which error is worse (here, false exclusion) and encode "when in doubt, keep" as an explicit rule. A binary output then isn't fabricated certainty - it's a stated decision rule.
3. **SME labels are not always the labels you need.** If the SME judged on more than your input carries, re-project their verdicts onto your actual input before few-shotting. Otherwise you import judgments your model can't reproduce and over-reach.
4. **Find the landmines before you ship.** Look for confirmed *fits* whose surface features look disqualifying. Each one becomes a guard and a paired few-shot.
5. **Strong model → simple prompt.** Principle-based instructions plus a tight, evidence-grounded few-shot set beat exhaustive rule enumeration when the model is capable.
6. **Validate on labeled data, and report the error that matters.** Don't just report accuracy; report the asymmetric error you care about (here: over-exclusion of confirmed fits = 0%).
