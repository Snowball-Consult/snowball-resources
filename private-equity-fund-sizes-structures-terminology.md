# Private Equity Fund Sizes and Structures Reference

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Comprehensive reference for identifying, categorizing, and extracting PE fund size information from unstructured sources |
| **Trigger** | Processing PE fund data, understanding fund structures, disambiguating fund types, extracting fund sizes from web sources |
| **Scope** | PE fund structure taxonomy, fund size terminology, market segment classifications, fund lifecycle and vintage conventions, data sources and reliability, disambiguation of non-PE vehicles, extraction patterns |
| **Not In Scope** | Specific fund performance analysis, portfolio company evaluation, PE investment strategy selection, deal sourcing |
| **Dependencies** | None |
| **Keywords** | PE, private equity, fund size, committed capital, AUM, NAV, flagship fund, continuation vehicle, LBO, buyout, fund lifecycle, vintage year, PitchBook, Preqin, Form D, LP, GP, dry powder, mega-fund, mid-market |
| **Domain Tags** | private-equity, PE, fund sizes, fund structures, buyout |
| **Maturity** | Working |
| **Last Reviewed** | 2026-02-05 |

---

## Core Insight

**"Fund size" almost always means committed capital at final close for the flagship fund - not AUM, not NAV, not credit funds, and not continuation vehicles.** Misclassifying these related-but-distinct concepts is the most common extraction error.

Private equity fund structures are deliberately complex for tax, regulatory, and investor accommodation reasons. A single PE firm like Blackstone manages dozens of distinct fund families across buyout, credit, real estate, and infrastructure - each with parallel vehicles, feeders, and co-investment sidecars. The challenge isn't finding fund size data; it's ensuring the extracted figure represents what it claims to represent.

---

## PE Fund Structure Taxonomy and Vehicle Types

### The Flagship Fund is the Definitive Measure

A **flagship fund** (also called the main fund or primary fund) is the sequentially-numbered, blind-pool vehicle that represents a PE firm's core investment strategy. When industry participants reference "Apollo's latest fund" or "KKR raised $20 billion," they mean the flagship buyout fund. Flagship funds follow predictable naming patterns: **[Firm Name] + [Strategy/Product] + [Roman Numeral] + [Geographic Focus]**.

Examples of flagship buyout funds include Blackstone Capital Partners IX ($20.7B), Apollo Investment Fund X ($20B), KKR North America Fund XIV, Carlyle Partners VIII, and Advent International GPE X. The Roman numeral indicates generation - Fund IX is the ninth flagship in that series. **The highest numeral typically represents the newest/current fund**, though firms may run multiple flagship series simultaneously (e.g., KKR North America Fund XIV while also raising KKR Asian Fund IV).

Fund numbering conventions are remarkably consistent: Roman numerals dominate (I, II, III, IV, V, VI, VII, VIII, IX, X, XI, XII...), with sequential incrementing for each successor fund. Numbering resets occur only with major strategy changes, spinoffs, or new product lines. Arabic numerals occasionally appear but are less common in traditional buyout franchises.

### Critical Non-Flagship Vehicle Types Requiring Disambiguation

**Continuation Vehicles (CVs)** transfer existing portfolio companies from a fund nearing its term into a newly-created SPV, allowing the GP to extend holding periods for "trophy assets." CVs provide liquidity options to existing LPs (cash out at current valuation or roll into the new vehicle) while admitting new secondary buyers. **CVs are NOT new flagship funds** - they contain existing assets being recapitalized. GP-led transactions grew from $9B in 2015 to $51B in 2023, representing approximately 48% of the secondaries market. Identifying keywords include: "continuation fund," "continuation vehicle," "GP-led secondary," "single-asset continuation," "roll or cash out," and "extending holding period."

**Parallel Funds** are separate legal entities investing pari passu (proportionally) with the main fund, structured to accommodate specific investor requirements - EU investors requiring Luxembourg vehicles, US investors requiring Delaware structures, or tax-exempt investors needing offshore wrappers. Parallel funds are economically identical to the flagship; their capital should be **aggregated** with the main fund total. Naming patterns include geographic suffixes: "[Fund Name] (Cayman)," "[Fund Name]-A/-B/-C," or "[Fund Name] Offshore."

**Co-Investment Vehicles** allow specific LPs to invest directly in individual deals alongside the main fund, typically with reduced or no fees. These are deal-specific (not blind-pool), representing additional capital deployed with different economics. Keywords include: "co-investment," "co-invest," "sidecar," "alongside the fund," and "deal-by-deal."

**Annex/Top-Up Funds** provide supplementary capital beyond the main fund - annex funds support follow-on investments after the investment period ends, while top-up funds participate in new opportunities during market dislocations. **Sidecar/Overage Funds** handle excess deal capacity when transactions exceed concentration limits.

**Separately Managed Accounts (SMAs)** are single-investor customized portfolios with bespoke terms, often not appearing in standard fund databases. Keywords include: "separately managed account," "fund of one," "dedicated account," and "customized mandate."

**Funds of Funds (FOF)** invest in portfolios of other PE funds rather than directly in companies. Major FOF managers include AlpInvest, Hamilton Lane, Pantheon, HarbourVest, and Adams Street Partners. FOFs represent allocator capital with two layers of fees.

**Secondary Funds** purchase existing LP interests or fund positions from selling LPs, providing liquidity at discounts to NAV. Distinguish from GP-led secondaries (continuation vehicles).

### Fund Families at Multi-Strategy Firms

Major PE firms manage multiple simultaneous fund families across distinct strategies. Understanding this structure prevents misattribution:

**Blackstone (~$1.27T AUM)** manages Corporate PE (Blackstone Capital Partners series), Real Estate (Blackstone Real Estate Partners/BREIT), Credit (BCRED, GSO), Secondaries (Strategic Partners), and Infrastructure (Blackstone Infrastructure Partners). The flagship buyout is the "BCP" series.

**Apollo (~$785B AUM)** derives most AUM from Credit ($392B) versus traditional PE (~$99B). Apollo Investment Fund X/XI represents the flagship buyout; Apollo Credit and Apollo Debt represent separate strategies.

**KKR (~$664B AUM)** runs geographic buyout franchises: KKR North America Fund, KKR European Fund, and KKR Asian Fund series, alongside separate Credit, Infrastructure, and Real Estate platforms.

**Carlyle (~$375B AUM)** similarly operates US Buyout (Carlyle Partners), Europe Buyout (Carlyle Europe Partners), Asia Buyout (Carlyle Asia Partners), plus Credit, Real Estate, and Investment Solutions (AlpInvest FOF).

---

## Fund Size Terminology

### Core Terms That Define "Fund Size"

**Committed Capital / Capital Commitments** is the definitive fund size metric - the total amount investors contractually agree to contribute over the fund's lifetime. When press releases announce a "$5 billion fund," they mean $5 billion in committed capital. This figure is fixed at the time of commitment and forms the basis for management fee calculations during the investment period.

**Total Commitments** aggregates all LP commitments plus the GP commitment (typically 1-3% of fund size).

**Target Size** represents the fundraising goal announced at launch - it may differ from the final close amount. Target appears in Form D filings ("Total Offering Amount"), press releases, and marketing materials.

**Hard Cap** is the absolute maximum a fund may accept, specified in the Limited Partnership Agreement. Funds cannot exceed hard caps without LP consent. Per Preqin data, only 20% of funds failed to reach hard caps in 2017 (a record low), and 56% of funds in 2015-2017 met or exceeded hard caps. Hard caps typically sit 10-20% above target.

**Soft Cap** usage varies - it sometimes means target size, sometimes the minimum viable fund size to execute the business plan.

**Final Close Amount** is the official, definitive fund size - total committed capital when fundraising concludes. This figure should be used for fund size extraction.

**First Close Amount** represents capital committed at the initial close, allowing the GP to begin investing. First closes typically represent 25-50% of target; a strong first close signals investor confidence.

### Capital Deployment and Lifecycle Terms

**Called Capital / Drawn Capital / Paid-In Capital (PIC)** is the portion of committed capital that has been transferred from LPs to the fund. The relationship is: Called Capital <= Committed Capital.

**Uncalled Capital / Unfunded Commitments** represents committed capital not yet called - the mathematical difference between committed and called capital.

**Dry Powder** is essentially synonymous with uncalled capital at the fund level. At the industry level, dry powder represents aggregate uninvested capital across all PE funds - approximately **$1.1 trillion in buyout funds** and **$3.9 trillion across all private capital strategies** as of recent Bain reports.

**Invested Capital / Deployed Capital** refers to capital actually used to make investments (called capital minus fees/expenses).

### Performance and Valuation Terms (NOT Fund Size)

**AUM (Assets Under Management)** is a firm-level metric representing the total market value of all assets across all funds. **This is NOT fund size.** AUM fluctuates with portfolio valuations, while committed capital is fixed. A firm might report "$50B AUM" while its latest flagship fund is $8B. In PE, firm AUM often reflects the sum of committed capital still managed across active funds plus permanent-capital vehicles.

**NAV (Net Asset Value)** represents the current market value of a fund's holdings minus liabilities - essentially "residual value." NAV fluctuates based on portfolio performance and can exceed or fall below original fund size.

**TVPI (Total Value to Paid-In Capital)** equals (Distributions + NAV) / Paid-In Capital. A TVPI of 2.0x means the fund has generated 2x value on invested capital. **DPI (Distributions to Paid-In Capital)** measures realized/liquid returns; **RVPI (Residual Value to Paid-In Capital)** measures unrealized value. The relationship: **TVPI = DPI + RVPI**.

### Number Formats and Currency Conventions

Fund sizes appear in multiple formats that must be normalized:

| Format | Equivalent |
|--------|------------|
| $500M, $500m, $500MM, $500mm, $500mn | 500,000,000 |
| $5B, $5b, $5bn, $5BN, 5 billion | 5,000,000,000 |
| $0.5B, $500 million, 500 million dollars | 500,000,000 |

The "MM" convention (double-M for million) derives from Roman numerals: M = 1,000, so MM = 1,000 x 1,000 = 1,000,000. This is traditional US investment banking convention; single "m" or "mn" is more common in European contexts.

**Currency considerations:** Most US funds denominate in USD. European funds may use EUR or GBP. Data providers typically convert to USD equivalent. Note original currency when available. "Billion" is now globally standardized to 10^9 (the historical European "milliard" is obsolete).

---

## Market Segment Classifications and Size Thresholds

### Classification Thresholds Vary by Source

Different industry authorities use different dollar thresholds for fund size classification. This inconsistency requires noting the source when categorizing funds:

**PitchBook Thresholds:**
- **Mega-Fund:** >$5 billion USD or EUR
- **Middle-Market:** $100 million - $5 billion USD or EUR

**Preqin Thresholds (Buyout Funds):**
- **Small:** <=$500 million
- **Medium:** $501 million - $1.5 billion
- **Large:** $1.5 billion - $4.5 billion
- **Mega:** >$4.5 billion

**Bain & Company** uses $5 billion+ as the mega-fund threshold, noting that for the first time in a decade, not a single buyout fund >$5B closed in Q1 2024.

### Deal Size and Company Value Classifications

Market segments also apply to target company characteristics:

| Segment | Fund Size | Deal/Enterprise Value | Target Company Revenue |
|---------|-----------|----------------------|------------------------|
| Micro/Small | <$100M | <$25M | <$10M |
| Lower Mid-Market | $100M-$500M | $25M-$100M | $10M-$50M |
| Core Mid-Market | $500M-$2B | $100M-$500M | $50M-$500M |
| Upper Mid-Market | $2B-$5B | $500M-$1B | $500M-$1B |
| Large/Mega | $5B+ | $1B+ | $1B+ |

### Historical Threshold Evolution

What constitutes "mega" has inflated significantly:

| Era | "Large" Threshold | "Mega" Threshold | Context |
|-----|-------------------|------------------|---------|
| 2005-2010 | $1B+ | $5B+ | Pre-financial crisis |
| 2010-2015 | $2-3B+ | $5B+ | Post-GFC recovery |
| 2020-2024 | $5B+ | Some argue $10B+ | Threshold creep |

The $5B mega-fund threshold has remained remarkably stable even as individual funds have grown dramatically - Blackstone raised a $24.1B real estate fund; EQT X closed at $24B; Carlyle has targeted $27B for its 13th flagship. Industry observers have predicted "super-mega-funds" of $50B.

### Regional Variations

The same dollar amount classifies differently by geography:

**US Market:** Most competitive, largest average fund sizes. $5B+ clearly mega-cap; $500M considered lower mid-market.

**European Market:** Slightly smaller average sizes. Mid-market typically EUR 50M-500M enterprise value. Same dollar threshold may represent larger relative position.

**Asia-Pacific:** $1B+ funds considered large in most APAC markets outside Greater China. RMB-denominated funds often excluded from global statistics to avoid double-counting.

**Emerging Markets:** $500M fund would be mega-cap in most EM contexts; $50M-$100M may be "large."

---

## Fund Lifecycle, Timing, and Vintage Year Conventions

### Complete Lifecycle Stages

**Fund Formation (months to years):** GP develops legal structure, investment strategy, and governing documents. Minimal public information.

**Fundraising Initiation ("In Market"):** GP launches marketing, conducts roadshows, distributes PPM. Duration: **6-18+ months** (2025 average approximately 18 months, up from 13 months during 2020-2024). Regulatory filings (Form D) and press releases begin appearing.

**First Close:** First investors formally commit; fund becomes operational. Typically 25-50% of target at first close. Press language: "held first close," "initial closing," "launched with $X in commitments."

**Subsequent Closes:** Additional investors join over 6-12 months; later investors pay equalization interest to compensate earlier investors.

**Final Close:** Fundraising ends; no new LPs admitted; total fund size finalized. Typically 12-18 months from first close. Press language: "final close," "hard close," "completed fundraising," "closed at $X."

**Investment Period (Years 1-5):** GP actively deploys capital. Typical pace: 40-60% called by Year 2, 75-85% by Year 4. **The "70-75% deployed" threshold** typically triggers successor fund launch.

**Harvest Period (Years 5-10+):** GP focuses on value creation and exits. Distributions to LPs accelerate.

**Fund Term:** Standard 10-year life from first close, with "2+1+1" extension structure (10 years + 2 one-year GP discretionary extensions + additional years with LP consent). **Actual average fund life is 14 years** for buyout funds due to extensions.

### Vintage Year Determination

**Vintage year** is the year a fund first deploys capital into investments - used for benchmarking performance against peers facing similar market conditions. **Critically, vintage year is NOT the year of final close.**

Data providers assign vintage differently:

| Provider | Primary Definition |
|----------|-------------------|
| Cambridge Associates | Year of first cash flow (first LP capital call) |
| PitchBook | Year fund makes first investment |
| Preqin | Year of first investment/drawdown |

A fund may hold first close in December 2023 but not make its first investment until January 2024, resulting in a 2024 vintage despite 2023 fundraising. Subscription credit facilities complicate this further - GPs may make investments before calling LP capital.

### Deployment Signals and Successor Fund Timing

**"75% deployed"** as a signal for successor fund launch can mean different things:
- "Invested in portfolio companies" (strictest interpretation)
- "Invested or committed" (includes signed deals pending close)
- "Invested, committed, or reserved" (includes follow-on reserves and fees)

Per Goodwin analysis: 80%+ of fund LPAs specify a 70-75% threshold; approximately 15% require 80%+. VC funds often use 65-70% thresholds due to higher follow-on reserve requirements.

Typical successor fund timing: Start fundraising in Year 3-4 of predecessor fund; first close in Year 4-5; final close in Year 5-6. This creates overlap where both funds may be making investments simultaneously with allocation policies governing deal splits.

---

## Data Sources Landscape and Reliability Hierarchy

### Major Data Providers Compared

**PitchBook (Morningstar):** Covers 115,000+ funds, 63,000+ firms, 3.6M+ VC/PE-backed companies. Strongest for deal-level and company data. Sources include SEC filings, FOIA requests to public pensions, direct GP/LP outreach, and proprietary research. Subscription required (~$20,000-30,000+/year).

**Preqin (acquired by BlackRock March 2025):** Covers 124,000+ funds. Industry standard for fund performance benchmarks and LP-GP relationship data. Strong on institutional investor behavior and allocations. Sources include FOIA requests, direct submissions, regulatory filings. Subscription required (~$15,000-25,000+/year).

**Cambridge Associates:** Covers 9,900+ funds from 2,400+ managers with unique methodology - data sourced **directly from quarterly unaudited and annual audited fund financial statements** provided by GPs. Does NOT use FOIA requests, regulatory filings, or third-party data. Considered highest quality for benchmarking; focuses only on "institutional quality" funds.

**Burgiss:** Data sourced exclusively from LPs including complete transactional and valuation history. Fewer funds than Preqin/PitchBook but highly accurate due to LP-verified records.

**S&P Capital IQ:** 90,000+ PE/VC funds (supplemented via Preqin partnership), 109,000+ public companies, 58M+ private companies. Strong for transactional data; generous downloading (10,000 results/download).

**CEPRES:** 16,500+ funds, 143,000+ deals with unique look-through data to portfolio company P&L level. Data sourced directly from GPs and LPs with 100% verification claims. Partnership with ILPA and Bain DealEdge.

### SEC Filings as Primary Sources

**Form D** is the foundational regulatory source for PE fund information:
- "Total Offering Amount" = target fund size
- "Total Amount Sold" = capital raised to date
- "Pooled Investment Fund" = fund classification
- Filed within 15 days of first sale; annual amendments while actively fundraising

**Limitations:** Minimal disclosure compared to public offerings; fund size may show "indefinite"; self-reported by issuers.

**Form ADV** provides adviser-level data:
- Part 1A, Schedule D, Section 7.B.1 lists all private funds managed
- Shows fund name, type (PE/VC/hedge/real estate), gross asset value
- Annual updating within 90 days of fiscal year end

**Form PF** is confidential - filed with SEC for systemic risk monitoring but NOT publicly available. Large PE advisers ($2B+ in PE AUM) file quarterly with detailed fund-level data.

### Public Pension Disclosures as Fund Size Sources

**CalSTRS (California State Teachers' Retirement System)** provides the most detailed disclosure among US public pensions: fund name, year acquired, capital committed, capital contributed, capital distributed, and IRR for each PE fund investment. This data reveals unfunded commitments (committed minus contributed) and realized gains (distributions) not available elsewhere.

**CalPERS** lists PE firms invested in, discloses commitments, amounts invested, and performance quarterly. Annual disclosure of fees and carried interest.

**State-by-state transparency varies significantly:**
- **Most transparent:** California (mandatory affirmative disclosure), North Carolina, Pennsylvania, South Carolina
- **Less transparent:** Massachusetts, Alaska (explicit exemptions for alternative investment confidential information)

**FOIA requests** can obtain fund-level data from state pension funds including: fund name, vintage year, commitment size, contributions, distributions, and fair market value. Protected information typically includes portfolio company-level details and proprietary fund terms.

### Source Reliability Hierarchy

For data extraction and verification, prioritize sources in this order:

1. **Highest reliability:** SEC EDGAR filings (Form D, Form ADV) - official, legally required
2. **High:** Official press releases from firm websites, Business Wire, PR Newswire
3. **High:** Cambridge Associates/Burgiss data (verified GP/LP sourced)
4. **Medium-High:** Major news outlets (WSJ, FT, Bloomberg) original reporting
5. **Medium:** PitchBook/Preqin (mix of verified and FOIA-sourced)
6. **Medium:** Public pension fund disclosures
7. **Lower:** Secondary news aggregation, unconfirmed reports

### Common Data Quality Issues

**Conflicting fund sizes across sources** occur due to: different reporting dates (interim vs final close), inclusion/exclusion of co-investment vehicles, currency conversion timing, and related entity treatment. **Resolution:** Prefer primary sources (Form D, official press releases); use most recent filing date; verify whether amount includes associated vehicles.

**Stale data:** Databases may not update quickly after fund events. **Resolution:** Cross-reference multiple sources; check filing dates; prefer sources with clear "as of" dates.

**Interim vs final close confusion:** Databases may show interim close as final size or maintain multiple entries for the same fund at different close amounts. **Resolution:** Check Form D amendment dates; look for explicit "final close" language in press releases.

**Sample and survivorship bias:** FOIA-sourced data only covers public LP universe; underperforming managers may withhold data. **Resolution:** Use multiple providers; recognize limitations.

---

## Disambiguation: Fund Types That Look Like PE But Aren't

### Credit/Debt Funds (Most Common Confusion)

Credit funds invest in debt instruments rather than equity ownership. Same firm names create confusion - Apollo's largest segment is Credit ($392B) versus traditional PE (~$99B); Blackstone manages BCRED alongside BCP.

**Identifying keywords:** "credit," "debt," "lending," "direct lending," "senior secured," "mezzanine," "floating rate," "first lien," "second lien," "unitranche," "CLO," "BDC," "distressed debt," "private credit"

**Why exclude:** Different asset class with different return profile (target 8-15% IRR vs 18-25% for buyout); no operational control; income/yield focused.

### Real Estate Funds

**Keywords:** "real estate," "property," "REIT," "BREIT," "BREP," "multifamily," "office," "industrial," "logistics," "cap rate," "NOI," "core/core-plus/value-add/opportunistic"

**Why exclude:** Different asset class with different valuation metrics (cap rates, NOI).

### Infrastructure Funds

**Keywords:** "infrastructure," "infra," "utilities," "transportation," "toll roads," "airports," "ports," "pipelines," "energy transition," "digital infrastructure," "renewables"

**Why exclude:** Different asset class with longer holding periods (10-20+ years), often regulated returns.

### Venture Capital Funds

**Keywords:** "venture," "VC," "seed," "Series A/B/C/D," "early-stage," "startup," "growth-stage," "pre-revenue"

**Why exclude:** Earlier stage companies, no leverage, minority stakes typical, different risk profile.

### Growth Equity Funds (Judgment Required)

Growth equity represents a gray area - sometimes classified as PE, sometimes separate:

**Include when:** Control-oriented growth, firm is traditionally buyout-focused, leverage used
**Exclude when:** Pure minority stakes (20-40% ownership), no leverage, no operational control

**Keywords:** "growth equity," "growth fund," "expansion capital," "minority investment"

### BDCs (Business Development Companies)

**Keywords:** "BDC," "Business Development Company," ticker symbols (NYSE:ARCC, FSK, HTGC, MAIN)

**Why exclude:** Publicly traded, primarily debt investments (70%+), SEC regulated, 90% income distribution requirement, retail accessible.

### SPACs

**Keywords:** "SPAC," "blank check company," "de-SPAC," "business combination"

**Why exclude:** Single-acquisition vehicle, public shareholders, different timeline (18-24 months vs 10 years), different economics.

---

## Practical Extraction Patterns and Parsing Guidance

### Press Release Fund Size Patterns

**High-confidence extraction patterns:**
- "[Fund Name] raised $X billion"
- "final close at $X"
- "committed capital of $X"
- "[Fund Name] ($X billion)"
- "the $X billion fund"
- "[Firm] announces final close of [Fund] at $X"
- "closed [Fund] above $X hard cap"

**Medium-confidence (requires verification):**
- "targeting $X" (target, not final)
- "with a hard cap of $X" (maximum, not actual)
- "first close of $X" (partial, not final)

**Low-confidence/exclude:**
- "AUM of $X" (firm-level, not fund)
- "manages $X" (ambiguous)
- "portfolio value of $X" (NAV, not committed capital)
- "invested $X" (deployed capital, not fund size)

### Red Flag Phrases Indicating Non-Flagship Vehicles

Watch for these terms that suggest the entity is NOT a flagship buyout fund:
- **Continuation:** "continuation fund," "CV," "GP-led secondary"
- **Credit/debt:** "credit," "lending," "loan," "debt fund"
- **Real estate:** "real estate," "property," "REIT"
- **Infrastructure:** "infrastructure," "infra"
- **Venture:** "venture," "seed," "early-stage"
- **Other vehicles:** "co-invest," "sidecar," "feeder," "offshore," "blocker," "SPAC," "BDC"

### Normalizing Number Formats

Standardize all extracted values to consistent format:

| Raw Format | Normalized Value |
|------------|------------------|
| $500M, $500m, $500MM, $500mm, $500mn, $0.5B, $0.5bn, $500 million | 500,000,000 |
| $5B, $5b, $5bn, $5BN, 5 billion, $5,000M | 5,000,000,000 |
| EUR 2.5bn | 2,500,000,000 EUR (note currency) |

### Currency Handling

- Default assumption: USD unless otherwise specified
- Note original currency when EUR, GBP, or other currencies appear
- Mark currency uncertainty explicitly
- Exchange rate at time of close typically used for historical comparisons

### Verification Checklist for Extracted Fund Data

Before accepting an extracted fund size as valid:

1. **Is this the flagship fund?** Check for Roman numeral sequencing, absence of credit/real estate/infrastructure keywords
2. **Is this final close or interim?** Look for explicit "final close" language
3. **Does the amount include related vehicles?** Note if press release mentions "including co-investment" or "including parallel funds"
4. **Is the source primary?** Prefer SEC filings and official press releases over secondary reporting
5. **What currency is this?** Note if non-USD and whether conversion has been applied
6. **How recent is this data?** Check filing/publication dates

---

## Comprehensive Glossary of PE Terminology

### Fund Structure Terms

| Term | Definition |
|------|------------|
| Limited Partnership (LP) | Primary legal structure for PE funds |
| General Partner (GP) | Fund manager entity; makes investment decisions; unlimited liability |
| Limited Partner (LP) | Passive investors providing capital; liability limited to investment |
| LPA | Limited Partnership Agreement - governing contract defining all terms |
| Blind Pool | Structure where investors commit before investments are identified |
| AIV | Alternative Investment Vehicle - separate entity for tax/regulatory reasons |
| Master-Feeder | Multiple feeder funds investing into single master fund |

### Size and Financial Terms

| Term | Definition |
|------|------------|
| Committed Capital | Total LP pledges = "fund size" |
| Called Capital / PIC | Amount actually transferred from LPs |
| Uncalled Capital / Dry Powder | Committed but not yet called |
| AUM | Total assets managed firm-wide (NOT fund size) |
| NAV | Current portfolio value minus liabilities |
| Target Size | Fundraising goal |
| Hard Cap | Maximum allowed; cannot exceed |
| Soft Cap | Initial target; can be exceeded to hard cap |
| Management Fee | Annual fee (typically 1.5-2% of committed) |
| Carried Interest | GP profit share (typically 20%) above hurdle |
| Hurdle Rate | Minimum return (typically 8%) before carry |

### Lifecycle Terms

| Term | Definition |
|------|------------|
| First Close | Initial closing; fund operational |
| Final Close | Fundraising ends; fund size finalized |
| Investment Period | Active deployment (typically Years 1-5) |
| Harvest Period | Exit/distribution focus (Years 5-10+) |
| Vintage Year | Year of first capital deployment |
| Capital Call / Drawdown | GP request for LP to transfer capital |
| Distribution | Return of capital/profits to LPs |
| Recycling | Reinvesting exit proceeds into new investments |
| Clawback | GP returns excess carry if returns fall below hurdle |

### Performance Terms

| Term | Definition | Relationship |
|------|------------|--------------|
| IRR | Annualized return accounting for cash flow timing | Primary PE metric |
| Gross IRR | Before fees and carry | |
| Net IRR | After all fees and carry | What LPs receive |
| MOIC | Total value / invested capital | Absolute return multiple |
| TVPI | (Distributions + NAV) / Paid-In | Comprehensive measure |
| DPI | Distributions / Paid-In | Realized returns |
| RVPI | NAV / Paid-In | Unrealized value |
| | | **TVPI = DPI + RVPI** |

### Deal Terms

| Term | Definition |
|------|------------|
| LBO | Leveraged Buyout - acquisition using significant debt |
| MBO | Management Buyout - LBO led by existing management |
| Platform Company | Initial acquisition as foundation for add-ons |
| Add-on / Bolt-on | Smaller acquisition combined with platform |
| Roll-up | Acquiring multiple companies in fragmented industry |
| Carve-out | Acquiring division from larger company |
| Take-Private | Acquiring public company and delisting |
| Dividend Recap | Borrowing to pay special dividend to sponsors |
| Rollover Equity | Seller's equity retained in new structure |

### Regulatory Terms

| Term | Definition |
|------|------------|
| Form D | SEC filing for Reg D private placement exemption |
| Form ADV | SEC investment adviser registration |
| Form PF | Private fund reporting (confidential) |
| PPM | Private Placement Memorandum - offering document |
| Accredited Investor | Meets SEC wealth/income thresholds |
| Qualified Purchaser | Higher threshold ($5M+ investments) |
| ILPA | Institutional Limited Partners Association |
| AIFMD | Alternative Investment Fund Managers Directive (EU) |

### Common Abbreviations

| Abbreviation | Full Term |
|--------------|-----------|
| PE | Private Equity |
| VC | Venture Capital |
| LP | Limited Partner |
| GP | General Partner |
| AUM | Assets Under Management |
| NAV | Net Asset Value |
| IRR | Internal Rate of Return |
| MOIC | Multiple on Invested Capital |
| TVPI | Total Value to Paid-In |
| DPI | Distributions to Paid-In |
| LBO | Leveraged Buyout |
| LPA | Limited Partnership Agreement |
| PPM | Private Placement Memorandum |
| LPAC | LP Advisory Committee |
| BDC | Business Development Company |
| SPAC | Special Purpose Acquisition Company |
| CV | Continuation Vehicle |
| SMA | Separately Managed Account |

---

## Regulatory and Reporting Context

### US Regulatory Framework

PE funds are generally exempt from SEC registration under the Investment Company Act of 1940 via Section 3(c)(1) (fewer than 100 beneficial owners) or Section 3(c)(7) (qualified purchasers only). However, advisers managing $150M+ in private fund assets must register with the SEC.

**Form D** must be filed within 15 days of first sale of securities, with annual amendments while fundraising. This is the primary public source of fund size data.

**Form ADV** provides ongoing adviser registration including lists of all private funds managed with gross asset values.

**Form PF** requires enhanced reporting for large PE advisers ($2B+ in PE AUM), including quarterly filings with detailed fund-level data - but this information is confidential and not publicly accessible.

### International Regulatory Sources

**UK (FCA):** Full-scope UK AIFMs file Annex IV transparency reports including NAV and leverage, but these are not publicly available. HM Treasury is consulting on streamlined frameworks with tiered approaches based on NAV thresholds.

**EU (AIFMD):** Article 24 requires reporting on exposures, leverage, and risk profiles. AIFMD II (effective 2026) will require enhanced transparency. Reports go to national competent authorities but are not publicly accessible.

**Offshore jurisdictions (Cayman, Luxembourg, Ireland):** Limited public disclosure; registration filings with local authorities but generally confidential.

### ILPA Standards

The Institutional Limited Partners Association sets reporting and governance standards including standardized templates for capital account statements, fee reporting, and performance attribution. ILPA guidelines increasingly influence industry practice even for non-member LPs.

---

## Decision Tree for Fund Size Extraction

When encountering a potential PE fund size data point, apply this verification sequence:

**Step 1: Is this a PE buyout fund?**
- Check for Roman numeral sequencing in name
- Verify absence of credit/debt/real estate/infrastructure/venture keywords
- Confirm blind-pool structure (not deal-specific)
- If unclear, classify as "unknown" or "requires verification"

**Step 2: Is this the flagship fund?**
- Check for continuation/co-investment/parallel/sidecar indicators
- Verify it's the main sequentially-numbered fund (not a suffix variant)
- If parallel fund, aggregate with main fund total

**Step 3: Is this final close data?**
- Look for explicit "final close" language
- Check if subsequent press releases announced additional closes
- Verify via Form D amendments if available
- If interim close, note as such and continue monitoring

**Step 4: What exactly is being measured?**
- Confirm "committed capital" (not AUM, NAV, or deployed capital)
- Note if amount includes co-investment or related vehicles
- Verify currency and apply conversion if needed

**Step 5: How reliable is the source?**
- Rank by source hierarchy (SEC filings > press releases > news > aggregators)
- Cross-reference against at least one additional source for amounts >$1B
- Note any discrepancies and flag for review

**Step 6: Apply market segment classification**
- Use PitchBook thresholds as primary reference (>$5B = mega; $100M-$5B = mid-market)
- Note vintage year for historical context
- Consider regional context for non-US funds

This systematic approach ensures consistent, accurate extraction of PE fund size data from any web source while properly categorizing funds and avoiding common misclassification errors.

---

## Related Documents

| Document | Relationship |
|----------|-------------|
| [PE Capital Markets Professional - Buyer Primer](pe-capital-markets-professional-buyer-primer.md) | PE capital markets buyer persona - uses this document's fund taxonomy as foundational context |
