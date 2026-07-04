# ASCII Block Art Skill for Claude Code

Render any word or phrase as large, bold ASCII block art - auto-fitted to your terminal width.

```
/ascii hello
```

```
##   ##  EEEEEEE  ##       ##       OOOOOOO
##   ##  EE       ##       ##       OO   OO
##   ##  EE       ##       ##       OO   OO
#######  EEEEE    ##       ##       OO   OO
##   ##  EE       ##       ##       OO   OO
##   ##  EE       ##       ##       OO   OO
##   ##  EEEEEEE  LLLLLLL  LLLLLLL  OOOOOOO
```

## Features

- Auto-scales horizontally to fill terminal width
- Word-wraps long phrases across multiple art rows
- Vertical doubling for visual weight
- Supports A-Z, 0-9, common punctuation
- Emoji support (hearts, stars)
- Custom shape overrides for Y, heart, star

## Install

**Prerequisites:** Python 3 with pyfiglet (`pip3 install pyfiglet`)

**One-liner (user-level install):**

```bash
git clone https://github.com/Snowball-Consult/snowball-resources.git /tmp/sr && \
  mkdir -p ~/.claude/skills && \
  cp -r /tmp/sr/skills/ascii ~/.claude/skills/ascii && \
  rm -rf /tmp/sr && \
  echo "Installed. Use /ascii in Claude Code."
```

**Or manually:**

1. Copy the `skills/ascii/` folder to `~/.claude/skills/ascii/`
2. That's it. Claude Code auto-discovers skills in `~/.claude/skills/`.

## Usage

In Claude Code, type:

```
/ascii your text here
```

Or just tell Claude to render something as ASCII art - it will pick up the skill.

## Project-level install

If you prefer per-project instead of global, copy to `.claude/skills/ascii/` inside your repo. The SKILL.md paths will need adjusting from `~/.claude/skills/ascii/` to `.claude/skills/ascii/`.

## How it works

The skill has two files:

| File | Role |
|------|------|
| `SKILL.md` | Instructions Claude follows when `/ascii` is invoked |
| `render.py` | Python script that does the actual rendering via pyfiglet |

Claude reads the SKILL.md, runs render.py with your text, reads the output file, and displays the result in a code block.

## From

[Snowball Consult](https://snowball-consult.com) - GTM data infrastructure consultancy.
