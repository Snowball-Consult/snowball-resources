# /plan-mode-questions

**The moment:** the conversation has piled up open questions, some of them buried in long replies, and you want to answer them quickly.

**What it does:** collects every open decision and shows them in Claude Code's multiple-choice dialog, recommended option first. You stay in your current mode.

## How it came about

I like the questions plan mode asks, and I wanted them in any conversation. Until then I dictated my answers to long replies, question by question.

The dialog is built into Claude Code (the AskUserQuestion tool), and Claude can use it outside plan mode. The skill adds a command that calls for it on demand, plus rules for what deserves a question.

## What it contains

One short `SKILL.md` with three steps:

1. Collect the open decisions. Look up whatever can be looked up, so only real decisions reach you.
2. Ask, with the recommendation first and the consequence of each option spelled out.
3. Close with a one-line list of what was decided. An unanswered question stays open.

## What it touches

It reads the conversation, plus files or docs when they can answer a question. After you answer, Claude continues the work you had already asked for.

## Build your own

```
Build me a /plan-mode-questions skill. It collects every decision still open in this conversation
and asks me with the multiple-choice question dialog, without entering plan mode.
Recommended option first, each option says what happens if I pick it.
Look up anything you can find out yourself. Never decide an unanswered question for me.
```

## Make it yours

- Should it recommend an option, or stay neutral?
- All questions at once, or the most important first?
- Should decisions be logged somewhere, for example in a decisions file?
