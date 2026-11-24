# /catch-me-up

**The moment:** you have many Claude Code sessions open, you come back to one after days, and you no longer know what it is about.

**What it does:** restores why the session started, how it got here and where it stopped. `/catch-me-up` (or `brief`) stays within 200 words and uses only the conversation history. `/catch-me-up full` stays within 300 and also runs a few read-only checks on whether the open work still stands as described.

## How it came about

I keep many sessions open and come back to them days or weeks later. I know which session I need, and I have forgotten why it started. I was typing things like "catch me up, one paragraph" by hand. What I wanted was the problem the session set out to solve, before the latest topic.

Claude Code has its own recap (`/recap`, plus an automatic one-liner when you return to the terminal). That one line is often enough. This skill is for when you need the story: origin, turns, stopping point.

## What it contains

- `SKILL.md`: the instructions. Find the origin, the progression, the position and the stopping point. A suggestion by Claude is never reported as a decision by you.
- `scripts/session_history.py`: reads this session's transcript on disk and prints a bounded digest. It follows the active conversation, including across compaction. Read-only, standard library only.
- `scripts/check_recap.py`: rejects a draft recap that is too long or has the wrong shape.
- `tests/`: 26 tests on made-up transcripts. Run `python3 -m unittest discover -s tests` from this folder.

## What it touches

It reads the transcript of the current session under `~/.claude/projects/` (or `$CLAUDE_CONFIG_DIR`). The skill tells Claude to change nothing, and removes the edit tools for that turn.

## Known limits

- Transcript formats change between Claude Code versions. The scripts were written against 2.1.268 to 2.1.272. On 2.1.331 they read the history in full and label compaction `Unknown`, because newer record types are not recognized.
- The judgement about what counted as a decision comes from the model.

## Build your own

```
Build me a /catch-me-up skill. When I return to an old session, it tells me in under 200 words:
the problem this session set out to solve, the decisions and turns that followed and why,
and the exact point where we stopped. Read the session's transcript from disk so it also works
after compaction. Never report your own suggestion as my decision. It must not change anything.
```

A version without the scripts, working only from what is in context, is one short `SKILL.md`. Start there.

## Make it yours

- How long should a recap be?
- What do you want first: the original goal, or the next step?
- Should it check the current state of files, or only tell the story?
