# CRM Company Record Selection Agent: Domain Lookup Parent-Child Disambiguation

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Agent specification for a Claygent that selects the correct CRM company record when a domain lookup returns multiple results (parent companies, subsidiaries, business units sharing a domain) |
| **Trigger** | Building champion tracking workflows where CRM domain lookups return multiple company records, resolving parent-child company hierarchies for contact association, post-primary-role-identification CRM record matching |
| **Scope** | Five raw inputs (person enrichment, company enrichment, dual CRM lookups, upstream agent output), merge/dedup, upstream agent validation, three-tier selection logic (name match, title context match, activity-based fallback), ParentCo elimination, shell record filtering, numeric scoring fallback, unambiguous/needs-review determination, output schema (7 fields), test cases with real CRM data patterns, implementation notes |
| **Not In Scope** | Primary role identification (not included), employment verification (not included), CRM record creation or merging, company hierarchy management in HubSpot, deduplication strategy (not included) |
| **Dependencies** | AI agent prompt building guide - system/user split (not included), Primary role identification agent - upstream agent providing domain + contact context (not included), Clay enriched company structure (not included), Claygent deep dive (not included), Clay AI formula generator - extraction formulas for input columns (not included) |
| **Keywords** | CRM company record, company selection, domain lookup, parent company, subsidiary, child company, company_segment, ParentCo, Sponsor, Lender, business unit, champion tracking, record disambiguation, HubSpot, company hierarchy, activity signals, name matching, Claygent, Clay, contact association |
| **Maturity** | Working |
| **Last Reviewed** | 2026-03-18 |

---

## Overview

When a champion tracking workflow identifies that a contact has moved to a new company and resolves their primary role domain (via an upstream primary role identification agent), the next step is a CRM lookup on that domain. For large organizations - private equity firms, financial services groups, multinational corporations - this lookup frequently returns multiple company records sharing the same domain: the parent holding company, operating subsidiaries, fund vehicles, lending arms, and more.

For example, looking up `blackstone.com` in a CRM might return:
- Blackstone Inc (ParentCo - the holding company)
- Blackstone Private Equity (Sponsor - the PE fund)
- Blackstone Credit & Insurance (Lender - the credit arm)
- Blackstone Real Estate (Sponsor - the real estate fund)
- Blackstone Treasury (Other - treasury operations)

A "VP, Credit Investments" at "Blackstone Credit" on LinkedIn should be associated with the Blackstone Credit & Insurance record, not the parent company or the PE fund. This agent makes that determination.

### Why This Is Hard

1. **LinkedIn company names don't match CRM names exactly.** LinkedIn might say "Blackstone Credit" while the CRM has "Blackstone Credit & Insurance." Substring matching helps but isn't always sufficient.
2. **Generic titles don't indicate a division.** An "Executive Assistant at Blackstone" could sit in any business unit. The agent needs a fallback strategy.
3. **ParentCo records are containers, not employers.** People almost never "work for" the parent holding company in practice - they work for a specific subsidiary. But the ParentCo record exists in the CRM and will appear in lookup results.
4. **Activity signals vary.** Some subsidiaries are active customers with high engagement; others are dormant records. Activity can help disambiguate but requires careful weighting.

### Pipeline Position

```
Employment verification (detect "Likely Outdated")
        |
Stage current employment data
        |
Primary role identification (pick primary role + domain + org_id)
        |
        v
+-------------------------------+     +-------------------------------+
|  CRM Domain Lookup            |     |  CRM LinkedIn ID Lookup       |
|  Input: contact_new_domain    |     |  Input: LinkedIn numeric ID   |
|  Returns: 0-N company records |     |  Returns: 0-N company records |
+-------------------------------+     +-------------------------------+
        \                               /
         \                             /
          v                           v
+-------------------------------------------+
|  THIS AGENT                              |  Claygent (this spec)
|  Input: Both lookup results +             |  Model: capable model
|         contact context                   |  Web access: OFF
|  Step 1: Merge & deduplicate results      |
|  Step 2-3: Filter ParentCo + shell records|
|  Step 4-6: Name / Title / Activity match  |
|  Output: Selected ID + needs_review flag  |
+-------------------------------------------+
        |
        v
  If needs_review = false:
    Auto-associate contact with company record
  If needs_review = true:
    Route to human review queue
        |
Role tenure fields (predecessor/successor Record IDs + CRM Links)
```

**Why dual lookup:** LinkedIn-reported company domains frequently differ from CRM domains. Example: a person at Bridgepoint shows `bridgepointgroup.com` on LinkedIn, but the CRM uses `bridgepoint.eu`. Domain-only lookup misses the match. LinkedIn numeric company ID (`org_id`) provides a stable identifier that links the same organization across domain variants.

---

## Architecture

### Single-Stage Local Analysis

This is a local-data-only agent. All inputs come from the CRM lookup results (already retrieved) and the contact's LinkedIn context (from upstream enrichment). No web research is needed because the decision is entirely about matching existing CRM records to existing contact data.

### Model Selection

This is a classification task on structured local data, but the agent processes full enrichment JSONs (not pre-extracted fields) and validates upstream agent decisions. **Use a capable model** - the full-JSON input and upstream validation step require a model that can parse large structured inputs and reason about consistency. Currently targeting a recent GPT model. If running in Clay, this may be Navigator-tier (5 credits) rather than Neon (2 credits) depending on the model selected.

### Why Not a Formula

A Clay AI formula could handle Tier 1 (name matching) cheaply. But Tiers 2 and 3 require interpreting job titles in the context of business segments and weighing multiple activity signals simultaneously. That's agent territory. If you want a cost-optimized two-pass approach, use a formula for the name match (per Clay AI formula patterns), then route only the unresolved cases to this agent.

### Error Mode: Prefer Low Confidence Over Wrong

This agent sits upstream of contact-to-company association. Picking the wrong company record means all downstream data (account enrichment, outreach targeting, reporting) is polluted. When the agent can't confidently disambiguate, it should return the best guess with Low confidence and populate `alternative_company_ids` so the match can be flagged for human review.

---

## Selection Logic

### Step 0: Merge & Deduplicate Lookup Results

The agent receives results from two CRM lookups that may overlap:
- **LinkedIn numeric ID lookup** - matches on the company's LinkedIn numeric ID (stored as `linkedin_company_numeric_id_enriched_external` in the CRM). Returns all CRM records for that LinkedIn organization, regardless of domain.
- **Domain lookup** - matches on the domain from the contact's LinkedIn profile. May return different records if the LinkedIn domain differs from the CRM domain.

Merge both result sets and deduplicate by `id` (`hs_object_id`). The merged set becomes the input for the selection logic below.

### Three-Tier Priority Hierarchy

After merge, filtering, the agent evaluates matches from highest confidence to lowest:

| Tier | Method | Logic | Expected Coverage | Confidence |
|------|--------|-------|-------------------|------------|
| 1 | **Company name match** | Contact's LinkedIn company name matches or is substantially contained in a CRM record's company name | ~60-70% | High |
| 2 | **Title/role context match** | Contact's job title implies a specific business segment that maps to a CRM record's `company_segment` or industry | ~15-20% | Medium |
| 3 | **Activity-based fallback** | No name or title signal - score remaining records by engagement metrics and segment priority | ~10-15% | Low |

### Tier 1: Company Name Match

LinkedIn company names frequently include the division: "Blackstone Credit", "EQT Infrastructure", "Ardian Growth". When this happens, a name-containment check against CRM record names resolves the match immediately.

**Matching rules:**
- Case-insensitive comparison
- Check if the LinkedIn company name is contained in the CRM company name, or vice versa
- Normalize common variations: "&" vs "and", remove "Inc", "LLC", "Ltd", etc.
- If multiple CRM records match by name, prefer the one with the closest string match (fewest extra characters)

**Examples:**
- LinkedIn: "Blackstone Credit" -> CRM: "Blackstone Credit & Insurance" -> **Match** (High confidence)
- LinkedIn: "EQT" -> CRM has "EQT Partners", "EQT Infrastructure", "EQT Private Equity" -> **No unique match** (falls to Tier 2)

### Tier 2: Title/Role Context Match

When the LinkedIn company name is generic (just the parent name), the contact's job title often indicates which business unit they belong to.

**Segment mapping signals:**

| Title Keywords | Likely Segment | CRM Field Patterns |
|---------------|----------------|-------------------|
| Credit, Lending, Loan, Debt, Fixed Income | Lender | `company_segment = "Lender"` or industry contains credit/lending terms |
| Investment, Fund, Portfolio, Buyout, Equity, Growth | Sponsor | `company_segment = "Sponsor"` |
| Real Estate, Property, REIT | Sponsor (RE) | `company_segment = "Sponsor"` + `mkt__fund_type` or `company_sectors` contains real estate |
| Treasury, Operations, Compliance, Legal, HR, Finance | Other/ParentCo | Could be shared services at parent level |

**Rules:**
- Only apply title-based matching when Tier 1 didn't produce a unique match
- If the title maps clearly to one segment and exactly one CRM record has that segment, select it
- If the title maps to a segment but multiple records share that segment, fall through to Tier 3

### Pre-Filter: ParentCo Elimination

Before applying the three tiers, remove any record where `company_segment = "ParentCo"` from consideration. These are holding-company records not used for contact association. **Exception:** if ALL records are ParentCo, keep them and skip to Tier 3.

This was previously embedded in Tier 3 but moved to a pre-filter step because ParentCo records should never compete with subsidiaries at any tier.

### Tier 3: Activity-Based Fallback (Numeric Scoring)

When neither name nor title resolves the match, score remaining candidates using explicit point values:

| Signal | Condition | Points |
|--------|-----------|--------|
| `lifecyclestage` | `customer` | +3 |
| `lifecyclestage` | `lead` | +1 |
| `active_user_count` | > 50 | +3 |
| `active_user_count` | 10-50 | +2 |
| `active_user_count` | 1-9 | +1 |
| `account_status` | `Active` | +1 |
| `company_segment` | `Sponsor` | +2 |
| `company_segment` | `Lender` | +1 |
| `company_segment` | `Other` | +0 |

Select the record with the highest total score. If tied, prefer the record with the higher `num_associated_contacts`. Confidence is Low.

### Unambiguous vs. Needs Review

The agent makes a binary determination about whether the match can be auto-associated:

| Selection Path | needs_review | company_id_unambiguous |
|---------------|-------------|----------------------|
| Single result after filtering | false | populated |
| Name match to one record | false | populated |
| Title match to one record | false | populated |
| Activity-based fallback | **true** | empty |
| All-ParentCo fallback | **true** | empty |
| No records remain | **true** | empty |
| Upstream agent obviously wrong | **true** | empty |

When `needs_review = true`, the agent must also provide a `review_reason` (10-16 words) explaining what needs human attention. This could be an ambiguous company match, an upstream agent error, or both.

### Special Cases

- **Single result:** Select immediately as unambiguous regardless of segment.
- **Single non-ParentCo result:** After ParentCo + shell elimination, if only one record remains, select it as unambiguous.
- **All ParentCo:** Select the ParentCo with the highest `hs_num_child_companies`. Set `needs_review = true`.
- **Shell records:** Ignore records where `company_segment` is missing AND `active_user_count` is 0/missing AND `lifecyclestage` is missing. These are typically auto-created by integrations (e.g., Clay creating a new company record from a LinkedIn domain that doesn't match existing CRM domains).
- **No records after filtering:** All fields empty/default, `needs_review = true`.

---

## Input Specification

### Variables (5 total)

| # | Variable | Source | Required | Description |
|---|----------|--------|----------|-------------|
| 1 | `enrich_person` | Clay "Enrich Person" integration | Yes | Full LinkedIn person enrichment JSON. Contains headline, title, summary, current_experience array (company names, domains, titles, org_ids), experience history, education, connections. The agent extracts company name, title, headline, and any division-specific signals directly from this data. |
| 2 | `enrich_company` | Clay "Enrich Company" integration | Yes | Full LinkedIn company enrichment JSON for the primary role company. Contains company description, industry, specialties, employee count, headquarters, LinkedIn URL. Provides additional context about the organization for disambiguation. |
| 3 | `crm_lookup_via_linkedin_id` | HubSpot Lookup Company by LinkedIn numeric ID | Yes | Full JSON results of company records matching the LinkedIn numeric company ID (`org_id` from enrichment, matched against `linkedin_company_numeric_id_enriched_external` in CRM). May return 0-N records. Can be empty if no match. |
| 4 | `crm_lookup_via_domain` | HubSpot Lookup Company by domain | Yes | Full JSON results of company records matching the contact's LinkedIn-reported company domain. May return 0-N records. Can be empty if no match or if domain differs from CRM domain. |
| 5 | `primary_role_agent_output` | Upstream primary role identification Claygent output (full JSON) | Yes | Full output from the upstream primary role identification agent. Contains `primary_role_domain`, `primary_role_company_name`, `primary_role_title`, and `agent_reasoning`. This agent validates the upstream determination and uses it as a starting point for CRM record selection. |

**Design rationale:** Previous versions pre-extracted individual fields (company name, title, headline, domain) from the enrichment data and passed them as separate variables. This was fragile - it limited what the agent could see and required upstream formulas for each field. Passing the full JSONs lets the agent extract whatever signals it needs (headline, title, summary, experience history, company description) and cross-reference them directly. This is viable because the agent runs on a capable model.

---

## System Prompt

```json
{
  "role": "CRM Data Analyst specializing in company hierarchy resolution for financial services firms. You understand parent-child company structures where a single organization (e.g., Bridgepoint, Blackstone) maps to multiple CRM records representing distinct business divisions (Private Equity, Credit, Infrastructure, Real Estate, etc.) and a ParentCo holding record. You also understand that LinkedIn company domains may differ from CRM domains for the same organization, which is why both LinkedIn numeric ID and domain lookups are provided. You have access to full enrichment data and can validate upstream agent determinations.",
  "constraints": [
    "You MUST select exactly one company record from the merged lookup results, or determine that no valid match exists.",
    "NEVER fabricate company IDs or data not present in the input.",
    "If only one non-ParentCo, non-shell record exists after filtering, select it as unambiguous.",
    "If ALL records are ParentCo, select the ParentCo with the highest hs_num_child_companies and set needs_review to true.",
    "Do not consider records where company_segment is missing AND active_user_count is 0 or missing AND lifecyclestage is missing -- these are likely shell records created by integrations.",
    "Limit selection_reasoning to 100 words maximum.",
    "review_reason must be 10 to 16 words.",
    "When needs_review is true, company_id_unambiguous must be empty string.",
    "When needs_review is true, always populate alternative_company_ids with all plausible options.",
    "If the upstream primary role agent made an obviously incorrect determination (e.g., selected an advisory role over a clear operating role, or the headline clearly names a different company as primary), set needs_review to true and explain in review_reason."
  ]
}
```

## User Prompt

```json
{
  "goal": "From the CRM lookup results (via LinkedIn numeric ID in {crm_lookup_via_linkedin_id} and/or domain in {crm_lookup_via_domain}), select the single best company record to associate with the contact described in {enrich_person}. The upstream primary role agent determined this person's primary role as described in {primary_role_agent_output}. Validate that determination, select the correct CRM company record, and determine whether the match is unambiguous or requires human review.",
  "task_steps_to_perform": [
    "1. EXTRACT CONTEXT: From {enrich_person}, extract the person's title, headline, summary, and current_experience entries (company names, domains, titles, org_ids). From {primary_role_agent_output}, extract primary_role_domain, primary_role_company_name, primary_role_title, and agent_reasoning. From {enrich_company}, extract any additional company context (description, industry, specialties) that may help disambiguate between CRM records.",
    "2. VALIDATE UPSTREAM AGENT: Check if the primary role determination in {primary_role_agent_output} is consistent with the full enrichment data in {enrich_person}. Specifically: Does the selected role appear to be an OPERATING role (MD, Partner, VP, Principal, Director, etc.) rather than ADVISORY or GOVERNANCE? Does the headline or title field in {enrich_person} clearly reference a different company as the primary affiliation? If the determination is obviously wrong, set needs_review to true and note the specific issue in review_reason. If the determination looks correct or reasonable, proceed with the upstream agent's company name, title, and domain as the starting point.",
    "3. MERGE & DEDUPLICATE: Combine results from {crm_lookup_via_linkedin_id} and {crm_lookup_via_domain}. Remove duplicates by matching on id. Extract from each unique record: id, name, company_segment, active_user_count, lifecyclestage, account_status, platform_display_name, company_sectors, industry, hs_parent_company_id, hs_num_child_companies, num_associated_contacts, notes_last_contacted, and domain.",
    "4. ELIMINATE PARENTCO: Remove any record where company_segment = 'ParentCo' from consideration. Exception: if ALL records are ParentCo, keep them, select the one with highest hs_num_child_companies, set needs_review to true with review_reason, and skip to output.",
    "5. ELIMINATE SHELL RECORDS: Remove any record where company_segment is missing AND active_user_count is 0 or missing AND lifecyclestage is missing. If no records remain after filtering, set all output fields to empty/false defaults with needs_review = true.",
    "6. NAME MATCH (highest priority): Compare the primary_role_company_name from {primary_role_agent_output} and the headline from {enrich_person} against each remaining record's 'name' and 'platform_display_name' fields. If a company name or division name closely matches one specific record (e.g., 'Blackstone Credit' matches 'Blackstone Credit & Insurance'), select that record as unambiguous. Partial matches count (e.g., 'EQT Infra' matches 'EQT Infrastructure'). If a clear name match is found, skip to output.",
    "7. TITLE/ROLE MATCH (second priority): If no clear name match, analyze the person's title and headline from {enrich_person} for division indicators. Map keywords: 'credit'/'debt'/'lending' -> Lender or Private Debt records. 'infrastructure'/'infra' -> Infrastructure records. 'real estate'/'BREP'/'property' -> Real Estate records. 'growth'/'venture' -> Growth records. 'PE'/'buyout'/'private equity' -> Sponsor/Buyout records. 'treasury'/'capital markets' -> Treasury records. 'hedge fund'/'alternatives'/'BAAM' -> BAAM/Hedge Fund records. If a single record matches, select it as unambiguous.",
    "8. ACTIVITY-BASED FALLBACK (third priority): If no name or title match resolves to a single record, score remaining candidates: (a) lifecyclestage = 'customer' scores +3, 'lead' scores +1; (b) active_user_count > 50 scores +3, 10-50 scores +2, 1-9 scores +1; (c) account_status = 'Active' scores +1; (d) company_segment = 'Sponsor' scores +2, 'Lender' scores +1, 'Other' scores +0. Select the highest score. Tiebreaker: higher num_associated_contacts. Set needs_review to true with review_reason (10-16 words).",
    "9. OUTPUT: Return selected_company_id, selected_company_name, company_id_unambiguous (only if unambiguous), needs_review, review_reason (10-16 words if applicable, empty string if not), selection_reasoning, and alternative_company_ids."
  ]
}
```

## Output Schema

---

```json
{
  "type": "object",
  "properties": {
    "selected_company_id": {
      "type": "string",
      "description": "HubSpot company record ID of the selected company. Always populated with best guess, even when needs_review is true."
    },
    "selected_company_name": {
      "type": "string",
      "description": "Name of the selected CRM company record."
    },
    "company_id_unambiguous": {
      "type": "string",
      "description": "Same as selected_company_id when the match is clear (name match, title match to single record, or single result after filtering). Empty string when needs_review is true."
    },
    "needs_review": {
      "type": "boolean",
      "description": "True when: (1) company match is ambiguous (activity-based fallback, all-ParentCo, no records), OR (2) upstream primary role agent made an obviously incorrect determination. False when company selection is based on clear name or title match and upstream agent looks correct."
    },
    "review_reason": {
      "type": "string",
      "description": "10 to 16 word summary of why review is needed. Should identify the specific issue: ambiguous company match, upstream agent error, or both. Empty string when needs_review is false."
    },
    "selection_reasoning": {
      "type": "string",
      "description": "Brief explanation of the full selection process - context extraction, upstream validation, merge/filter, which step resolved, and why. Max 100 words."
    },
    "alternative_company_ids": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Array of other plausible HubSpot company IDs. Empty array when match is unambiguous."
    }
  },
  "required": [
    "selected_company_id",
    "selected_company_name",
    "company_id_unambiguous",
    "needs_review",
    "review_reason",
    "selection_reasoning",
    "alternative_company_ids"
  ]
}
```

## Variables

```
{enrich_person}: variable
{enrich_company}: variable
{crm_lookup_via_linkedin_id}: variable
{crm_lookup_via_domain}: variable
{primary_role_agent_output}: variable
```

---

## Clay Column Setup

| Column | Type | Source | Maps to Variable |
|--------|------|--------|-----------------|
| Enrich Person | Integration | Clay "Enrich Person" (upstream) | `{enrich_person}` |
| Enrich Company | Integration | Clay "Enrich Company" (upstream) | `{enrich_company}` |
| Primary Role ID | Claygent | Upstream primary role identification agent | `{primary_role_agent_output}` |
| Lookup New Company in CRM via Domain | Integration | HubSpot lookup by domain (from primary_role_domain) | `{crm_lookup_via_domain}` |
| Lookup New Company in CRM via Numeric LinkedIn ID | Integration | HubSpot lookup by LinkedIn numeric company ID (from org_id in enrichment) | `{crm_lookup_via_linkedin_id}` |
| **CRM Record Selection** | **Claygent** | **This agent** | - |
| Parse Selected ID | Formula | Extract `selected_company_id` from agent output | - |
| Parse Selected Name | Formula | Extract `selected_company_name` from agent output | - |
| Parse Unambiguous ID | Formula | Extract `company_id_unambiguous` from agent output | - |
| Parse Needs Review | Formula | Extract `needs_review` from agent output | - |
| Parse Review Reason | Formula | Extract `review_reason` from agent output | - |
| Parse Alternatives | Formula | Extract `alternative_company_ids` from agent output | - |

### Credit Cost

| Component | Credits | Notes |
|-----------|---------|-------|
| HubSpot Lookup Company (x2) | 0 | Clay native integrations (domain + LinkedIn ID) |
| Claygent (capable model) | 2-5 credits | Depends on model tier selected. Full-JSON input + validation warrants a capable model. |
| **Total per contact** | **~2-5 credits** | Enrichment credits already spent upstream |

---

## Test Cases

### Test Case 1: Clear Name Match (Step 6)

**Context:** Contact's LinkedIn says "Blackstone Credit" - directly matches a CRM record.

**Input:**
```
enrich_person: { "title": "VP, Credit Investments", "headline": "VP, Credit Investments at Blackstone Credit", "current_experience": [{"company": "Blackstone Credit", "title": "VP, Credit Investments", "company_domain": "blackstone.com"}] }
enrich_company: { "name": "Blackstone", "industry": "Investment Management" }
primary_role_agent_output: { "primary_role_domain": "blackstone.com", "primary_role_company_name": "Blackstone Credit", "primary_role_title": "VP, Credit Investments", "agent_reasoning": "Single current role, OPERATING, matches headline." }
crm_lookup_via_linkedin_id: [same 5 records as crm_lookup_via_domain]
crm_lookup_via_domain: [
  {"id": "101", "properties": {"name": "Blackstone Inc", "domain": "blackstone.com", "company_segment": "ParentCo", "hs_num_child_companies": "4", "active_user_count": "12", "lifecyclestage": "customer"}},
  {"id": "102", "properties": {"name": "Blackstone Private Equity", "domain": "blackstone.com", "company_segment": "Sponsor", "hs_parent_company_id": "101", "active_user_count": "137", "lifecyclestage": "customer"}},
  {"id": "103", "properties": {"name": "Blackstone Credit & Insurance", "domain": "blackstone.com", "company_segment": "Lender", "hs_parent_company_id": "101", "active_user_count": "194", "lifecyclestage": "customer"}},
  {"id": "104", "properties": {"name": "Blackstone Real Estate", "domain": "blackstone.com", "company_segment": "Sponsor", "hs_parent_company_id": "101", "active_user_count": "45", "lifecyclestage": "lead"}},
  {"id": "105", "properties": {"name": "Blackstone Treasury", "domain": "blackstone.com", "company_segment": "Other", "hs_parent_company_id": "101", "active_user_count": "3", "lifecyclestage": "subscriber"}}
]
```

**Expected Output:**
```json
{
  "selected_company_id": "103",
  "selected_company_name": "Blackstone Credit & Insurance",
  "company_id_unambiguous": "103",
  "needs_review": false,
  "review_reason": "",
  "selection_reasoning": "Upstream agent correct. Merged 5 records, ParentCo eliminated. Name match: 'Blackstone Credit' from enrichment matches CRM 'Blackstone Credit & Insurance'. Title confirms. Unambiguous.",
  "alternative_company_ids": []
}
```

### Test Case 2: Title Context Match (Step 7)

**Context:** Contact's LinkedIn says just "Ardian" (the parent name), but their title reveals they work in private debt.

**Input:**
```
enrich_person: { "title": "Director, Private Debt", "headline": "Director, Private Debt at Ardian", "current_experience": [{"company": "Ardian", "title": "Director, Private Debt", "company_domain": "ardian.com"}] }
enrich_company: { "name": "Ardian", "industry": "Investment Management" }
primary_role_agent_output: { "primary_role_domain": "ardian.com", "primary_role_company_name": "Ardian", "primary_role_title": "Director, Private Debt", "agent_reasoning": "Single current role, OPERATING, matches headline." }
crm_lookup_via_linkedin_id: [same 3 records as crm_lookup_via_domain]
crm_lookup_via_domain: [
  {"id": "201", "properties": {"name": "Ardian", "domain": "ardian.com", "company_segment": "ParentCo", "hs_num_child_companies": "2", "active_user_count": "8", "lifecyclestage": "customer"}},
  {"id": "202", "properties": {"name": "Ardian Private Debt", "domain": "ardian.com", "company_segment": "Lender", "hs_parent_company_id": "201", "active_user_count": "42", "lifecyclestage": "customer"}},
  {"id": "203", "properties": {"name": "Ardian Growth", "domain": "ardian.com", "company_segment": "Sponsor", "hs_parent_company_id": "201", "active_user_count": "67", "lifecyclestage": "customer"}}
]
```

**Expected Output:**
```json
{
  "selected_company_id": "202",
  "selected_company_name": "Ardian Private Debt",
  "company_id_unambiguous": "202",
  "needs_review": false,
  "review_reason": "",
  "selection_reasoning": "Upstream agent correct. ParentCo eliminated. No unique name match ('Ardian' too generic). Title 'Director, Private Debt' from enrichment maps to Lender segment, matching Ardian Private Debt. Unambiguous.",
  "alternative_company_ids": []
}
```

### Test Case 3: Activity Fallback - Needs Review (Step 8)

**Context:** Contact is an EA at "Blackstone" - generic title, generic company name. No name or title signal.

**Input:**
```
enrich_person: { "title": "Executive Assistant", "headline": "Executive Assistant at Blackstone", "current_experience": [{"company": "Blackstone", "title": "Executive Assistant", "company_domain": "blackstone.com"}] }
enrich_company: { "name": "Blackstone", "industry": "Investment Management" }
primary_role_agent_output: { "primary_role_domain": "blackstone.com", "primary_role_company_name": "Blackstone", "primary_role_title": "Executive Assistant", "agent_reasoning": "Single current role, OPERATING, matches headline." }
crm_lookup_via_linkedin_id: [same 5 records as crm_lookup_via_domain]
crm_lookup_via_domain: [same 5 Blackstone records as Test Case 1]
```

**Expected Output:**
```json
{
  "selected_company_id": "102",
  "selected_company_name": "Blackstone Private Equity",
  "company_id_unambiguous": "",
  "needs_review": true,
  "review_reason": "Generic title 'Executive Assistant' at 'Blackstone' gives no signal to distinguish PE from Credit division.",
  "selection_reasoning": "ParentCo eliminated. No name signal ('Blackstone' matches all). No title signal (EA is generic). Scoring: PE=+3(customer)+3(137 users)+2(Sponsor)=8, Credit=+3+3+1(Lender)=7. PE selected by score.",
  "alternative_company_ids": ["103", "104", "105"]
}
```

**Design note:** The numeric scoring makes this deterministic (PE=8 vs Credit=7), but `needs_review = true` because it's an activity fallback - the agent is guessing based on engagement signals, not identity match. A human should verify which Blackstone division this EA actually sits in.

### Test Case 4: Single Result - Unambiguous

**Context:** Both lookups return just one record. No disambiguation needed.

**Input:**
```
enrich_person: { "title": "Principal", "headline": "Principal at EQT Partners", "current_experience": [{"company": "EQT Partners", "title": "Principal", "company_domain": "eqtgroup.com"}] }
enrich_company: { "name": "EQT Partners", "industry": "Investment Management" }
primary_role_agent_output: { "primary_role_domain": "eqtgroup.com", "primary_role_company_name": "EQT Partners", "primary_role_title": "Principal", "agent_reasoning": "Single current role, OPERATING, matches headline." }
crm_lookup_via_linkedin_id: [{"id": "301", "properties": {"name": "EQT Partners", "domain": "eqtgroup.com", "company_segment": "Sponsor", "active_user_count": "89", "lifecyclestage": "customer"}}]
crm_lookup_via_domain: [{"id": "301", "properties": {"name": "EQT Partners", "domain": "eqtgroup.com", "company_segment": "Sponsor", "active_user_count": "89", "lifecyclestage": "customer"}}]
```

**Expected Output:**
```json
{
  "selected_company_id": "301",
  "selected_company_name": "EQT Partners",
  "company_id_unambiguous": "301",
  "needs_review": false,
  "review_reason": "",
  "selection_reasoning": "Merged and deduped to 1 unique record. Single result - EQT Partners selected by default. Unambiguous.",
  "alternative_company_ids": []
}
```

### Test Case 5: No Results

**Context:** Both lookups return nothing.

**Input:**
```
enrich_person: { "title": "Managing Partner", "headline": "Managing Partner at Stealth Fund", "current_experience": [{"company": "Stealth Fund", "title": "Managing Partner", "company_domain": "stealthfund.com"}] }
enrich_company: { "name": "Stealth Fund" }
primary_role_agent_output: { "primary_role_domain": "stealthfund.com", "primary_role_company_name": "Stealth Fund", "primary_role_title": "Managing Partner", "agent_reasoning": "Single current role, OPERATING, matches headline." }
crm_lookup_via_linkedin_id: []
crm_lookup_via_domain: []
```

**Expected Output:**
```json
{
  "selected_company_id": "",
  "selected_company_name": "",
  "company_id_unambiguous": "",
  "needs_review": true,
  "review_reason": "No CRM company records found via LinkedIn ID or domain lookup for this organization.",
  "selection_reasoning": "Both lookups returned empty. No records to evaluate.",
  "alternative_company_ids": []
}
```

### Test Case 6: Dual Lookup with Domain Mismatch + Shell Record (Real Data - Bridgepoint)

**Context:** Nikki Zhao is a "Senior Associate at Bridgepoint." Her LinkedIn reports `bridgepointgroup.com` as the domain, but the CRM uses `bridgepoint.eu`. The domain-only lookup returns a shell record (auto-created by Clay). The LinkedIn ID lookup (`org_id: 2027252`) returns all 4 Bridgepoint entities.

This test case demonstrates why dual lookup was added - domain mismatch would have caused a complete miss with domain-only lookup.

**Input:**
```
enrich_person: { "title": "Senior Associate", "headline": "Senior Associate at Bridgepoint", "org": "Bridgepoint", "current_experience": [{"company": "Bridgepoint", "title": "Senior Associate", "company_domain": "bridgepointgroup.com", "org_id": 2027252, "start_date": "2024-09-01"}], "experience": [prior roles at Advent International, Deutsche Bank] }
enrich_company: { "name": "Bridgepoint", "description": "Bridgepoint Group is one of the world's leading quoted private asset growth investors, specialising in private equity, infrastructure and private credit.", "industry": "Investment Management" }
primary_role_agent_output: { "primary_role_domain": "bridgepointgroup.com", "primary_role_company_name": "Bridgepoint", "primary_role_title": "Senior Associate", "agent_reasoning": "Single current role at Bridgepoint matches the person's title and headline exactly, classifying as operating role by default." }
crm_lookup_via_linkedin_id: [
  {"id": "5334631868", "properties": {"name": "Bridgepoint Private Equity", "domain": "bridgepoint.eu", "company_segment": "Sponsor", "hs_parent_company_id": "7686075367", "hs_num_child_companies": "0", "active_user_count": "19", "lifecyclestage": "customer", "account_status": "Active", "company_sectors": "Private Equity", "platform_display_name": "Bridgepoint Capital Markets", "mkt__fund_type": "Buyout", "num_associated_contacts": "114", "notes_last_contacted": "2026-02-27T16:31:19.588Z"}},
  {"id": "7630278627", "properties": {"name": "Bridgepoint Credit", "domain": "bridgepoint.eu", "company_segment": "Lender", "hs_parent_company_id": "7686075367", "hs_num_child_companies": "0", "active_user_count": "57", "lifecyclestage": "lead", "account_status": "Active", "company_sectors": "Private Debt", "platform_display_name": "Bridgepoint Credit", "num_associated_contacts": "66", "notes_last_contacted": "2025-11-11T14:56:46.002Z"}},
  {"id": "7686075367", "properties": {"name": "Bridgepoint (ParentCo)", "domain": "bridgepoint.eu", "company_segment": "ParentCo", "hs_num_child_companies": "2", "active_user_count": "0", "num_associated_contacts": "0"}},
  {"id": "421944437989", "properties": {"name": "Bridgepoint Group", "domain": "bridgepointgroup.com", "active_user_count": "0", "num_associated_contacts": "1"}}
]
crm_lookup_via_domain: [
  {"id": "421944437989", "properties": {"name": "Bridgepoint Group", "domain": "bridgepointgroup.com", "active_user_count": "0", "num_associated_contacts": "1"}}
]
```

**Expected Output:**
```json
{
  "selected_company_id": "5334631868",
  "selected_company_name": "Bridgepoint Private Equity",
  "company_id_unambiguous": "",
  "needs_review": true,
  "review_reason": "Generic title 'Senior Associate' at 'Bridgepoint' gives no signal to distinguish PE from Credit division.",
  "selection_reasoning": "Upstream agent correct (single OPERATING role). Merged 4 unique records from dual lookup. Eliminated ParentCo + shell record. 2 candidates: PE and Credit. 'Bridgepoint' matches both. 'Senior Associate' is generic. Scoring: PE=+3(customer)+2(19 users)+1(Active)+2(Sponsor)=8, Credit=+1(lead)+3(57 users)+1(Active)+1(Lender)=6. PE selected.",
  "alternative_company_ids": ["7630278627"]
}
```

**Design notes:**
- Without LinkedIn ID lookup, only the shell record (Bridgepoint Group) would have been found via domain. The contact would have been associated with a useless record or flagged as no match.
- The shell record (421944437989) was auto-created by Clay because the LinkedIn domain `bridgepointgroup.com` didn't match any existing CRM domain. It has no `company_segment`, no `lifecyclestage`, and `active_user_count = 0`, so it's correctly filtered out.
- The remaining decision between PE and Credit is genuinely ambiguous for a "Senior Associate" - this is the correct case for `needs_review = true`.

---

## Production Notes

### Segment Priority Is Domain-Specific

The Sponsor > Lender > Other > ParentCo hierarchy reflects financial services norms where the investment arm is the primary operating entity. For non-financial companies (e.g., a technology conglomerate with multiple product divisions), you may need to adjust:
- Replace segment-based priority with headcount or revenue-based priority
- Use `lifecyclestage` and `active_user_count` as the primary fallback signals instead of segment ordering

### The Flagship Entity Problem

Test Case 3 highlights the core limitation of Tier 3. When a generic role at a generic company name hits the activity fallback, the agent must guess - and the "right" guess depends on business context that isn't in the data. Two mitigations:

1. **Add a `flagship_entity` flag** to the primary subsidiary CRM record. A simple boolean HubSpot property that marks the default entity for ambiguous matches. The agent could check this before applying segment priority.
2. **Don't auto-associate ambiguous matches.** Route them to a human review queue using the `needs_review` flag. The conditional branch in Clay: if `needs_review == true`, skip the CRM update and flag for review. The `review_reason` field gives the reviewer context on what to check.

### HubSpot Lookup Results Structure

The HubSpot "Lookup Company" integrations in Clay return results in a specific format. Both `crm_lookup_via_linkedin_id` and `crm_lookup_via_domain` should map to their respective raw integration outputs. Common patterns:
- Results are nested under a `results` array in some configurations
- Each record has `hs_object_id` in the `properties` object
- Properties may use different casing depending on the HubSpot API version

If the lookup output wraps results in an outer object, add a pre-processing formula to extract the inner array before passing to this agent.

### selection_reasoning and review_reason Fields

Per standard AI agent prompting patterns, reasoning fields are not included by default (Clay captures reasoning natively). This agent includes two deliberately:
- `selection_reasoning` (100 words max) - full diagnostic of which steps fired and why, for debugging
- `review_reason` (10-16 words) - concise summary for the human reviewer, only populated when `needs_review = true`

The two fields serve different audiences: `selection_reasoning` is for the pipeline builder debugging misclassifications; `review_reason` is for the sales rep or data ops person reviewing the flagged record.

### Future Consideration: Previous Employment Context

The agent currently doesn't consider the contact's prior employment. If someone previously worked at a Lender and moved to Blackstone, there's a weak prior that they might land in a credit-adjacent division. A future version could accept the contact's previous `company_segment` as an optional input and use it as a Tier 2.5 signal. This requires passing in additional context from the employment verification pipeline output.

---

## Related Documents

| Document | Relationship |
|----------|-------------|
| Primary Role Identification Agent (not included) | Upstream agent - identifies the primary role domain that feeds the CRM lookup. This agent consumes its output (domain, company name, title). |
| Employment Verification Agent (not included) | Upstream agent - detects that the contact has changed jobs. Triggers the champion tracking pipeline that includes this agent. |
| Contact Current Employment Staging (not included) | Upstream CRM fields - stages the "where did they move" data. This agent refines which CRM record to associate with. |
| Contact Role Tenure Fields (not included) | Downstream CRM fields - once this agent selects the right record, handles predecessor/successor record linking via Record IDs and clickable CRM Links. |
| Clay Enriched Company Structure (not included) | Company data schema - describes fields available in CRM company records. |
| AI Agent Prompt Building Guide (not included) | Prompt structure pattern (system + user split for local-data mode). |
| Claygent Deep Dive (not included) | Model selection, credit costs, agent architecture patterns. |
| Clay AI Formula Generator (not included) | Formula patterns for extraction columns and potential formula-based pre-filter for name matching. |
| CRM Deduplication First Principles (not included) | Company matching and hierarchy concepts that inform the parent-child disambiguation logic. |
| B2B Account Hierarchy Architecture (not included) | Comprehensive hierarchy reference - provides architectural context for the parent-child disambiguation this agent performs (maturity levels, dual hierarchy framework, edge cases). |
