# /exit-wrap

**The moment:** you are done for now and want to close the window without losing anything.

**What it does:** proposes a searchable session name, writes or updates one handover file for the topic, commits only the files this session touched, and pushes. Later, in a new session, you ask about the topic and continue from the handover.

## How it came about

It started with two questions I kept asking: "how should I rename this session?" and "if I exit now, is this logged?" So the end of a session became one command. It is my most used skill by a wide margin.

The handover came later. I was keeping windows open only because the session inside had not produced a file yet.

## What it contains

One `SKILL.md`. My own version also runs a health check on my knowledge base and writes client session notes. Those parts depend on my setup, so this version leaves them out and includes the handover format, which is a separate skill on my side.

## What it touches

- `handovers/` in your project: creates or updates one file
- git: a commit of this session's files, and a push
- Only runs when you type it (`disable-model-invocation: true`), because it commits and pushes

**Check before the first run:** handovers contain conversation content. In a public repository, keep `handovers/` out of git. The skill asks when the remote is public.

To have new sessions find the handovers, add a line like this to your `CLAUDE.md`:

```
When I return to an earlier topic ("where were we on X"), look in handovers/ first
and continue from that file's "How to pick this up" section.
```

## Build your own

```
Build me an /exit-wrap skill for the end of a session. Propose a searchable session name,
write or update one handover file per topic (goal, decisions with reasons, what is open,
how to pick it up), commit only the files this session touched, by name, and push.
Tell me what you left alone. Only run it when I type it.
```

## Make it yours

- What do you do by hand at the end of every session? That is your list.
- Commit only, or also push? Straight to main, or a branch?
- Where do handovers live, and should they be in git?
- Is there a check that has to pass before a commit?
