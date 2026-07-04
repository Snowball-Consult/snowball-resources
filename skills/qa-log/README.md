# Quiz Me: a Q&A Learning Log for Claude Code

A capture-first spaced-repetition system for Claude Code. `/learned` turns any good answer into a recall card the moment it lands. `/quiz` brings cards back as free-recall questions, grades your answer semantically, and reschedules each card based on how you did. A session-start hook reminds you when cards are due, so the system resurfaces itself even after you forget you built it.

Use it as-is, or treat it as a reference implementation and build your own. The whole system is one Python file, two skill files, and a hook.

## The experience

You ask good questions all day - in the terminal, in chat, in a search bar - and the answers evaporate. This closes the loop:

1. An answer lands that you want to keep. You type `/learned`. Claude distills the exchange into a recall card (question, crisp answer, one line on why it matters) and files it. Capture costs one word.
2. Days later you open a terminal and the session greets you with: `📚 Q&A log: 3 cards due - /quiz`.
3. `/quiz` asks the questions one at a time. You answer from memory, in your own words. Claude grades the substance of what you said, tells you exactly what you missed, and reschedules the card.

The differentiator over a flashcard app is step 3: **semantic grading of free recall**. You produce the answer yourself and the model judges how close you got, closer to an oral exam than to flipping a flashcard.

**The design principle:** capture friction is the binding constraint, and the quiz is downstream of it. The store only works if capturing a card costs almost nothing at the moment a good answer lands. So capture is a one-word reflex, and the spaced-repetition quiz is the reward layer on top.

## How it works

| Piece | Role |
|-------|------|
| `qa_log.py` | The engine: card storage, SM-2-lite scheduling, due-card queries, stats, the session-start nudge. Python 3 standard library only. |
| `skills/learned/SKILL.md` | `/learned` - capture. Distills the last Q&A in the conversation into a card. |
| `skills/quiz/SKILL.md` | `/quiz` - review. Pulls due cards, asks free recall, grades semantically, records the grade. |
| `cards/` | One markdown file per card. Scheduling state in frontmatter, Q&A in the body. Git-backed, human-readable, no database. |
| `hooks-snippet.json` | SessionStart hook wiring for the nudge. |

The split matters: **the LLM only judges recall quality; the date math is deterministic Python** (`_schedule` in `qa_log.py`). Claude decides how good your answer was, the algorithm decides when you see the card again.

### Card format

One markdown file per card in `cards/`, named `qa-NNN_{slug}.md`. Frontmatter holds the scheduling state (flat scalars only); the body holds the human-readable Q/A.

```markdown
---
id: qa-001
created: 2026-07-04
source: terminal          # terminal | claude.ai | google | other
tags: claude-code, context-management
type: recall              # recall | recognition
interval: 0               # days until next review
ease: 2.50                # SM-2 ease factor
reps: 0                   # successful reps in a row
next_review: 2026-07-04   # new cards are due immediately
last_reviewed:
last_grade:
---

## Question

<one-line, reframed so it tests recall rather than recognition>

## Answer

<the crisp answer>

**Why it matters:** <one line>

## Review history

| Date | Grade | Interval (d) | Next review |
|------|-------|--------------|-------------|
```

### Scheduling (SM-2-lite)

Each graded answer maps to one of four grades and reschedules the card:

| Grade | Meaning | Effect |
|-------|---------|--------|
| `again` | Missed it | Reset to a 1-day interval, ease drops |
| `hard` | Partial recall | Small interval bump, ease drops slightly |
| `good` | Got it | Interval grows by the ease factor |
| `easy` | Instant and confident | Interval grows faster, ease rises |

New cards are due immediately. Intervals climb 1 day, then 3 days, then interval x ease, so cards you know well fade into the future while shaky ones keep coming back. The `/quiz` skill never shows the raw grade codes; you see plain labels instead (Missed it / Partial / Got it / Nailed it).

### The nudge

A `SessionStart` hook runs `qa_log.py nudge`, which prints a one-line reminder when cards are due or when nothing new has been captured for 7+ days, and stays silent otherwise. The reminder fires at the one moment you can act on it - opening a terminal session - rather than on some unattended schedule. An empty store stays quiet until you start using it, and the hook is wrapped so an error can never break your session.

## Install

Prerequisites: Python 3 (standard library only) and Claude Code.

From the root of the project where the learning log should live:

```bash
git clone https://github.com/Snowball-Consult/snowball-resources.git /tmp/sr && \
  cp -r /tmp/sr/skills/qa-log ./qa-log && \
  mkdir -p .claude/skills && \
  cp -r ./qa-log/skills/learned ./qa-log/skills/quiz .claude/skills/ && \
  rm -rf /tmp/sr
```

That gives you:

1. `qa-log/` at your project root - the engine, the cards folder, and this README as the methodology doc the skills reference.
2. `/learned` and `/quiz` as project skills in `.claude/skills/`.

Then wire the nudge (optional, but it is the best part): merge the contents of `qa-log/hooks-snippet.json` into your project's `.claude/settings.json`. If you already have a `hooks` key, add the `SessionStart` entry alongside your existing hooks.

If you prefer the skills available in every project, copy them to `~/.claude/skills/` instead; the `qa-log/` folder stays per-project.

### Try it

A sample card ships in `cards/`, so there is something to quiz on day one:

```
/quiz                # review due cards
/learned             # capture the Q&A just discussed
```

## CLI reference

The skills call this; you can also run it directly.

```bash
python3 qa-log/qa_log.py add --question "..." --answer "..." --why "..." \
        --source terminal --tags "topic-a, topic-b" --type recall
python3 qa-log/qa_log.py due --include-new --json   # what to quiz (machine-readable)
python3 qa-log/qa_log.py due --recent 7             # also surface this week's captures
python3 qa-log/qa_log.py review qa-001 --grade good # record a grade, reschedule
python3 qa-log/qa_log.py list
python3 qa-log/qa_log.py stats
python3 qa-log/qa_log.py nudge                      # the SessionStart reminder
```

## A note on scope

Keep the learning log separate from any always-loaded memory or context system you run. Memory holds facts you want present in every session; the learning log holds things you are actively trying to retain through recall. Mixing the two pollutes both.

## From

Built by [Snowball Consult](https://snowball-consult.com) - a GTM data infrastructure consultancy. Questions? Reach out at andreas@snowball-consult.com
