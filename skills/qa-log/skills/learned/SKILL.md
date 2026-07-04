---
name: learned
description: Capture a question-and-answer you want to retain into the Q&A learning log as a spaced-repetition card. Use after a good answer lands, or pass a question directly. Trigger phrases - "log that", "remember this Q&A", "/learned".
argument-hint: "[optional: the question, or nothing to capture the last Q&A]"
---

Capture a Q&A into the learning log following the methodology in `qa-log/README.md`. The point of this skill is near-zero capture friction, so move fast and only ask the user something when the answer genuinely isn't already in front of you.

## Step 1: Identify the Q&A

Determine the question and answer to capture:

- **No `$ARGUMENTS`** (the common case - "log that" / "/learned" right after an answer): use the **most recent substantive question the user asked and the answer just given** in this conversation. Do not ask the user to restate it; it is already in context.
- **`$ARGUMENTS` contains a question**: that is the question. If the answer to it exists earlier in the conversation, use it. If not, answer it now (briefly and accurately), then capture that.

## Step 2: Distill the card

Turn the raw exchange into a recall card. Do not paste the transcript.

- **Question** (front): rewrite as a single clear line that tests *recall*, not recognition. It should be answerable from memory and not give away the answer. Prefer "How do you steer what Claude Code preserves during compaction, and when does steering backfire?" over "Tell me about compaction."
- **Answer** (back): the crisp, correct answer in 1-4 sentences or a tight list. Accurate and self-contained - this is what gets graded against later.
- **Why it matters** (one line): the reason this is worth retaining. Skip if genuinely not applicable.
- **type**: `recall` by default. Use `recognition` only if the user says it's a recognize-it-when-I-see-it fact rather than something to reproduce.
- **tags**: 1-3 short kebab-case topic tags.
- **source**: `terminal` unless the user says the question originally came from `claude.ai` or `google`.

## Step 3: Write the card

Run the add command (quote values; escape embedded quotes):

```bash
python3 qa-log/qa_log.py add \
  --question "<recall question>" \
  --answer "<crisp answer>" \
  --why "<one line>" \
  --source terminal \
  --tags "<tag-a, tag-b>" \
  --type recall \
  --json
```

## Step 4: Confirm

Show the captured card id and a one-line preview of the front, e.g. `Captured qa-007 - "How do you steer compaction, and when does it backfire?"`. Mention `/quiz` is how it comes back. Keep the confirmation to one or two lines.

## Examples

```
/learned                                  # capture the Q&A just discussed
/learned why does guiding compaction help # capture this specific question (answer it first if needed)
log that                                  # same as bare /learned
```
