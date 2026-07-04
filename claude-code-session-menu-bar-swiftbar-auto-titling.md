# Claude Code Session Menu Bar

> **About this resource:** This is shared by [Snowball Consult](https://snowball-consult.com) as a methodology demo.
> It's meant as inspiration - not as a plug-and-play solution. Some referenced dependencies may not be included.
> Questions? Don't hesitate to reach out at andreas@snowball-consult.com

## Document Metadata

| Field | Value |
|-------|-------|
| **Purpose** | Architecture and annotated code for a macOS menu bar plugin that browses and resumes Claude Code sessions with auto-generated titles |
| **Trigger** | "How do I quickly resume Claude Code sessions?", building a session picker, improving session discoverability |
| **Scope** | SwiftBar plugin architecture, SessionEnd hook for auto-titling, JSONL session data format, display logic, dark mode support |
| **Not In Scope** | SwiftBar installation/configuration, Claude Code internals beyond session storage, non-macOS platforms |
| **Dependencies** | [SwiftBar](https://github.com/swiftbar/SwiftBar) (macOS menu bar plugin framework), Claude Code CLI |
| **Keywords** | Claude Code, sessions, resume, SwiftBar, menu bar, auto-title, SessionEnd hook, JSONL, macOS, dark mode |
| **Maturity** | Working |
| **Last Reviewed** | 2026-04-02 |

---

## The Problem

Finding closed Claude Code sessions to resume is painful. The built-in `claude --resume` requires opening a terminal first, and sessions without a manual `/rename` show as truncated first-prompt text that all looks the same. Most sessions are closed by just closing the terminal window, so no naming ever happens. The resume picker becomes a wall of indistinguishable text.

## The Solution

A macOS menu bar dropdown that shows all sessions grouped by date, with auto-generated titles. Click any session to resume it in Terminal.app. Two components:

1. **SwiftBar plugin** - reads session data, renders the dropdown
2. **SessionEnd hook** - auto-generates a concise title when any session closes

The hook is the key piece. It writes titles back into Claude Code's own session format, so they appear in both the menu bar AND the built-in `claude --resume` picker.

---

## Architecture

```
Session closes
    |
    v
SessionEnd hook fires (Claude Code passes session_id on stdin)
    |
    v
auto-title-session.py
    |-- Reads first user prompt from ~/.claude/projects/{project-hash}/{id}.jsonl
    |-- Skips if session already has a custom-title (user used /rename)
    |-- Calls: claude -p --model haiku --no-session-persistence "label this session"
    |-- Appends {"type":"custom-title","customTitle":"..."} to the JSONL
    |-- Updates SwiftBar cache for instant menu refresh
    |
    v
Title appears in BOTH:
    - claude --resume picker (reads custom-title from JSONL)
    - SwiftBar CC menu (reads from cache)
```

### Files

| File | Role |
|------|------|
| `sessions-menu.5m.py` | SwiftBar plugin - scans session files, renders grouped dropdown |
| `auto-title-session.py` | SessionEnd hook - generates title via Haiku, writes to JSONL |
| `resume-session.sh` | Helper - opens Terminal.app with `claude --resume <id>` via osascript |
| `generate-session-summaries.py` | Optional batch script - backfills titles for existing sessions |

### Menu Layout

Plain "CC" text in the menu bar. Dropdown grouped into: Active (with live PID detection), Today, Yesterday, This Week, Older. Click any session to resume it in a new Terminal window.

---

## Where Claude Code Stores Sessions

Claude Code stores each session as a JSONL file (one JSON object per line):

```
~/.claude/projects/{project-hash}/{session-uuid}.jsonl
```

The project hash is derived from your working directory. For example, `/Users/me/myproject` becomes `-Users-me-myproject`.

Each line in the JSONL is a typed entry. The ones relevant to this plugin:

```json
{"type": "user", "message": {"role": "user", "content": "Fix the login bug"}, "timestamp": "2026-04-01T14:30:00Z"}
```

```json
{"type": "custom-title", "customTitle": "Login bug fix", "sessionId": "abc-123"}
```

The `custom-title` type is what Claude Code's own `/rename` command writes. The auto-titling hook writes the same format, so Claude Code treats it identically.

Active sessions are tracked in `~/.claude/sessions/*.json` with a PID and session ID. The plugin checks if the PID is still running to detect active sessions.

---

## The Auto-Titling Hook

This is the most valuable piece. Without it, most sessions are just truncated first prompts.

### Hook Configuration

In `.claude/settings.local.json`:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 /path/to/auto-title-session.py",
            "timeout": 15000
          }
        ]
      }
    ]
  }
}
```

The hook receives JSON on stdin: `{"session_id": "uuid-here"}`.

### Title Generation Logic

The script:
1. Reads the session JSONL, extracts the first real user prompt
2. Skips if the session already has a `custom-title` (user already used `/rename`)
3. Skips trivial sessions (fewer than 2 user messages)
4. Calls `claude -p --model haiku` with a labeling prompt
5. Appends the title as a `custom-title` entry to the JSONL file

The prompt asks Haiku to produce a 3-8 word title, not a sentence:

```python
SYSTEM_PROMPT = (
    "You are a labeling machine. You ONLY output short titles. "
    "You never answer questions, give advice, or use markdown. "
    "Output ONLY the title, nothing else."
)

PROMPT_TEMPLATE = """Label this session in 3-8 words. Session date: {session_date}

Rules: concise title, not a sentence. No markdown, no bold, no quotes, no periods.

Good: HubSpot contact enrichment fields, Knowledge base manifest cleanup, Login bug investigation 4/1

SESSION PROMPT TO LABEL: {first_prompt}

TITLE:"""
```

Reject patterns catch cases where the model answers the prompt instead of labeling it:

```python
REJECT_PATTERNS = [
    r"(?i)^I need", r"(?i)^Yes", r"(?i)^Sure",
    r"(?i)^Here", r"(?i)^Let me", r"(?i)^The ",
]
```

### Critical: `--no-session-persistence`

Always pass `--no-session-persistence` when calling `claude -p` for title generation. Without it, each Haiku call creates a new JSONL session file, polluting the session list. This was learned the hard way after 180 phantom sessions had to be manually cleaned up.

---

## The SwiftBar Plugin

The plugin runs every 5 minutes (controlled by the `.5m.py` filename convention). It scans all session JSONL files, extracts metadata, and renders a SwiftBar dropdown.

### Display Name Priority

Each session shows the best available name:

1. `customTitle` - user-set via `/rename` or auto-generated by the SessionEnd hook
2. `aiSummary` - from batch backfill script (for older sessions)
3. Cleaned first prompt - truncated to ~10 words, filler stripped ("okay", "hey", "can you")

### Performance: Incremental Cache

The plugin caches parsed session metadata in a JSON file. On each refresh, it only re-parses JSONL files whose modification time has changed. This keeps warm refreshes under 50ms even with hundreds of sessions.

```python
def scan_sessions(cache):
    sessions = cache.get("sessions", {})
    for filepath in PROJECT_DIR.glob("*.jsonl"):
        session_id = filepath.stem
        mtime = filepath.stat().st_mtime

        cached = sessions.get(session_id)
        if cached and cached.get("modified") == mtime:
            continue  # Skip unchanged files

        # Parse only changed files...
```

### Active Session Detection

The plugin checks `~/.claude/sessions/*.json` for running PIDs:

```python
def get_active_sessions():
    active = set()
    for f in SESSIONS_DIR.glob("*.json"):
        data = json.load(open(f))
        pid, sid = data.get("pid"), data.get("sessionId")
        if pid and sid:
            try:
                os.kill(pid, 0)  # Check if process exists (doesn't actually kill)
                active.add(sid)
            except ProcessLookupError:
                pass
    return active
```

### Dark Mode Support

macOS dark mode makes light-themed text invisible on the dark menu background. The plugin detects the current mode at startup and swaps the color palette:

```python
import subprocess

def is_dark_mode():
    try:
        result = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True, text=True, timeout=2,
        )
        return result.stdout.strip() == "Dark"
    except Exception:
        return False

DARK = is_dark_mode()

# Swap palette based on mode
TEXT_PRIMARY = "#f3f4f6" if DARK else "#1a1a2e"
TEXT_SECONDARY = "#d1d5db" if DARK else "#4b5563"
ACCENT_BLUE = "#4D7AFF" if DARK else "#0019FF"
```

Since SwiftBar refreshes every 5 minutes, mode switches are picked up naturally.

### Resume via osascript

SwiftBar's built-in `param2=` parameter splits on spaces, breaking multi-word commands. The workaround is a tiny helper script:

```bash
#!/bin/bash
cd ~/your-project-dir
if [ -n "$1" ]; then
    osascript -e "tell application \"Terminal\" to do script \"cd ~/your-project-dir && claude --resume $1\""
else
    osascript -e "tell application \"Terminal\" to do script \"cd ~/your-project-dir && claude --resume\""
fi
```

Each menu item calls this script with the session ID as an argument.

---

## Gotchas

- **Project hash in path**: The `~/.claude/projects/` directory uses a hash derived from your working directory. The path `-Users-me-myproject` comes from `/Users/me/myproject`. You need to find your own project hash.

- **Haiku title quality**: Haiku occasionally answers the prompt instead of labeling it ("I need to check the database" instead of "Database migration fix"). The reject patterns catch most cases, but some slip through. Tuning the system prompt and examples is an ongoing process.

- **SwiftBar param splitting**: Any osascript command with spaces must go through a helper script, not SwiftBar's built-in parameter passing.

- **Cache file corruption**: If the plugin crashes mid-write, the cache can become invalid JSON. Writing to a temp file and atomically renaming avoids this:

```python
tmp = cache_file.with_suffix(".tmp")
with open(tmp, "w") as f:
    json.dump(cache, f)
tmp.rename(cache_file)
```

---

## Build Your Own

This was built entirely with Claude Code in a few sessions. The plugin is ~200 lines of Python, the hook is ~100 lines, and the helper script is 5 lines of bash. Zero pip dependencies - just Python 3 standard library, SwiftBar, and the Claude CLI.

If you want to build your own version:

1. **Start with the hook** - the auto-titling SessionEnd hook is the highest-value piece. Even without SwiftBar, it makes `claude --resume` dramatically more usable.

2. **Install SwiftBar** - it's a free, open-source menu bar plugin framework. Any Python script with the right filename convention becomes a menu bar item.

3. **Adapt to your terminal** - the resume script uses Terminal.app via osascript. iTerm2, Kitty, Warp, and others have their own automation APIs.

4. **Adapt to your project** - the project directory path is derived from your working directory. Find yours in `~/.claude/projects/`.

The value of sharing this is not the code (you can vibe-code the whole thing from this description). It's the pattern: hook into SessionEnd, generate a title with Haiku, write it back as `custom-title` to the JSONL, and surface it in a menu bar. That loop is what makes session management go from painful to invisible.
