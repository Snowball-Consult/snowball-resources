# Ideal Buyer Persona Definition - Application Delivery Infrastructure into Fortune 500

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Demonstrate the structure and depth of an Ideal Buyer Persona definition for a B2B infrastructure company selling application delivery / traffic management into Fortune 500 enterprises |
| **Trigger** | Qualifying a contact, building persona filters, defining outreach targeting, scoring contacts |
| **Scope** | Person/contact-level targeting criteria - primary persona, secondary personas, champion archetypes, title signals, background signals, skip rules, segmentation by industry and cloud maturity |
| **Not In Scope** | Company-level criteria (see companion ICP Definition), messaging templates, outreach sequences |
| **Dependencies** | ICP Definition (companion document for company-level criteria, not included) |
| **Keywords** | persona, ideal buyer persona, application delivery, load balancing, traffic management, platform engineering, SRE, infrastructure, Fortune 500, enterprise, ADC, service mesh |
| **Maturity** | Working |
| **Last Reviewed** | 2026-04-02 |

**This is a living document.** It will be refined through team input, alignment sessions, and market feedback.

Persona is distinct from ICP. Persona answers "which person at the company?" while ICP answers "what company?" Both must be satisfied for a qualified opportunity.

---

## Persona Definition (Read Aloud)

> Your **primary ideal buyer** is a **Staff or Principal Platform Engineer, or a Director of Platform Engineering / SRE** at a Fortune 500 company who is **responsible for application delivery and traffic management** - though this is always a **"partial hat,"** never their full-time job. Load balancing is maybe 15-20% of what they do. The rest is CI/CD pipelines, developer tooling, Kubernetes operations, and observability. They only think about traffic management when something breaks, when a renewal is coming up, or when a migration forces the question. Their title will never say "Head of Load Balancing" or "Director of Application Delivery" - those titles don't exist. It's generic: "Staff Platform Engineer," "Director of Infrastructure," "Senior SRE." You have to look past the title.
>
> The strongest signal that someone is the right person is **previous experience at an infrastructure or CDN company** - they worked at Cloudflare, Fastly, Akamai, or a cloud-native infrastructure vendor before moving to the enterprise side. The second-best signal is **open-source contributions to traffic management projects** - Envoy, Istio, the Kubernetes Gateway API SIG, or NGINX. People who built or contributed to the data plane in a previous life are the ones who own it in their current role. A **CKA certification** is a moderate signal - it shows they operate at the cluster infrastructure level, not the application layer.
>
> At large enterprises (10,000+ employees), there's usually a **dedicated platform engineering team** and you're looking for the Staff/Principal engineer or director who owns the traffic management slice. At mid-size Fortune 500s (1,000-10,000 employees), platform engineering exists but traffic management is a **side responsibility for whoever owns Kubernetes** - and that person's title could be anything from "Senior SRE" to "Cloud Engineer" to "DevOps Lead." At traditional enterprises that haven't migrated yet, it's still a **network architect or senior network engineer** who manages the legacy hardware appliances - completely different persona, different language, different pain.
>
> The real pain isn't "we need a better load balancer." The pain is the **"two-speed infrastructure" problem** - on-prem traffic management and cloud traffic management are completely separate systems, separate teams, separate tools, no unified view. The person who can articulate that fragmentation problem is your buyer.
>
> You should also target the **junior-to-mid SREs who experience the operational pain** - they're the ones getting paged at 3am when a misconfiguration cascades, spending hours patching security vulnerabilities on quarterly cycles, and writing the postmortems that identify traffic management as a root cause. They're more responsive to outreach than their directors, and they can champion internally. But they can't sign a purchase order. **Target both levels** - the L3-L5 engineer who feels the pain, and the Director/VP who holds the budget. The ideal champion is the **Staff engineer (L5-L6)** who bridges both worlds: enough seniority to influence architecture decisions, close enough to operations to feel the pain and articulate it.
>
> **Skip pure application developers, product managers, and sales/marketing roles** - they don't touch infrastructure and won't understand the problem. **Don't automatically exclude the CTO or VP of Engineering** - at smaller Fortune 500 companies, they're the economic buyer and they care about infrastructure cost, team retention, and incident frequency. They're over-solicited but they respond when the message is about **risk reduction or migration velocity**, not product features.

---

## Primary Persona: Platform Engineering / SRE Leader

**Who they are:**
- Staff/Principal Platform Engineer or Director/VP of Platform Engineering or SRE
- Responsible for application delivery, traffic management, and ingress strategy (as one of several responsibilities)
- Background often includes CDN companies, infrastructure vendors, or cloud-native startups

**Why they buy:**
- Own the reliability and performance of traffic routing across the organization
- Managing the "two-speed" problem: legacy hardware appliances on-prem, cloud-native load balancing in the cloud, no unified control plane
- Facing forced migration decisions: legacy hardware end-of-life deadlines, retirement of major open-source ingress controllers, renewal cost increases

**How to identify:**
- Title contains: Staff Platform Engineer, Principal Platform Engineer, Director of Platform Engineering, VP of Infrastructure, Director of SRE, VP of SRE
- AND (LinkedIn experience includes CDN/infrastructure companies OR open-source contributions to Envoy/Istio/Gateway API OR job description mentions "ingress," "traffic management," "application delivery," or "service mesh")
- At traditional enterprises: look for Network Architect or Senior Network Engineer who manages hardware appliances
- Company website engineering blog and GitHub org often reveal who owns the infrastructure layer

**Market context:** Load balancing is always listed as ONE item in a longer list of responsibilities in job postings. It's never the headline. If you market to "load balancing decision makers," you reach nobody. You need to market to platform engineers and SREs broadly, with messaging that resonates with someone who spends 15-20% of their time on traffic management alongside five other responsibilities.

---

## Secondary Persona: Junior-to-Mid SRE (Pain-Experiencer)

**Who they are:**
- SRE, Infrastructure Engineer, or Platform Engineer at L3-L5 level (2-7 years experience)
- Operates on-call rotations covering traffic management incidents
- Handles day-to-day configuration, patching, and incident response for load balancers

**Why they matter:**
- They get paged at 3am when the load balancer misconfiguration causes an outage
- They spend hours patching security vulnerabilities on quarterly cycles
- They fight with complex configuration syntax for routine changes
- They write the postmortems that identify load balancing as a contributing factor
- They know exactly what's wrong but lack the authority to fix it through purchasing

**How to identify:**
- Title contains: SRE, Site Reliability Engineer, Infrastructure Engineer, Platform Engineer, DevOps Engineer
- AND seniority level is mid (2-7 years, L3-L5)
- Signal: active in SRE communities, incident management tooling in their stack, on-call rotation mentioned in role

**Engagement approach:**
- Target alongside senior personas, not instead of
- Juniors champion internally; Directors/VPs sign purchase orders
- They need senior sponsorship - junior engineers alone can't push a six-figure infrastructure purchase through procurement
- The most effective junior champions are the ones who run an unsanctioned proof-of-concept in a staging environment and show it working

---

## Secondary Persona: Network Architect (Traditional Enterprise)

**Who they are:**
- Senior Network Engineer or Network Architect at a traditional enterprise (financial services, manufacturing, healthcare)
- Manages legacy hardware appliances as part of broader network infrastructure (alongside firewalls, DNS, SD-WAN)
- May have vendor-specific certifications for the incumbent solution

**Why they matter:**
- At enterprises that haven't fully migrated to cloud, this person still owns traffic management
- They're feeling the squeeze: hardware end-of-life notifications, rising renewal costs, quarterly security patching cycles
- They're often skeptical of "cloud-native" messaging - they need to hear "better version of what you already have," not "rip everything out"

**How to identify:**
- Title contains: Network Architect, Senior Network Engineer, Director of Network Services, Director of Network Engineering
- AND company is in a traditional industry (financial services, healthcare, manufacturing) or has low cloud maturity
- Signal: vendor-specific certifications for incumbent ADC solution, NANOG or network engineering community participation

**Engagement approach:**
- Different language than the platform engineering persona - speak "network" not "Kubernetes"
- Position as modernization, not replacement
- They need to see coexistence with existing infrastructure during transition, not a rip-and-replace pitch
- Their biggest fear is disrupting production traffic - address risk directly

**Status:** This persona is shrinking as enterprises migrate to cloud and platform engineering teams take over. But it's still the dominant buyer at the most traditional Fortune 500s (banks, insurers, manufacturers). Don't ignore it.

---

## Emerging Persona: AI Infrastructure Lead

**Who they are:**
- Leads or contributes to AI/ML infrastructure at an enterprise deploying large language models or other AI inference workloads
- May sit in a dedicated ML Platform team or within the broader platform engineering org

**Why they might buy:**
- AI inference workloads require intelligent traffic management that understands token throughput and GPU utilization, not just HTTP request routing
- This is a net-new buying cycle, separate from the legacy replacement conversation
- They need load balancing across GPU clusters, model routing, and inference optimization

**How to identify:**
- Title contains: ML Platform Engineer, AI Infrastructure Lead, Director of ML Engineering
- AND company is deploying AI at scale (check for GPU infrastructure mentions, AI/ML blog posts, hiring for ML infra roles)

**Status:** Emerging. The AI inference traffic management need is creating a genuinely new category. This persona may not even know that their traffic management problem maps to application delivery infrastructure - they may be building custom solutions. Needs further validation before active targeting.

---

## Persona Signals (Ranked by Strength)

| Signal | Strength | Detection Method | Notes |
|--------|----------|------------------|-------|
| Previous experience at CDN or infrastructure company | Strongest | LinkedIn experience search | Cloudflare, Fastly, Akamai, infrastructure vendors, cloud-native companies (Tetrate, Solo.io, Kong). They understand the problem space from the builder side. |
| Open-source contributions to traffic management projects | Very Strong | GitHub profile, CNCF contributor lists | Envoy, Istio, Kubernetes Gateway API SIG, Cilium, NGINX, HAProxy. The most direct individual signal - they built or contributed to the tools they now evaluate. |
| Authored a postmortem involving load balancer failure | Strong | Internal signal (hard to detect externally), conference talks, blog posts | An "outage survivor" has organizational trauma and political capital. Look for SREcon or KubeCon talks about incident response, reliability postmortems. |
| CKA (Certified Kubernetes Administrator) certification | Medium-Strong | LinkedIn certifications | Shows cluster-level infrastructure competence. 250K+ enrollments in 2024 - common enough to filter by but not rare enough to be definitive. |
| "Platform Engineering" or "SRE" in current title at ICP-fit company | Medium | Title search + company match | Necessary but not sufficient. Confirms the functional area without confirming they own the traffic management slice. |
| High shared connection density with your engineering team | Medium | LinkedIn cross-reference (aggregate) | Same "Pathfinder" signal that works in any vertical - more connection paths = higher likelihood of warm entry. |
| Blog posts or conference talks about infrastructure modernization | Medium | Content search, speaker lists | Shows they're thinking about this problem and willing to invest time in solving it. |
| Vendor-specific certification for incumbent ADC | Medium | LinkedIn certifications | Confirms they manage the existing solution - a potential migration candidate. |
| Cloud certifications (AWS Advanced Networking, GCP Professional Cloud Network Engineer) | Moderate | LinkedIn certifications | Shows cloud networking depth, but doesn't confirm they own traffic management specifically. |
| Staff/Principal level at ICP-fit company | Baseline | Title + company match | Right seniority for champion role, but need additional signals to confirm they're in the infrastructure domain. |

---

## Champion Archetypes

Champions emerge from five distinct origin stories. Recognizing which archetype you're dealing with shapes how you sell to them.

| Archetype | Motivation | How to Detect | Approach |
|-----------|-----------|---------------|----------|
| **The Outage Survivor** | Lived through a major traffic management incident (P0/P1). Wrote the postmortem. Personal mission to prevent recurrence. | Conference talks about reliability, active in incident management communities, references outage in conversation. | Strongest emotional motivation. Lead with reliability and risk reduction. They have political capital from the incident - help them spend it. |
| **The Migration Leader** | Leading a cloud migration. Discovered legacy infrastructure doesn't translate. Needs to solve traffic management for the new environment. | LinkedIn shows "cloud migration" or "infrastructure modernization" projects. Often a recent role change. | Strongest timeline pressure. Migration milestones create hard deadlines. Align your sales cycle to their migration timeline. |
| **The Cloud-Native Advocate** | Believes in Kubernetes, infrastructure-as-code, GitOps. Views legacy appliances as technical debt. Wants to consolidate into the cloud-native stack. | Open-source contributions, conference talks, blog posts about cloud-native architecture, Kubernetes community involvement. | Strongest technical conviction. Will build the internal business case unprompted. Give them technical depth, not sales materials. |
| **The Cost Optimizer** | Got the renewal quote and had a visceral reaction. Tasked with reducing infrastructure costs. | Finance-adjacent title, P&L responsibility mentioned, infrastructure cost optimization projects. | Strongest budget motivation. Has quantifiable savings to present to leadership. Help them build the business case spreadsheet. |
| **The Security Closer** | Tired of patching vulnerabilities quarterly. Concerned about the attack surface of aging infrastructure. | Active in security communities, compliance background, CISO relationship. | Strongest risk narrative. Can frame the purchase as risk mitigation, which unlocks different (and often larger) budget lines than infrastructure optimization. |

---

## Exclusions

| Exclude | Why | Example Titles |
|---------|-----|----------------|
| Application developers | Don't touch infrastructure, won't understand the problem | Frontend Engineer, Backend Developer, Full-Stack Engineer |
| Product managers | Don't make infrastructure decisions | Product Manager, Technical Program Manager (unless infra-focused) |
| Sales, marketing, and business roles | No infrastructure involvement | Sales Engineer (at the buyer's company), Marketing, Business Analyst |
| IT Help Desk / Desktop Support | Different layer entirely | IT Support Specialist, Help Desk Analyst |

**Do NOT automatically exclude:**

| Role | Why keep | Approach |
|------|----------|----------|
| Junior SRE / Infrastructure Engineer (L3-L5) | Feel the operational pain directly (3am pages, CVE patching). Most responsive to outreach. Can champion internally. | Target alongside seniors. They run the unsanctioned POC that proves the product works. |
| CTO / VP of Engineering | Economic buyer at smaller F500s. Cares about infrastructure cost, team retention, incident frequency. | Over-solicited - lead with risk reduction or migration velocity, not feature lists. |
| CISO / Security Lead | Can unlock risk mitigation budgets that are separate from (and often larger than) infrastructure budgets. | Not a primary buyer but a powerful ally. Security concerns can accelerate or kill a deal. |
| Enterprise Architect | Ensures alignment with technology strategy. May block or champion based on architectural fit. | Needs to see how the solution fits the broader technology roadmap, not just the traffic management use case. |

---

## Persona by Company Profile

### By Cloud Maturity

How the buyer profile changes based on where the company is in its cloud journey:

| Cloud Maturity | Who Owns Traffic Management | Who to Target | Pain Point |
|----------------|---------------------------|---------------|------------|
| Cloud-native (born in cloud or fully migrated) | Platform Engineering team | Staff/Principal Platform Engineer, Director of Platform Engineering | Multi-cloud consistency, advanced routing, unified observability across regions |
| Hybrid (40-70% cloud, mid-migration) | Contested - NetOps AND Platform Engineering | Both personas - the platform engineer for cloud workloads, the network architect for on-prem | "Two-speed infrastructure" - separate systems, separate teams, no unified view. This is where the buying committee is largest and the decision is most complex. |
| Cloud-cautious (primarily on-prem, <30% cloud) | Network Engineering / Network Operations | Network Architect, Senior Network Engineer | Hardware end-of-life, renewal cost shock, security patching fatigue. Not ready for "cloud-native" messaging - need "better version of what you have." |

### By Industry Vertical

| Vertical | Buyer Characteristics | Cycle Length | Key Constraint |
|----------|---------------------|-------------|----------------|
| Financial Services | Most conservative. Security and compliance dominate. Legacy infrastructure deeply entrenched. Network engineering teams still dominant. | 12-18+ months | PCI DSS compliance, multi-jurisdictional regulations (DORA in EU), low-latency requirements for trading. SSL/TLS termination at the load balancer layer is a compliance concern. |
| Technology / SaaS | Most likely cloud-native. Platform engineering well-established. Comfortable with open-source. | 3-6 months | May have already moved past traditional ADCs entirely. Pain is multi-cloud consistency and scale, not legacy replacement. |
| Retail / E-commerce | Moving to cloud rapidly but hybrid. Seasonal traffic spikes (Black Friday) create acute pain. | 6-12 months | Cost sensitivity higher than finserv. Seasonal scaling requirements expose infrastructure limits. |
| Healthcare | Increasingly digital (telehealth, patient portals) but behind in cloud adoption. | 12-18 months | HIPAA compliance. Heavily procurement-driven. Similar constraints to financial services. |
| Manufacturing / Industrial | Most traditional IT infrastructure. IoT and edge computing creating new requirements. | 12+ months | Lowest cloud maturity. May still run legacy appliances managed by a single network engineer. Longest modernization horizon. |

---

## Buying Process Roles

How different roles play out in the infrastructure purchasing process at Fortune 500 companies. Average buying committee: ~33 people. Average cycle: 6-18 months.

| Role | Who | Notes |
|------|-----|-------|
| **Economic Buyer** | VP/SVP of Infrastructure or Engineering. CIO for company-wide platform decisions. Director+ level required for infrastructure purchases of this magnitude. | Budget authority. Cares about cost, risk, strategic alignment. Experiences pain abstractly through incident metrics and budget line items. |
| **Technical Champion** | Staff/Principal Platform Engineer or Senior/Lead SRE. At traditional enterprises: Network Architect. | Runs the evaluation and POC. Writes the internal recommendation. The person your sales team actually talks to in the evaluation. |
| **Security Gate** | CISO or Security team. | Must approve from a security posture perspective. Can kill or delay any infrastructure deal by months. Compliance review (PCI DSS, SOC 2, HIPAA) adds entire cycles. |
| **Enterprise Architect** | Enterprise Architect or Chief Architect. | Ensures alignment with technology strategy. Evaluates how the solution fits the broader roadmap. Can block based on architectural concerns. |
| **Procurement** | Vendor Management / Procurement. 79% of F500s have formal vendor management programs. | Manages the commercial relationship. Negotiates pricing, contract terms, multi-year agreements. Existing vendor enterprise license agreements create switching friction. |
| **Application Teams** | Engineering leads for the applications that will run behind the new solution. | Must validate that their apps work correctly with the new traffic management. Their adoption (or resistance) determines rollout success. Not decision-makers, but their rejection kills deals. |

**How interest gets triggered:**

*Forced decisions:* Most infrastructure purchasing in this space is triggered by external events - hardware end-of-life notifications, major open-source project retirements, renewal cost increases. The "buy" moment is usually forced, not proactive. Time your outreach to these events.

*Internal momentum:* Champions often start with an unsanctioned POC in a staging environment. They deploy the new solution alongside existing infrastructure, prove it works, then build the business case. The most effective framing is **risk reduction** (not cost savings) - because risk mitigation budgets are separate from and often larger than infrastructure optimization budgets.

*Peer influence:* Technical buyers trust other engineers. Conference talks, community discussions, and peer referrals carry more weight than vendor marketing. If your champion can reference a peer at a comparable company who made the switch, the internal sale gets dramatically easier.

---

## Identifying the Right Person at Hybrid Enterprises

The hybrid enterprise (40-70% cloud, mid-migration) is the largest and most complex buyer segment. Traffic management ownership is fragmented between the legacy network team and the modern platform engineering team, and the buying decision often involves both. Four approaches:

1. **Find the migration leader.** Someone at the company is leading the cloud migration or infrastructure modernization initiative. That person (or someone on their team) is likely encountering the traffic management fragmentation problem. Look for "cloud migration" or "infrastructure modernization" in their LinkedIn activity, recent blog posts, or conference talks.

2. **Look for the bridge builder.** At hybrid enterprises, the most valuable contact is someone who understands both worlds - legacy infrastructure AND cloud-native. They might have started in network engineering and moved into platform engineering, or vice versa. This person can navigate both teams internally and has the credibility to drive a unified solution.

3. **Open-source footprint as identifier.** Even at traditional enterprises, the person who contributes to or uses cloud-native traffic management projects (Envoy, Istio, Gateway API) is likely the one pushing modernization internally. GitHub activity, CNCF community participation, and KubeCon attendance are all signals.

4. **Study outage patterns.** If the company has had a public incident that involved traffic management (check status page history, incident retrospectives, or engineering blog posts), the person who wrote the postmortem or led the response is your best entry point. They have both the pain and the organizational mandate to fix it.

---

## Related Documents

- Ideal Customer Profile (ICP) Definition - Companion document for company-level targeting criteria
- Champion Identification and Scoring Framework - Methodology for scoring and prioritizing champions
- Outreach Personalization Guide - Persona-specific messaging by archetype and seniority level
