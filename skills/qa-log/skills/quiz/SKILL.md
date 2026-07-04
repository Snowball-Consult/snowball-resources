---
name: quiz
description: Run a spaced-repetition review session over the Q&A learning log. Asks due cards one at a time as free recall, grades your answer semantically, and reschedules each card. Trigger phrases - "quiz me", "/quiz".
argument-hint: "[optional: N (max cards), 'recent', or a tag to filter]"
---

Run a review session over the Q&A learning log following the methodology in `qa-log/README.md`. The differentiator over a flashcard app is **semantic grading of free recall**: the user answers in their own words and you judge how close they got. Be a fair but honest grader - the value is in accurate feedback, not in being nice.

## Step 1: Pull the due cards

Parse `$ARGUMENTS`: a number sets the session cap (default 10); `recent` adds cards captured in the last 7 days even if not yet due; a word is treated as a tag filter.

```bash
python3 qa-log/qa_log.py due --include-new --limit <N> [--recent 7] --json
```

Parse the JSON (`cards` array; each has `id`, `question`, `answer`, `why`, `type`, `tags`). If a tag filter was given, keep only cards whose `tags` include it. If `count` is 0, tell the user there's nothing due (offer `--recent` or capturing some with `/learned`) and stop.

Tell the user how many cards are queued, then go one at a time.

## Step 2: Ask one card

For each card:

1. Show **only the question**. Never reveal the answer yet. For a `recognition`-type card you may offer multiple choice (generate 3 plausible distractors); for `recall` (default), ask for a free-text answer.
2. **Wait for the user's answer.** Do not grade and reveal in the same turn as asking - this is active recall, the retrieval effort is the whole point.

## Step 3: Grade and reveal

Once the user answers:

1. **Grade** their answer against the card's stored answer, judging it on substance (not wording). The `again`/`hard`/`good`/`easy` labels are internal scheduling codes (SM-2) - never show them to the user. Present the plain-language label instead:
   - `again` -> **"Missed it"** - missed the core idea, or "I don't know"
   - `hard` -> **"Partial"** - got some of it but missed a key piece
   - `good` -> **"Got it"** - substantively correct
   - `easy` -> **"Nailed it"** - correct, complete, and immediate (only if they nailed it cleanly)
2. **Reveal** the stored answer. If they missed or were partial, say specifically *what* was missing or wrong. If they got it, confirm and add the "why it matters" if it deepens it.
3. **Record** the grade (CLI still takes the raw SM-2 code):

```bash
python3 qa-log/qa_log.py review <card-id> --grade <again|hard|good|easy> --json
```

State the next review interval briefly (e.g. "next up in 3 days").

## Step 4: Session summary

After the last card (or if the user stops early), give a short scoreboard: how many asked, the grade spread using the plain labels (e.g. 4 Got it / 1 Partial / 1 Missed it), and which cards came back soonest so they know what's still shaky. Keep it tight.

## Examples

```
/quiz              # up to 10 due cards
/quiz 5            # cap at 5
/quiz recent       # include this week's captures even if not yet due
/quiz claude-code  # only cards tagged claude-code
quiz me            # same as /quiz
```
