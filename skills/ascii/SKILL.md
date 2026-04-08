---
name: ascii
description: Render a word or phrase as bold ASCII block art, auto-fitted to terminal width
argument-hint: "<word or phrase>"
---

Render the given word or phrase as large, bold ASCII block art.

## Step 1: Get the Input

If $ARGUMENTS contains a word or phrase, use that as the text to render.

If $ARGUMENTS is empty, ask: **"What word or phrase do you want rendered as ASCII art?"**

## Step 2: Render

Run the render script with the text as literal arguments (no shell variables or substitutions):

```
python3 ~/.claude/skills/ascii/render.py hello world
```

The script auto-detects terminal width. Supports A-Z, 0-9, punctuation, and emoji.

If the script fails (e.g., pyfiglet not installed), install it with `pip3 install pyfiglet` and retry.

> **Project-level install?** If this skill lives at `.claude/skills/ascii/` instead of `~/.claude/skills/ascii/`, adjust paths accordingly.

## Step 3: Display

Read `~/.claude/skills/ascii/output.txt` using the Read tool, then display it.

CRITICAL rendering rules to avoid the terminal bullet shifting the first row:
1. Do NOT output any text before calling the Bash and Read tools. Go straight to the tool calls with no preceding text.
2. AFTER reading the output file, output a short text line (the input text) followed immediately by the art inside a markdown code block (triple backticks). Both must be in the SAME final output block - the bullet lands on the text line, keeping the code block clean.
3. No other commentary needed.
