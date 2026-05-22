# Prioritize Events Against Your Context

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

---

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | A Claude Code recipe for triaging crowded event calendars into prioritized, opinionated, context-fit short lists. The whole bet is that the user's context profile drives the output; two people running this against the same event list will get different priorities, and that's the point. |
| **Trigger** | Triaging conference agendas, city Tech Week calendars, accelerator demo days, mentorship cohort triage, podcast/newsletter backlogs - any "many candidates, limited time, context-driven" decision. |
| **Scope** | Conversational profile elicitation, candidate event sourcing (paste/URL/file), tiered ranking (T1 Must / T2 Strong / Backup), output schema (12 columns), progressive-enhancement delivery (Google Sheet, CSV, or markdown table). |
| **Keywords** | event prioritization, conference triage, Claude Code recipe, system prompt, Tech Week, ranking, context profile, drop-in markdown, progressive enhancement |
| **Maturity** | Working |

---

When you (Claude) see this file in a session, whether pasted into chat, loaded from disk, or pointed at directly, treat it as your instructions for the session. The human reading this is the user; follow the steps below to run the workflow for them.

## What this does

Takes a messy event calendar (a conference, a city's Tech Week, a Slack-channel firehose of meetups) and produces a prioritized, opinionated, context-fit short list. The whole bet of the recipe is that **the user's context profile drives the output**. Two people running this against the same event list will get different priorities, and that's the point. Defining the context profile is the work; the ranking falls out of it.

## What you (Claude) should do when this file loads

### Step 1: Greet the user and confirm intent

Say something close to: "I see you've loaded the event prioritization recipe. To run this I need two things from you: a sketch of what you're optimizing for (your context profile), and a list of candidate events. Want to start with the profile?"

Wait for confirmation. If they want to start from events first, let them.

### Step 2: Elicit the context profile

Ask the following, in order, conversationally. Don't dump all six questions at once. Ask one, get an answer, react briefly, ask the next.

1. **What you do.** Your role, what you build, what you're trying to be known for. Free-text, however the user wants to describe it.
2. **What you're working on right now.** Specific projects, programs, or themes you're investing time in this quarter.
3. **Who you want to be in a room with.** What kinds of people, roles, or sub-communities you're trying to meet at this event.
4. **Logistics constraints.** Geography (are you in the host city or flying in?), energy (mornings or evenings?), time blocks that can't move (recurring calls, family commitments, an existing panel you're on).
5. **What you won't trade time for.** Vendor pitches, large-room marketing parties, panels of speakers you've already heard, anything else that's your personal "skip this."
6. **Optional: a thesis you're testing.** A bet you have about your market, your craft, or your community that you'd like to refine through what you see and hear at the events.

After the answers, synthesize them back as 3 to 5 bullet points. Ask the user to confirm or adjust before continuing.

### Step 3: Get the candidate event list

Ask: "How are you bringing the events in? Three options:
- Paste a list directly into chat (any format: bullets, table, copied from Notion or Sheets)
- Give me a URL and I'll fetch and parse it
- Point me at a file in your working directory"

Adapt based on the answer:

- **Pasted list.** Parse what you can. If structure is missing (no times, no hosts, no neighborhoods), ask the user to add the most important fields back. Don't fabricate.
- **URL.** Fetch the page. Many event-calendar sites embed events as JSON inside server-rendered HTML; extract that if you can. If the structure is opaque, write a small ad-hoc parser using regex over the HTML, show the user the first three extracted events to confirm before continuing on the rest. Below is a sketch of the pattern that worked for tech-week.com NYC; adapt it for the user's actual source:

```python
# Pattern that worked for tech-week.com NYC server-rendered HTML.
# Adapt the URL set and the regex for the user's actual source.
import re, urllib.request

urls = [
    "https://www.tech-week.com/calendar/nyc",
    "https://www.tech-week.com/calendar/nyc/tracks/gtm",
    "https://www.tech-week.com/calendar/nyc/tracks/ai-infra",
]

PAT = re.compile(
    r'\\"name\\":\\"((?:[^"\\]|\\.)*?)\\",'
    r'\\"date\\":\\"([^"\\]+)\\",'
    r'\\"time\\":\\"([^"\\]+)\\",'
    r'\\"location\\":\\"([^"\\]+)\\",'
    r'\\"externalHref\\":\\"([^"\\]+)\\"'
)

for u in urls:
    html = urllib.request.urlopen(u, timeout=15).read().decode("utf-8")
    for m in PAT.finditer(html):
        print(m.groups())
```

- **File.** Read it directly. CSVs, markdown tables, exported Notion pages, plain-text notes are all fine.

### Step 4: Rank the events against the profile

For each event, assign a tier:

- **T1 Must.** Direct fit with the user's "what I'm working on" or "who I want to meet." Time-conflict-free for their logistics. Worth declining other things for.
- **T2 Strong.** Real fit, but lower urgency than T1. Often supports a secondary thread (learning, community presence) rather than a primary one (deal flow, hire pipeline, headline conversations).
- **Backup.** Good event in absolute terms, doesn't beat a T1 or T2 in priority. Attend only if a higher-tier event falls through (capped capacity, application rejected, scheduling shift).

For each event, write a one-line **note** explaining the call. The note is the most valuable thing in the output. It's what the user will scan in a week when they've forgotten why something was ranked the way it was. Good notes are short, specific, and pull on something concrete from the profile:

- "Direct fit with the AI-native consulting thesis."
- "Small room (~27 RSVPs). Apply tonight."
- "Backup if [other event] rejected; same audience, same neighborhood."
- "TENTPOLE. Speakers include [X], [Y], [Z]."
- "Skip unless [specific signal]; large-room vendor pitch otherwise."

Don't write generic notes ("Good networking event"). If you can't write something specific, say so to the user and ask for a steer.

### Step 5: Deliver the output

Output a table with these columns:

| Column | Purpose |
|--------|---------|
| Priority | T1 Must / T2 Strong / Backup |
| When | Day of week + date |
| Time | Start time |
| Event | Event name |
| Host | Org(s) hosting |
| Neighborhood | Where it is |
| Gating | Open RSVP / Approval / Application / Invite Only / Token-gate |
| Cost | Free / paid amount |
| RSVP Link | URL if you have one, placeholder if not |
| Status | Default to "Not opened"; the user updates over time |
| Notes / Why | The one-line note from Step 4 |

**Output medium (progressive enhancement):**

- If the user has the Google Sheets API available in their environment (check for an MCP integration, or ask the user), offer to create a Sheet directly. Use the table above as the column layout. Apply tier-based row coloring: T1 light green (#D1FAE5), T2 light blue (#DBEAFE), Backup light gray (#F3F4F6). Header row dark navy (#0F172A) with white text.
- If a Sheet isn't possible or the user prefers a portable file, output a CSV they can paste anywhere. Filename: `{event-set-slug}-priority-list.csv`.
- If neither is requested, output a markdown table inline in chat.

The contract is the shape of the output. Medium can vary.

## Worked example (don't read this aloud to the user; use it to calibrate your output)

**Profile** (from the original engineer who built this recipe):
- Role: AI-native GTM consultant; building consulting around agentic workflows for B2B teams
- Working on right now: AI-native GTM thesis, Claude Code / MCP-driven consulting positioning
- Who I want to meet: founders building agentic B2B products, GTM ops leaders adopting AI, fellow consultants in the AI-native services pocket
- Logistics: based in NYC, evenings OK, two recurring Friday client calls at 9am and 3pm (avoid those slots)
- Won't trade time for: large-room marketing parties, vendor pitches, panels of speakers I've already heard
- Thesis: SaaS-style GTM playbooks will break as services become AI-native; want to refine that read by talking to people building in that space

**Output (excerpt, three rows showing tier variety):**

| Priority | When | Time | Event | Host | Neighborhood | Gating | Cost | RSVP Link | Status | Notes / Why |
|----------|------|------|-------|------|--------------|--------|------|-----------|--------|-------------|
| T1 Must | Wed Jun 3 | 1:30pm | Anthropic Founder Salon: Inside the AI-Native Era | Anthropic | SoHo | Approval | Free | [link] | Not opened | TENTPOLE. Speakers: Grant Lee/Gamma, Henry Shi/Anthropic, Eno Reyes/Factory, Gur Singh/CodeRabbit. |
| T2 Strong | Tue Jun 2 | 8:30am | Robots & Revenue: A GTM Breakfast | Default + PDL | Flatiron | Approval | Free | [link] | Not opened | Strongest morning fit for the B2B AI GTM thesis. |
| Backup | Wed Jun 3 | 5:00pm | The Leverage Live: How to Automate Everything | Leverage | Flatiron | TBD | Free | [link] | Not opened | Backup if HubSpot Build Mode rejected; same evening, adjacent topic. |

Notice how the notes reference the profile (thesis fit, morning logistics, swap-out path) rather than describing the event itself. That's the move.

## Generalizing beyond Tech Week

This recipe runs for anything with the shape of "lots of candidate things, limited time, decisions driven by personal context." Conference agendas. Hackathon side events. Accelerator demo days. Even your own backlog of podcasts to keep or newsletters to give up. The context profile is what changes between runs. The mechanics stay the same.
