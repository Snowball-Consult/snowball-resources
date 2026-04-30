# Private Equity Job Title Decomposition - Seniority, Function, and Geographic Variation Taxonomy

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Category** | REFERENCE |
| **Purpose** | PE-specific overlay to domain-agnostic job title decomposition - canonical title hierarchy, function taxonomy, geographic variation matrix, and classification decision rules for automated title parsing in PE contact databases |
| **Trigger** | Classifying PE professional titles into function and seniority, building PE title parsing agents, resolving ambiguous PE titles, understanding geographic title variation |
| **Scope** | PE title hierarchy (entry to Managing Partner), geographic title conventions (US, UK, Europe, Asia, Middle East), PE function taxonomy with firm-size scaling, C-suite/partnership overlap resolution, edge cases, classification decision rules |
| **Not In Scope** | General title decomposition theory, classification methodology (rule-based vs. ML vs. LLM), CRM implementation, hedge fund/VC hierarchies in depth, compensation benchmarking, recruiting advice |
| **Dependencies** | Job Title Decomposition (domain-agnostic) (not included); [PE Fund Sizes and Structures Reference](private-equity-fund-sizes-structures-terminology.md); [PE Capital Markets Professional - Buyer Primer](pe-capital-markets-professional-buyer-primer.md) |
| **Keywords** | PE, private equity, job title, seniority, function, title decomposition, VP, Director, Principal, Managing Director, Partner, Managing Partner, Operating Partner, Investment Manager, geographic variation, title hierarchy, buyout, growth equity, private credit |
| **Domain Tags** | private-equity, title-decomposition, seniority, function, geographic-variation |
| **Maturity** | Working |
| **Last Reviewed** | 2026-03-03 |

---

## Core Insight

**Most PE professionals have "generic" investment functions - their role IS the default for their firm type.** A regular investor at a PE firm is an Analyst, Associate, VP, Principal, or Partner - with no functional specialization. Non-generic functions (IR, Capital Markets, BD, Legal, HR, Operations) are the exceptions. The classification task is therefore two-axis: **Function** (what's special about this person) x **Seniority** (their level in the hierarchy).

The single biggest classification trap is geographic variation. The same title token encodes different seniority levels depending on geography and firm origin. "Investment Manager" is junior in the US, mid-level in the UK, and maps to VP in Germany. "Director" means pre-Partner in PE but board member under UK Companies Act. These geographic shifts affect roughly 5-10 title tokens but account for the majority of classification errors.

---

## 1. The Standard PE Title Hierarchy

### 1.1 Canonical Ladder

The US PE hierarchy descends from investment banking with modifications for the partnership model:

| Level | Title(s) | Typical Age | YoE | Key Responsibilities | Carry Eligible? |
|-------|----------|-------------|-----|----------------------|-----------------|
| Entry | Analyst / Summer Analyst | 22-25 | 0-2 | Financial modeling, screening, monitoring, supporting due diligence | No |
| Junior | Associate | 24-28 | 2-4 | Lead deal execution, modeling, due diligence, initial sourcing | Rarely |
| Mid-Junior | Senior Associate | 26-32 | 4-6 | Bridge execution and leadership, lead smaller transactions, mentor juniors, IC discussions | Sometimes |
| Mid | Vice President | 30-35 | 6-9 | Lead transaction teams end-to-end, coordinate all deal aspects, present to Investment Committee | Often |
| Mid-Senior | Director / Principal | 33-39 | 9-12 | Deal origination, critical negotiations, portfolio company board seats, fundraising support | Yes |
| Senior | Managing Director / Partner | 36+ | 12+ | Final investment decisions, LP relationships, firm strategy, fundraising | Yes (significant) |
| Top | Managing Partner / Founding Partner | 40+ | 15+ | Firm governance, strategy, highest carry allocation | Yes (largest) |

**Total timeline from entry to Partner:** approximately 15-20 years with 2-3 years between promotions.

**Sources:** Mergers & Inquisitions PE Career Path; Growth Equity Interview Guide; 300hours.com

### 1.2 Employee vs. Partnership Titles

A critical structural distinction:

- **Employee titles** (Analyst through Director/Principal): Salaried positions. Compensation is base + bonus, with carry starting to appear at VP level and ramping through Principal.
- **Partnership titles** (MD, Partner, Managing Partner): May involve equity ownership in the management company. Partners "must also invest a significant amount of their personal wealth into the fund."

This distinction is highly firm-specific. At some firms, "Managing Director" is a senior employee title without equity, while "Partner" indicates actual partnership/ownership. At others, MD and Partner are interchangeable for the same level. A typical Partner/MD might receive 0.3-0.7% of the carry pool for a $1-10B fund.

### 1.3 Comparison to Adjacent Industry Hierarchies

| PE Title | IB Equivalent | Hedge Fund Equivalent | Private Credit Equivalent |
|----------|---------------|----------------------|--------------------------|
| Analyst | Analyst | Research Analyst | Analyst |
| Associate | Associate | Analyst / Research Associate | Associate |
| Senior Associate | (varies) | Senior Analyst | Senior Associate |
| VP | VP | Sector Head / Senior Analyst | VP |
| Director / Principal | Director / SVP | Portfolio Manager | Director / SVP |
| MD / Partner | Managing Director | PM / CIO | MD / Partner |

**Key differences from IB:** PE is flatter - fewer layers, more direct interaction between juniors and seniors, because PE firms are much smaller than IB divisions. IB's terminal employee title is MD; PE's partnership track sits above it.

**Key differences from hedge funds:** HF title structures are less standardized and "often a function of where the founder started their career." Titles are less meaningful and less consistent.

### 1.4 Firm Size Effect on Hierarchy

| Dimension | Mega-Fund ($10B+) | Middle Market ($500M-5B) | Lower MM / Micro (<$500M) |
|-----------|--------------------|--------------------------|---------------------------|
| **Number of levels** | 6-7 (Analyst, Associate, Sr Associate, VP, Principal, MD, SMD) | 5-6 (standard ladder) | 3-4 (Associate, Principal, Partner) |
| **Title granularity** | Highly differentiated | Standard | Compressed - may skip VP or combine levels |
| **Promotion speed** | Slow - "so many people in the mid-to-top levels, and no one wants to leave early and give up their carried interest" | Moderate | Faster - may "skip one rung of the ladder" to attract talent |
| **Title inflation** | Minimal - titles earned slowly | Moderate | Significant - VP or Principal titles given to professionals who would be Associates at mega-funds |

**Firm-specific variations at the top:**
- **Blackstone:** Analyst > Associate > VP > Principal > MD > **Senior Managing Director (SMD)**
- **KKR:** Analyst > Associate > VP > **Principal** (roughly = Senior Associate elsewhere) > Director > MD > Member (Partner)
- **Apollo:** Uses both "Managing Director" and "Partner" as distinct titles, with Partner senior to MD

**Critical implication for classification:** "Principal" at KKR has approximately 5 years of experience, while at most other firms Principal means pre-Partner with 9-12 years. The same title at different firms represents different seniority levels.

---

## 2. Geographic Title Variation

This is the hardest classification problem and where most automated systems fail.

### 2.1 Title-by-Geography Equivalence Matrix

| US Standard | UK (London) | Germany | France | Nordics | Asia (HK/SG) | Middle East (SWF) |
|------------|-------------|---------|--------|---------|--------------|-------------------|
| Analyst | Analyst / Investment Analyst | Analyst | Analyste | Associate (entry) | Analyst | Analyst |
| Associate | Associate / Investment Executive | Associate | Associate / Charge d'Affaires | Senior Associate | Associate | Associate |
| Senior Associate | Senior Associate | **Investment Manager** (junior) | Senior Associate | Vice President | **Investment Manager** | Senior Associate |
| VP | VP / **Associate Director** | **Investment Manager** | Vice-President | Director | VP / Investment Manager | VP |
| Director / Principal | **Investment Director** / Principal | **Investment Director** | **Directeur de Participations** | Senior Director | Director | Director |
| MD | MD | Partner / Geschaeftsfuehrer | Managing Director | Partner | MD | Executive Director / MD |
| Partner / Managing Partner | Partner | Managing Partner | Partner / Associe-Gerant | Managing Partner | Partner | Partner (rare at SWFs) |

### 2.2 United Kingdom

London is the largest PE market outside the US. Key UK-specific patterns:

- **Associate Director** = VP equivalent. Used interchangeably with "VP" at many UK firms. Requires 3-6 years PE experience.
- **Investment Director** = Director/Principal equivalent. Professionals "take on accountability for origination whilst taking day-to-day control of investment processes" and begin getting board seats.
- **Investment Manager** = Senior Associate to junior VP at UK mid-market firms (especially non-US-origin firms).
- **Investment Executive** = Junior deal team member (roughly Associate level).

**Two conventions coexist in London:**
- **US-origin firms** (KKR, Blackstone, Apollo, Carlyle) preserve American VP/Principal/MD structure
- **European-origin firms** (Permira, CVC, 3i, Bridgepoint, Apax) use Investment Manager/Investment Director/Associate Director nomenclature, with flatter structures and broader role bands

3i Group uses: Associate, Senior Associate, Associate Director, Director, Partner, Senior Partner, Managing Partner.

**Sources:** Circle Square PE job specs; eFinancialCareers; PER People; 3i Group

### 2.3 Germany

German PE uses distinct conventions influenced by the "Investmentmanager" tradition:

1. **Analyst / Associate** (entry)
2. **Investment Manager** (mid-level, roughly = US VP/Senior Associate, EUR 100-300K)
3. **Investment Director** (senior)
4. **Partner / Managing Partner** (executive)

German structures emphasize "broader role bands with flatter reporting" - fewer levels but each covers a wider span.

**Legal titles unique to Germany:**
- **Prokurist** (Sections 48-49 HGB): Commercial power of attorney, not a PE career level but a formal legal designation granting authority to represent the company. May appear alongside investment titles.
- **Geschaeftsfuehrer** (Managing Director): Legal representative of a GmbH. The most senior partners at PE firms structured as German GmbHs hold this title for legal purposes. Carries personal legal liability and is registered in the commercial register. More than a job title.

**Source:** Treuenfels executive search; LinkedIn Germany salary data

### 2.4 France

French PE has its own distinct nomenclature:

1. **Stagiaire** (Intern)
2. **Analyste** (Analyst)
3. **Associate**
4. **Senior Associate**
5. **Vice-President**
6. **Directeur d'Investissement / Directeur de Participations** (= US Director/Principal)
7. **Managing Director / Partner**

**France-specific titles:**
- **Charge d'Affaires** (Deal Officer): Junior-to-mid role, roughly Associate to Senior Associate. 3-5 years M&A experience before this role.
- **Directeur de Participations** (Portfolio Director): Senior title requiring "at least ten years of cumulative experience." English equivalents: Investment Director, Principal, or MD depending on fund size.

Many French PE firms with international LP bases are increasingly adopting English-language titles alongside traditional French ones.

**Source:** LinkFinance; The Big Win; HelloWork; InvestPrep

### 2.5 Nordics

Nordic PE shows egalitarian corporate culture influence. EQT (Europe's largest PE firm, Sweden-headquartered) uses: Associate, Senior Associate, Vice President, Director, Senior Director, Partner, Managing Partner.

Nordic firms tend to have flatter structures. The "Director" and "Senior Director" titles (rather than Principal/MD) appear more common at Nordic-origin firms. EQT also uses the distinctive "Investment Advisory Professional" title reflecting its legal structure where the advisory entity employs the deal team.

### 2.6 Asia

**Hong Kong / Singapore:** International PE firms use standard US title structures. Asian-origin firms (PAG, formerly Baring Asia) may use "Investment Manager" at the SA/VP level and "Investment Director" at the Principal level.

**Sovereign wealth funds:** GIC (Singapore) uses banking-style hierarchy: Associate, AVP (Assistant Vice President), VP, SVP (Senior Vice President). "GIC employees are likely to make it to SVP level as long as they do a decent job."

**India:** Hierarchy similar to international standards but advancement can happen more quickly at smaller funds. Entry-level pay is significantly lower ($20-40K equivalent).

**Japan:** Independent domestic firms exist alongside international firms. International firms use standard global titles. Japanese corporate hierarchy titles (bucho, kacho) are NOT used in PE firms.

### 2.7 Middle East

Dominated by sovereign wealth funds with distinct structures:

- **ADIA** (Abu Dhabi): Analyst > Associate > Senior Analyst > Portfolio Manager (equity roles); Associate > VP > Director (PE division)
- **PIF** (Saudi Arabia): Standard titles, Associate ~$225K, Senior Associate ~$275-300K
- **Mubadala** (Abu Dhabi): Standard titles, reportedly lower compensation than ADIA/QIA

SWF roles are "broader and shallower" than PE - about 50% deal analysis, 50% macro asset allocation. Promotion is "quite difficult" and "much more political." 0% personal income tax advantage.

Private PE firms in the region (Investcorp, Gulf Capital) use more standardized international titles.

### 2.8 Titles That Change Meaning by Geography

| Title Token | US | UK | Germany | France | Asia | Confidence |
|-------------|----|----|---------|--------|------|------------|
| **Investment Manager** | Rarely used; if used, generic/junior | Senior Associate to VP (mid-market) | VP equivalent (core mid-level title) | Not standard | Senior Associate/VP hybrid | **Context-dependent** |
| **Associate Director** | Not commonly used | = VP (standard alternative) | Not standard | Not standard | Not standard | **Context-dependent** |
| **Investment Director** | Not commonly used | = Principal/Director (senior) | Senior (pre-Partner) | = Directeur d'Investissement | = Principal/Director | **Context-dependent** |
| **Director** | Pre-Partner (= Principal) | VP-equivalent OR pre-Partner (firm-dependent); legally = board member | Varies | Mid-senior | Varies | **Context-dependent** |
| **Principal** | Pre-Partner at most firms; BUT = Senior Associate at KKR | Generally = Director / pre-Partner | Pre-Partner | Pre-Partner | Pre-Partner | **Context-dependent** (even within US) |

---

## 3. The Function Dimension

### 3.1 The "Generic" Function Concept

The majority of PE professionals have no functional specialization. Their role is the default for their firm type:

- A regular investor at a PE fund = generic function + seniority level
- A regular banker at an investment bank = generic
- A regular lender at a direct lending fund = generic

"Generic" is always paired with seniority: "generic VP," "generic Partner," "generic Managing Director." The function dimension only captures what makes someone different from the standard investment professional at their firm type.

### 3.2 PE-Specific Functions

These functions are unique to PE/financial services and don't exist in most corporate environments:

| Function | Description | Typical Titles |
|----------|-------------|----------------|
| **Investor Relations (IR)** | LP relationships, fundraising communications, quarterly reporting, capital call coordination | Head of IR, VP of Investor Relations, IR Associate, Director of Investor Relations |
| **Capital Markets** | Internal team arranging debt financing for investments and portfolio companies | Head of Capital Markets, Capital Markets VP, Capital Markets Associate |
| **Portfolio Operations / Value Creation** | Dedicated teams driving operational improvements in portfolio companies. Drives ~47% of value creation in buyouts. | Operating Partner, Operating MD, Director of Portfolio Ops, VP of Value Creation |
| **Fund Administration / Fund Accounting** | NAV calculation, financial records, investor reporting, capital call processing. 60%+ of mid-market firms outsource this. | Fund Controller, Fund Accountant, Head of Fund Administration |
| **Carried Interest / Waterfall Administration** | Calculates carry distribution, manages GP profit share, K-1 preparation | (Usually part of Fund Accounting or Finance) |
| **Deal Sourcing / Business Development** | Dedicated origination distinct from investment team | Head of BD, Business Development Associate, Origination VP |

### 3.3 Shared Functions (Corporate-Generic with PE Nuances)

| Function | PE-Specific Nuance |
|----------|-------------------|
| **Legal / General Counsel** | Fund formation, LP agreement drafting, SEC compliance, deal documentation. 85% also serve as CCO, 44% as Corporate Secretary. |
| **Compliance / CCO** | SEC registration, KYC/AML, regulatory monitoring. Required for SEC-registered advisers. Many smaller firms outsource. |
| **Finance / CFO / Accounting** | Fund-level accounting (distinct from fund admin), firm P&L, tax strategy across multiple fund vehicles |
| **Tax** | Complex multi-entity structures, carried interest taxation, K-1 preparation across jurisdictions |
| **HR / Talent** | Two distinct types: (1) firm-level HR, (2) portfolio talent leaders managing human capital across portfolio companies |
| **IT / Technology** | Firm systems plus Technology Operating Partners driving digital transformation at portfolio companies |
| **Marketing / Communications** | Firm branding, thought leadership, LP marketing materials. Often small team with agency support. |
| **Operations / COO** | Firm-level operational management, overseeing back-office functions |

### 3.4 How Functions Scale with Firm Size

| Firm Size | AUM | Headcount | Functional Structure |
|-----------|-----|-----------|---------------------|
| **Micro PE** | <$100M | 2-5 | Everyone invests. No dedicated non-investment functions. Accounting/legal outsourced. |
| **Small / Lower MM** | $100M-$1B | 5-25 | Generalists with functional depth. 1-2 dedicated IR/ops people. |
| **Middle Market** | $1B-$5B | 25-75 | Dedicated IR team, emerging operations team (5-25), in-house legal/compliance. |
| **Upper MM** | $3B-$10B | 50-150 | Dedicated functional teams: IR, operations (20-50), legal, compliance, finance, HR. |
| **Mega-Fund** | $10B+ | 150-5,000+ | Massive specialized departments. KKR Capstone: 80-100 ops. Bain Capital Portfolio Group: 115+. |

**Headcount efficiency:** Firms with <$250M AUM average 13.8 employees (111.6 per $1B AUM). Firms with >$10B AUM average 227.2 employees (9.4 per $1B AUM).

### 3.5 Complete Function Classification List

For automated classification, the recommended function categories:

| Function Code | Label | Examples |
|---------------|-------|----------|
| `GENERIC` | Generic (default investment role) | Analyst, Associate, VP, Principal, MD, Partner (with no functional modifier) |
| `IR` | Investor Relations | Head of IR, IR Associate, VP of Investor Relations |
| `CAP_MKTS` | Capital Markets | Capital Markets VP, Head of Capital Markets |
| `BD` | Business Development | BD Associate, Head of Origination, Business Development VP |
| `BD_CAP_MKTS` | BD + Capital Markets | Combined BD and capital markets roles |
| `OPS` | Portfolio Operations / Value Creation | Operating Partner, Operating MD, VP of Value Creation, Director of Portfolio Ops |
| `BOARD` | Board (primary function) | Independent Director, Board Member, Non-Executive Director |
| `CEO_PRES` | CEO / President | CEO, President, Co-CEO |
| `CFO` | CFO | Chief Financial Officer, Finance Director (at portfolio companies) |
| `COO` | COO | Chief Operating Officer |
| `CTO` | CTO | Chief Technology Officer |
| `CIO` | CIO | Chief Investment Officer, Chief Information Officer |
| `GC` | General Counsel | General Counsel, Chief Legal Officer |
| `COMPLIANCE` | Compliance | Chief Compliance Officer, Compliance Analyst, Deputy CCO |
| `LEGAL` | Legal / Counsel | Legal Counsel, Associate General Counsel, Paralegal |
| `ACCT_VAL` | Accounting / Valuation / Audit | Fund Controller, Fund Accountant, Valuation Analyst |
| `HR_TALENT` | HR / Talent | Head of Talent, HR Director, Chief People Officer |
| `IT` | IT / Technology | CTO (firm-level), IT Director, Technology Operating Partner |
| `MARKETING` | Marketing / Communications | Head of Marketing, Communications Director |
| `ADVISOR` | Advisor | Senior Advisor, Advisory Partner, Strategic Advisor |
| `CONSULTANT` | Consultant | Management Consultant, External Consultant |
| `EA` | Executive Assistant | Executive Assistant, Office Manager |
| `FOUNDER` | Founder (repeats as top-level title) | Founder, Co-Founder, Founding Partner |
| `OTHER` | Other / Unclassified | Titles that don't fit any category; flag for manual review |

---

## 4. C-Suite and Partnership Title Overlap

### 4.1 CEO vs. Managing Partner

Most PE firms historically did NOT have a CEO. The top title was Managing Partner (partnership-based). As firms went public (Blackstone 2007, KKR 2010, Apollo 2011, Carlyle 2012), they adopted CEO titles for corporate governance.

**Classification rule:** At non-public PE firms, Managing Partner = effective CEO. At public alternative asset managers, CEO and Managing Partner may coexist with CEO being senior.

| Firm | CEO | Chairman | Notes |
|------|-----|----------|-------|
| **Blackstone** | Schwarzman (Co-Founder, Chairman & CEO) | Same person | Jonathan Gray: President & COO |
| **KKR** | Bae & Nuttall (Co-CEOs since 2021) | Kravis & Roberts: Co-Executive Chairmen | Founder succession model |
| **Apollo** | Rowan (Co-Founder, CEO since 2021) | - | Leon Black departed 2021 |
| **Carlyle** | Harvey Schwartz (external hire, 2023) | Rubenstein & D'Aniello: Co-Executive Chairmen | First major PE firm to bring external CEO |

### 4.2 The Partner Taxonomy

| Partner Type | Economics | Engagement | Classification |
|-------------|-----------|------------|----------------|
| **Equity Partner** | Carry + GP ownership profit distribution | Full-time, active | Seniority: Senior; Function: GENERIC (usually) |
| **Salaried / Non-Equity Partner** | Salary + bonus, no carry | Full-time | Seniority: Mid-Senior to Senior; Function: varies |
| **Managing Partner** | Highest carry allocation (2-3% of pool) | Full-time, firm leadership | Seniority: Top; Function: CEO_PRES or GENERIC |
| **Senior Partner** | Higher carry than standard Partner | Full-time | Seniority: Senior; Function: GENERIC |
| **Operating Partner** | Base $392-661K, carry $4.3-12.6M at work | Full-time or part-time (varies) | Seniority: Senior; Function: OPS |
| **Venture Partner** | Carry on deals they originate, fees | Part-time | Seniority: Senior; Function: BD |
| **Senior Advisor** | Retainers $167-610K, carry $3-6M at work | Part-time (5-50% time) | Seniority: Senior; Function: ADVISOR |
| **Advisory Partner** | Varies - may be compensated or honorary | Part-time advisory | Seniority: Mid-Senior to Senior; Function: ADVISOR |
| **Founding Partner** | Typically highest carry, disproportionate economics | Varies - may transition to Chairman | Seniority: Top; Function: FOUNDER |
| **General Partner (as title)** | Full partnership economics | Full-time | Note: also a legal entity name |

### 4.3 Managing Director vs. Partner

At firms that distinguish them:
- **Partner** = equity ownership + carry + voice in firm governance
- **MD** = senior operational role that may or may not include partnership economics

At many firms they are interchangeable. Some firms use MD for credit teams and Partner for equity investing.

**Classification rule:** When both exist at the same firm, Partner > MD. When only one is used, treat as equivalent to the other. Default to the same seniority tier.

### 4.4 Senior Managing Director (SMD)

Blackstone's signature title. SMD serves as a member of the Executive Committee and is "expected to devote substantially all of their business time, skill, energies and attention to Blackstone." Other firms occasionally use this title but it is most strongly associated with Blackstone.

**Classification rule:** SMD = Senior (same tier as Partner), or Top if combined with firm leadership role.

### 4.5 Chairman Usage

| Type | Usage | Classification |
|------|-------|---------------|
| **Chairman & CEO** | Founder holding both titles at public firm | Seniority: Top; Function: CEO_PRES |
| **Co-Executive Chairman** | Founders stepped back from CEO but active | Seniority: Top; Function: BOARD (primary) |
| **Chairman Emeritus** | Fully retired founder, honorary | Seniority: Top (historical); Function: BOARD |
| **Executive Chairman** | Active governance, more than emeritus, less than CEO | Seniority: Top; Function: BOARD |

**Key pattern:** "Chairman" is increasingly a succession bridge - Founder/CEO > Executive Chairman > Chairman Emeritus.

### 4.6 Founder Title Interactions

Founder titles are persistent - they never go away. Common compounds:
- "Founder and Managing Partner" (active leadership)
- "Co-Founder and CEO" (public firm)
- "Co-Founder and Co-Executive Chairman" (stepped back)

**Classification rule:** Extract the functional role (CEO, Managing Partner, Chairman) for seniority classification. Flag FOUNDER as a secondary function attribute.

---

## 5. Edge Cases and Ambiguous Titles

### 5.1 Titles with Industry-Dependent Meaning

| Title | PE Meaning | Other Industry Meaning | Disambiguation Signal |
|-------|-----------|------------------------|----------------------|
| **Principal** | Mid-senior, pre-Partner (9-12 YoE). BUT at KKR = Senior Associate level (5 YoE). | Consulting: pre-Partner at BCG. Tech: very senior IC. Education: school head. | Industry context required. Within PE, firm identity modifies meaning. |
| **Director** | Pre-Partner investment professional | UK law: board member (fiduciary duty). Corporate: mid-management. Non-profit: Executive Director = CEO. | Geography + industry. In PE, check if firm is UK-origin. |
| **Vice President** | Mid-career (5-8 years). Goldman had 12,000 VPs out of 34,000 employees. | Corporate: true executive reporting to C-suite (1 of 5-10). | Industry context. PE/IB VP is 2-3 seniority levels lower than corporate VP. |
| **Associate** | Entry-to-junior (2-4 YoE) | Law firms: respected professional ($225K+). Retail: minimum wage entry. | Industry + company context. |
| **Managing Director** | Senior, potentially equivalent to Partner | IB: terminal employee title (no partnership). Corporate: regional/business unit leader. | In PE, check if firm also has "Partner" as a separate title. |

### 5.2 Compound / Dual-Hat Titles

Compound titles represent ~15-25% of LinkedIn titles. Common PE patterns:

- "Head of IR and Capital Markets" > Function: IR + CAP_MKTS; Seniority: from "Head of" modifier
- "CFO and COO" > Function: CFO (primary); Seniority: from C-level
- "Managing Director and Head of Europe" > Seniority: Senior; Function: GENERIC + geographic scope
- "Co-Founder & CEO" > Seniority: Top; Function: CEO_PRES + FOUNDER

**Handling rule:** Split on "&," "/," "and," "|," ",". Multi-label classify each segment. Never discard the original compound - compound title holders are often senior and the compoundness itself is a signal of seniority.

### 5.3 Adjacent Industry Titles in PE Databases

| Title Source | Example Titles | Classification Approach |
|-------------|----------------|------------------------|
| **Portfolio company executives** | CEO, CFO, COO, CTO, VP of Sales | Classify using corporate hierarchy, NOT PE hierarchy. A VP at a portfolio company is a true executive. |
| **Placement agents** | Managing Director at Park Hill, VP at Evercore Private Capital Advisory | These are IB/broker-dealer titles, not PE firm titles. |
| **Fund administrators** | Fund Controller, Fund Accountant | Function: ACCT_VAL. Seniority: from title level. May be outsourced (not a PE firm employee). |
| **Outside counsel** | Partner at Kirkland & Ellis, Associate at Simpson Thacher | Law firm hierarchy, not PE hierarchy. |
| **LP advisory committee members** | "LPAC Member" | Not a formal employee/title. Flag as LPAC role. |
| **Independent directors** | Independent Director, Non-Executive Director | Function: BOARD. Seniority: Senior (board-level). |

### 5.4 Special Role Classifications

| Title | Function | Seniority | Notes |
|-------|----------|-----------|-------|
| **Operating Partner** | OPS | Senior | Both function AND seniority marker. Can be full-time or part-time. |
| **Venture Partner** | BD | Senior | Part-time deal sourcing. More common in VC than PE buyout. |
| **Executive-in-Residence (EIR)** | ADVISOR | Senior | Short-term (6-12 months), between roles. |
| **Senior Advisor** | ADVISOR | Senior | Part-time (5-50% time), retainer-based. 3-4 board seats average. |
| **Secondee** | Use originating profession (LEGAL, ACCT_VAL) | From originating firm level | Temporary assignment, typically lawyer or accountant. Flag engagement_type = "Secondee." |
| **Chief of Staff** | OPS | Mid to Mid-Senior | Increasingly a power role in PE. Many grow into COO roles. |
| **Paralegal** | LEGAL | Junior to Mid | Knowledge of registered and private funds required. |
| **Student / Intern** | Pre-entry | Below Analyst | Flag engagement_type = "Intern" or "Student." Summer Analyst = undergraduate; Summer Associate = post-experience. |

---

## 6. Practical Classification Rules

### 6.1 Seniority Decision Tree

```
1. Does the title contain C-level tokens (CEO, CFO, COO, CTO, CIO, CMO)?
   YES -> Seniority: SENIOR or TOP (check if firm-level or portfolio company)

2. Does the title contain "Managing Partner" or "Founding Partner"?
   YES -> Seniority: TOP

3. Does the title contain "Senior Managing Director"?
   YES -> Seniority: SENIOR (Blackstone-style top tier)

4. Does the title contain "Partner" (without "Managing," "Operating," "Venture," "Advisory")?
   YES -> Seniority: SENIOR

5. Does the title contain "Managing Director" or "MD"?
   YES -> Seniority: SENIOR

6. Does the title contain "Operating Partner"?
   YES -> Seniority: SENIOR, Function: OPS

7. Does the title contain "Director" or "Principal" (without "Managing")?
   YES -> Seniority: MID-SENIOR
   UNLESS firm is KKR and title is "Principal" -> Seniority: MID (post-MBA level)

8. Does the title contain "Vice President" or "VP"?
   YES -> Seniority: MID
   UNLESS corporate context (not PE/IB) -> Seniority: SENIOR

9. Does the title contain "Investment Manager"?
   YES -> Geography check:
     US -> Seniority: MID-JUNIOR to MID
     UK -> Seniority: MID-JUNIOR to MID
     Germany -> Seniority: MID (= VP equivalent)
     Asia -> Seniority: MID-JUNIOR to MID

10. Does the title contain "Senior Associate"?
    YES -> Seniority: MID-JUNIOR

11. Does the title contain "Associate" (without "Senior")?
    YES -> Seniority: JUNIOR

12. Does the title contain "Analyst"?
    YES -> Seniority: ENTRY

13. Does the title contain "Intern" or "Student" or "Summer"?
    YES -> Seniority: PRE-ENTRY
```

### 6.2 Function Decision Tree

```
1. Does the title contain IR/Investor Relations tokens?
   ("Investor Relations," "IR," "LP Relations," "Client Services") -> Function: IR

2. Does the title contain Capital Markets tokens?
   ("Capital Markets," "Debt Capital," "Leveraged Finance") -> Function: CAP_MKTS

3. Does the title contain both BD and Capital Markets tokens?
   -> Function: BD_CAP_MKTS

4. Does the title contain BD/Origination tokens?
   ("Business Development," "BD," "Origination," "Deal Sourcing") -> Function: BD

5. Does the title contain Operations/Value Creation tokens?
   ("Operating," "Portfolio Operations," "Value Creation," "Capstone") -> Function: OPS

6. Does the title contain C-suite tokens?
   CEO/President -> CEO_PRES; CFO -> CFO; COO -> COO; CTO -> CTO; CIO -> CIO

7. Does the title contain Legal tokens?
   ("General Counsel," "GC," "Legal," "Counsel") -> Function: GC or LEGAL

8. Does the title contain Compliance tokens?
   ("Compliance," "CCO") -> Function: COMPLIANCE

9. Does the title contain Accounting/Finance tokens?
   ("Fund Controller," "Fund Accountant," "Valuation," "Audit") -> Function: ACCT_VAL

10. Does the title contain HR/Talent tokens?
    ("HR," "Human Resources," "Talent," "People") -> Function: HR_TALENT

11. Does the title contain IT tokens?
    ("IT," "Information Technology," "Systems") -> Function: IT

12. Does the title contain Board tokens?
    ("Board," "Non-Executive Director," "Independent Director," "Chairman," "Chairperson") -> Function: BOARD

13. Does the title contain Advisor tokens?
    ("Advisor," "Advisory," "Senior Advisor," "EIR," "Executive in Residence") -> Function: ADVISOR

14. Does the title contain EA tokens?
    ("Executive Assistant," "EA," "Office Manager") -> Function: EA

15. None of the above?
    -> Function: GENERIC (default investment role)
```

### 6.3 Confidence Markers

| Classification | Confidence | When This Applies |
|---------------|------------|-------------------|
| **Universal** (always correct) | High | "Managing Partner" = TOP seniority. "Analyst" = ENTRY. "Investor Relations" = IR function. Standard tokens with unambiguous meaning across all PE contexts. |
| **Context-dependent** (correct with additional signals) | Medium | "Investment Manager" (needs geography). "Director" (needs firm origin + geography). "Principal" (needs firm identity). "VP" (needs industry - PE vs. corporate). |
| **Ambiguous** (needs human review or external data) | Low | "Committee/Exec" (unclear function). Compound titles with conflicting signals. Titles from adjacent industries in PE databases. "Partner" at micro-funds (may represent different seniority than at mega-funds). |

### 6.4 Firm Size as Classification Modifier

| Signal | Rule |
|--------|------|
| AUM < $100M, headcount < 10 | Deflate titles by 1 seniority level (a "Partner" here may have equivalent responsibility to a VP/Principal at a larger fund) |
| AUM $100M-$1B | Titles roughly at face value but less granular |
| AUM $1B-$10B | Standard hierarchy applies |
| AUM > $10B | Titles are well-calibrated; may have additional tiers (SMD at Blackstone) |

---

## 7. Glossary

PE-specific terms that have different meanings in other industries:

| Term | PE Meaning | Common Misinterpretation |
|------|-----------|-------------------------|
| **Associate** | Entry-to-junior investment professional (2-4 YoE) | Senior professional (law), generic entry (retail) |
| **Vice President** | Mid-career (5-8 YoE), manages deal teams | True executive reporting to CEO (corporate) |
| **Director** | Pre-Partner investment professional (9-12 YoE) | Mid-management (corporate), board member (UK law) |
| **Principal** | Pre-Partner (9-12 YoE at most firms; 5 YoE at KKR) | Pre-Partner in consulting, senior IC in tech, school head |
| **Managing Director** | Senior, may = Partner or one level below | Terminal IB title (no partnership), regional GM (corporate) |
| **Partner** | Equity owner in the management company with carried interest | Law firm partner (different economics), consulting partner |
| **General Partner** | Can mean: (1) the legal entity atop the fund, or (2) a person's title indicating IC participation | General business partner (informal) |
| **Operating Partner** | PE ops professional working with portfolio companies. Both function + seniority marker. | Generic "partner" in operations (corporate) |
| **Carry / Carried Interest** | GP's ~20% share of fund profits above hurdle rate | Not used outside PE/VC/HF |
| **Investment Committee (IC)** | Decision-making body that approves investments | Generic corporate committee |
| **Deal Team** | Group of PE professionals executing a specific transaction | Project team (corporate equivalent) |
| **Dry Powder** | Committed but undeployed capital | Not used outside PE |
| **Investment Manager** | US: rarely used/junior. Germany: = VP. UK: SA-to-VP range. Asia: SA/VP hybrid. | Asset management company (different industry) |

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| Job Title Decomposition (domain-agnostic) (not included) | Foundational reference. This document is the PE-specific overlay. |
| [PE Fund Sizes and Structures Reference](private-equity-fund-sizes-structures-terminology.md) | Firm size segments used as classification modifiers. Fund structure context. |
| [PE Capital Markets Professional - Buyer Primer](pe-capital-markets-professional-buyer-primer.md) | Buyer persona for one PE function (capital markets). Uses seniority/function from this doc. |
| [LinkedIn Profile Verification Agent - PE/Capital Markets](linkedin-profile-verification-pe-capital-markets.md) | PE-primed identity verification. Title signals feed into verification logic. |
