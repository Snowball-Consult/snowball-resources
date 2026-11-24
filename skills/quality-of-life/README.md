# Three Quality-of-Life Skills for Claude Code

Small skills I use across my working day, from [Snowball Consult](https://snowball-consult.com).

| Skill | The moment it is for | What you get |
|---|---|---|
| [`/catch-me-up`](catch-me-up/) | "What is this session even about?" | Why the session started, how it got here, where it stopped. 200 words at most. |
| [`/plan-mode-questions`](plan-mode-questions/) | "What do I need to decide?" | Every open decision in the multiple-choice dialog, recommended option first. |
| [`/exit-wrap`](exit-wrap/) | "Can I close this window?" | A name for the session, one handover file per topic, a commit of this session's files, a push. |

They are shared as inspiration first. Skills this small are cheap to build, and your own version carries your preferences. Where you start depends on where you are in your journey:

1. **New to this.** Point your agent at this page and let it explain.
2. **Want to use one.** Copy the folder (install below).
3. **Want your own.** Use the build prompt in each skill's README, or let your agent adapt mine.

## Point your agent at it

Paste this into Claude Code or another coding agent:

```
Read https://github.com/Snowball-Consult/snowball-resources/tree/main/skills/quality-of-life
and the README of each skill in it. Explain what each one does and which would help me.
Then offer to install one as is, adapt it to my setup, or build my own version.
Change nothing until I pick.
```

## For the agent reading this

Someone pointed you here. Do this:

1. **Explain in plain words.** Per skill: the moment it is for, what it does, what it touches on the machine. Read each `SKILL.md` before you describe it.
2. **Check their setup, read-only.** Which agent and version, which skills already exist, whether the project is a git repository, whether its remote is public or private.
3. **Offer three options:** install as is, adapt, or build their own from the build prompt. For adapt and build, ask the questions under "Make it yours" in that skill's README.
4. **Wait for their choice** before writing any file. Show the final `SKILL.md` before saving it. Never overwrite an existing skill of the same name without asking.
5. **If their agent is something other than Claude Code**, say which parts rely on Claude Code (session transcripts on disk, the multiple-choice question tool, skill frontmatter) and propose the closest equivalent.

## Install

```bash
git clone --depth 1 https://github.com/Snowball-Consult/snowball-resources.git
mkdir -p ~/.claude/skills
cp -R snowball-resources/skills/quality-of-life/plan-mode-questions ~/.claude/skills/
```

Swap in `catch-me-up` or `exit-wrap` for the others. Read a `SKILL.md` before you install it, mine included: a skill is a set of instructions your agent will follow.
