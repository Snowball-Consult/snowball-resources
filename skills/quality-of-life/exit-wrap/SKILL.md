---
name: exit-wrap
description: End-of-session routine - propose a session name, write or update the topic handover, commit this session's files, push.
argument-hint: "[no handover] [optional summary]"
disable-model-invocation: true
---

Wrap up the current session so it can be closed without losing anything.

## Step 0: Switches

The handover is on by default, also for sessions that changed no files. If `$ARGUMENTS` contains "no handover" (or "no handoff"), skip Step 3. Treat the remaining text as a summary of the work and use it for the name and the commit message.

## Step 1: Propose a session name

You cannot run `/rename` yourself. Work out a name and give the user the line to paste: `/rename <name>`.

- kebab-case, 5 to 10 words, made of the words the user would search for later
- it names what the session was about, which can differ from what the first message mentioned

## Step 2: Find this session's files

Run `git status` and `git diff`. List the files this session created, changed, moved or deleted. Other sessions may share the checkout, so leave every file this session did not touch, and report those at the end.

If this is not a git repository, write the handover, skip Step 4 and say so.

## Step 3: Topic handover

Handovers live in `handovers/` at the project root (create it if missing), one file per topic, named `YYYY-MM-DD_<topic-keywords>.md`.

Before the first handover in a project, check whether the remote repository is public. If it is, or you cannot tell, ask whether handovers should be committed or kept out of git. They contain conversation content. Never write secrets, tokens or credentials into one.

- **The topic already has a file:** update it in place and keep the filename. Rewrite everything above "Session ledger" to the current state, then add one ledger entry. Leave older entries unchanged.
- **No match, or a doubtful one:** write a new file. Merging two files later is easy; separating two mixed topics is hard.

Structure:

```markdown
# Handover: <topic>

## What we were trying to do
<2-4 sentences, plus the user's original request in their own words>

## What got decided
- <decision>: <choice>. Why: <reason>. Ruled out: <alternatives>.

## What got built or changed
- <file, commit or setting>

## What is still open
- Decided, to do: ...
- Undecided: ...
- Parked on purpose: ...

## How to pick this up
1. <first action>

## Session ledger
Newest first.
- YYYY-MM-DD `<session id>` (<session name>): <1-3 lines on what this session did>
```

The current session id is `${CLAUDE_SESSION_ID}`. Write only what happened. A section with nothing to say gets "None".

## Step 4: Commit and push

1. Follow the repository's own git rules (branching, message format) where it has them.
2. If the project has a health check or test command for what changed, run it. If it fails, stop and report before committing.
3. Check the diff for secrets. If you find one, stop and tell the user.
4. Stage by name and commit by path: `git add <new files> && git commit -m "<message>" -- <paths>`. Never `git add -A`, `git add .` or `git commit -a`.
5. Push if the branch has a remote. If the push is rejected, report it. Never force.

## Step 5: Report

- the `/rename` line to paste
- handover path, and whether it was created or updated
- commit hash and message, pushed or not
- files left alone, and why
