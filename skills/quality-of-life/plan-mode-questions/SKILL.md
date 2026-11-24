---
name: plan-mode-questions
description: Put the open decisions in this conversation into the multiple-choice question dialog (the one plan mode uses), without entering plan mode.
argument-hint: "[optional: which topic or decisions to ask about]"
disable-model-invocation: true
---

Present the decisions that need to be made through the AskUserQuestion tool. Stay in the current permission mode; never call EnterPlanMode.

## Step 1: Collect the decisions

- If `$ARGUMENTS` is given, cover only that topic. Otherwise cover every decision still open in this conversation, including ones asked as prose in earlier replies.
- Look up anything the repository, the conversation or vendor docs can answer. Ask only what is the user's to decide.
- Drop anything already decided. If nothing is open, say so in one line and stop.

## Step 2: Ask

Call AskUserQuestion straight away, with no prose list of the questions first.

- Each question stands on its own: include the one fact needed to decide, since earlier text may be hidden while the dialog is open.
- Put the recommended option first with "(Recommended)" at the end of its label. Each description states what happens if it is chosen.
- Use `multiSelect: true` when options can be combined. Use `preview` when options are things to compare visually (mockups, snippets, layouts).
- Do not add an "Other" option; the dialog supplies one.
- The tool takes at most 4 questions per call and 2 to 4 options per question. With more decisions, ask the ones that other answers depend on first, then call again for the rest.

## Step 3: Close

List the decisions as one line each, then continue the work they unblock if it was already requested. Choosing an option approves only what that option says. If the dialog is dismissed or a question is left unanswered, treat that decision as open and do not choose for the user.
