#!/usr/bin/env python3
"""Read-only history digest for one Claude Code session transcript.

Resolves the exact session's JSONL under the configured data location,
follows the active conversation path (parentUuid chain, bridging compaction
boundaries via logicalParentUuid), cuts off immediately before the current
/catch-me-up invocation, and prints a bounded digest with explicit
compaction and coverage metadata.

Standard library only. Never writes anything.

Transcript shapes were validated against Claude Code 2.1.268-2.1.272:
  - chain records: type user|assistant|system|attachment with uuid/parentUuid
  - compaction:    system/compact_boundary (compactMetadata.trigger, parentUuid
                   null, logicalParentUuid -> pre-compaction tail) followed by a
                   user record with isCompactSummary true
  - subagents:     isSidechain true (same file) or <session>/subagents/*.jsonl
  - slash command: user record whose content is "<command-name>/x</command-name>..."
                   followed by an isMeta user record holding the expansion
"""
import argparse
import glob
import json
import os
import re
import sys

KNOWN_VERSION_PREFIXES = ("2.1.",)
CHAIN_TYPES = {"user", "assistant", "system", "attachment"}
META_TYPES = {"last-prompt", "mode", "permission-mode", "atis-latch", "bridge-session",
              "ai-title", "custom-title", "agent-name", "file-history-snapshot",
              "file-history-delta", "queue-operation", "cost-state", "summary"}
SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,80}$")
COMMAND_RE = re.compile(r"<command-name>/([^<\s]+)</command-name>")
COMMAND_ARGS_RE = re.compile(r"<command-args>(.*?)</command-args>", re.S)
USAGE = "Usage: /catch-me-up [brief|full]"


# ------------------------------------------------------------------ arguments

def normalize_args(raw):
    """Default -> brief; case/whitespace normalised; anything else -> usage only."""
    if raw is None:
        return "brief"
    v = raw.strip().lower()
    if v == "":
        return "brief"
    if v in ("brief", "full"):
        return v
    return USAGE


# ------------------------------------------------------------------ locating

def project_dir_name(cwd):
    """Claude Code derives the project folder from the cwd by replacing every
    character that is not a letter or digit with '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(cwd))


def locate(config_dir, session_id, cwd):
    projects = os.path.join(config_dir, "projects")
    preferred = os.path.join(projects, project_dir_name(cwd), session_id + ".jsonl")
    if os.path.isfile(preferred):
        return preferred, []
    hits = sorted(glob.glob(os.path.join(projects, "*", session_id + ".jsonl")))
    if not hits:
        return None, []
    return hits[0], hits[1:]


# ------------------------------------------------------------------ parsing

def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _tool_summary(name, inp):
    if not isinstance(inp, dict):
        return name
    parts = []
    for key in ("description", "command", "file_path", "pattern", "path", "url",
                "skill", "query", "prompt"):
        v = inp.get(key)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip().replace("\n", " ")[:160])
        if len(parts) == 2:
            break
    return f"{name}: " + " | ".join(parts) if parts else name


def slim(rec):
    """Project a raw record onto the small shape the digest needs."""
    typ = rec.get("type")
    s = {
        "uuid": rec.get("uuid"), "parent": rec.get("parentUuid"),
        "logical_parent": rec.get("logicalParentUuid"), "type": typ,
        "subtype": rec.get("subtype"), "ts": rec.get("timestamp"),
        "sidechain": bool(rec.get("isSidechain")), "meta": bool(rec.get("isMeta")),
        "compact_summary": bool(rec.get("isCompactSummary")),
        "prompt_id": rec.get("promptId"), "version": rec.get("version"),
        "text": "", "tools": [], "results": [], "command": None, "command_args": None,
        "compact": None,
    }
    msg = rec.get("message") if isinstance(rec.get("message"), dict) else {}
    content = msg.get("content")
    if typ == "user":
        s["text"] = _text_of(content)
        if isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    s["results"].append(str(c or "")[:400])
        m = COMMAND_RE.search(s["text"])
        if m:
            s["command"] = m.group(1)
            a = COMMAND_ARGS_RE.search(s["text"])
            s["command_args"] = (a.group(1).strip() if a else "")
    elif typ == "assistant":
        s["text"] = _text_of(content)
        if isinstance(content, list):
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    s["tools"].append(_tool_summary(b.get("name", "?"), b.get("input")))
    elif typ == "system" and rec.get("subtype") == "compact_boundary":
        md = rec.get("compactMetadata") or {}
        s["compact"] = {"trigger": md.get("trigger"), "pre_tokens": md.get("preTokens"),
                        "post_tokens": md.get("postTokens"), "ts": rec.get("timestamp")}
    return s


def parse_file(path, max_bytes):
    """Line-bounded parse. Returns (records, meta, parse_info)."""
    records, meta = [], {}
    info = {"lines": 0, "malformed_lines": 0, "malformed_line_numbers": [],
            "trailing_partial": False, "byte_cap_hit": False, "bytes": 0,
            "versions": {}, "unknown_types": {}, "meta_records": 0, "attachments": 0}
    size = os.path.getsize(path)
    info["file_bytes"] = size
    read = 0
    with open(path, "rb") as fh:
        while True:
            line = fh.readline()
            if not line:
                break
            read += len(line)
            info["lines"] += 1
            if read > max_bytes:
                info["byte_cap_hit"] = True
                break
            if not line.endswith(b"\n"):
                # last line without newline: a write in progress, or a truncated file
                try:
                    json.loads(line)
                except Exception:
                    info["trailing_partial"] = True
                    break
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except Exception:
                info["malformed_lines"] += 1
                if len(info["malformed_line_numbers"]) < 20:
                    info["malformed_line_numbers"].append(info["lines"])
                continue
            if not isinstance(rec, dict):
                info["malformed_lines"] += 1
                continue
            typ = rec.get("type")
            if typ in CHAIN_TYPES and rec.get("uuid"):
                v = rec.get("version")
                if v:
                    info["versions"][v] = info["versions"].get(v, 0) + 1
                if typ == "attachment":
                    info["attachments"] += 1
                records.append(slim(rec))  # attachments stay: they are links in the chain
            elif typ in META_TYPES:
                info["meta_records"] += 1
                if typ == "custom-title":
                    meta["title"] = rec.get("customTitle")
                elif typ == "ai-title" and "title" not in meta:
                    meta["ai_title"] = rec.get("aiTitle")
            else:
                key = str(typ)
                info["unknown_types"][key] = info["unknown_types"].get(key, 0) + 1
    info["bytes"] = read
    return records, meta, info


# ------------------------------------------------------------------ active path

def active_path(records):
    """Walk parentUuid from the last on-chain record; bridge compaction via
    logicalParentUuid. Returns (path_chronological, excluded_counts, flags)."""
    by_uuid = {}
    sidechain = 0
    for r in records:
        if r["sidechain"]:
            sidechain += 1
            continue
        by_uuid[r["uuid"]] = r
    leaf = None
    for r in reversed(records):
        if not r["sidechain"] and r["type"] in ("user", "assistant", "system"):
            leaf = r
            break
    flags = {"root_reached": False, "dangling_parent": False, "cycle": False}
    path = []
    seen = set()
    cur = leaf
    while cur is not None:
        if cur["uuid"] in seen:
            flags["cycle"] = True
            break
        seen.add(cur["uuid"])
        path.append(cur)
        nxt = cur["parent"]
        if nxt is None and cur["compact"] is not None:
            nxt = cur["logical_parent"]
        if nxt is None:
            flags["root_reached"] = True
            break
        if nxt not in by_uuid:
            flags["dangling_parent"] = True
            flags["dangling_at"] = cur["uuid"]
            break
        cur = by_uuid[nxt]
    path.reverse()
    excluded = {"sidechain": sidechain, "off_path": len(by_uuid) - len(path)}
    return path, excluded, flags


# ------------------------------------------------------------------ turns

def is_human(r):
    return (r["type"] == "user" and not r["meta"] and not r["compact_summary"]
            and r["command"] is None and not r["results"] and r["text"].strip() != "")


def build_turns(path, skill_name):
    """Group the path into turns and apply the recap cutoff."""
    # cutoff: the last invocation of this skill on the path
    cut_idx, cut_args = None, None
    invocations = [i for i, r in enumerate(path) if r["command"] == skill_name]
    if invocations:
        cut_idx = invocations[-1]
        cut_args = path[cut_idx]["command_args"]
    history = path[:cut_idx] if cut_idx is not None else path
    prior_recaps = [i for i in invocations if cut_idx is None or i < cut_idx]

    turns, cur = [], None
    in_recap = False
    for i, r in enumerate(history):
        if r["type"] == "attachment":
            continue  # hook output / skill listings: chain links only, never content
        if r["compact"] is not None:
            turns.append({"kind": "compact_boundary", "ts": r["ts"], "compact": r["compact"],
                          "recap_exchange": False, "items": []})
            cur = None
            continue
        if r["compact_summary"]:
            turns.append({"kind": "compact_summary", "ts": r["ts"], "summary": r["text"],
                          "recap_exchange": False, "items": []})
            cur = None
            continue
        if r["command"] is not None:
            in_recap = (r["command"] == skill_name)
            cur = {"kind": "command", "ts": r["ts"], "command": r["command"],
                   "args": r["command_args"], "recap_exchange": in_recap, "items": []}
            turns.append(cur)
            continue
        if is_human(r):
            in_recap = False
            cur = {"kind": "human", "ts": r["ts"], "human": r["text"],
                   "recap_exchange": False, "items": []}
            turns.append(cur)
            continue
        if cur is None:
            cur = {"kind": "continuation", "ts": r["ts"], "recap_exchange": in_recap, "items": []}
            turns.append(cur)
        if r["type"] == "assistant":
            if r["text"].strip():
                cur["items"].append({"k": "assistant", "text": r["text"]})
            for t in r["tools"]:
                cur["items"].append({"k": "tool", "text": t})
        elif r["type"] == "user" and r["results"]:
            for res in r["results"]:
                cur["items"].append({"k": "result", "text": res})
        elif r["type"] == "user" and r["meta"]:
            pass  # skill expansions / local-command caveats: historical noise
    cutoff = {"found": cut_idx is not None, "args": cut_args,
              "ts": path[cut_idx]["ts"] if cut_idx is not None else None}
    return turns, cutoff, len(prior_recaps)


# ------------------------------------------------------------------ verdicts

def compaction_verdict(turns, info, flags, status_ok):
    events = [t["compact"] for t in turns if t["kind"] == "compact_boundary"]
    summaries = [t for t in turns if t["kind"] == "compact_summary"]
    if events or summaries:
        return "Yes", events, "compact_boundary/compaction-summary metadata on the active path"
    if not status_ok:
        return "Unknown", events, "transcript unavailable"
    reasons = []
    if info["malformed_lines"]:
        reasons.append("malformed records in the file")
    if info["byte_cap_hit"]:
        reasons.append("byte cap hit before end of file")
    if info["unknown_types"]:
        reasons.append("unrecognised record types: " + ", ".join(sorted(info["unknown_types"])))
    bad_versions = [v for v in info["versions"] if not v.startswith(KNOWN_VERSION_PREFIXES)]
    if bad_versions:
        reasons.append("unvalidated transcript schema version(s): " + ", ".join(sorted(bad_versions)))
    if not info["versions"]:
        reasons.append("no version stamps on records")
    if not flags.get("root_reached"):
        reasons.append("active path does not reach a root record")
    if flags.get("dangling_parent"):
        reasons.append("active path has a missing parent record")
    if reasons:
        return "Unknown", events, "; ".join(reasons)
    return "No", events, "full parse of a validated-schema transcript; active path reaches its root with no compaction records"


def history_verdict(turns, info, flags, budget, status_ok):
    if not status_ok:
        return "Partial", "transcript unavailable"
    first = next((t for t in turns if t["kind"] in ("human", "compact_summary", "compact_boundary")), None)
    if first is not None and first["kind"] in ("compact_summary", "compact_boundary") and flags.get("dangling_parent"):
        return "Summary-only", "the path begins at a compaction summary whose pre-compaction records are not in the file"
    reasons = []
    if info["malformed_lines"]:
        reasons.append(f"{info['malformed_lines']} malformed line(s) skipped")
    if info["byte_cap_hit"]:
        reasons.append("byte cap hit; tail of the file not read")
    if flags.get("dangling_parent"):
        reasons.append("earliest records not resolvable (missing parent)")
    if budget["truncated"]:
        reasons.append("output budget dropped detail for turns " +
                       ", ".join(f"{a}-{b}" for a, b in budget["skipped_ranges"]))
    if reasons:
        return "Partial", "; ".join(reasons)
    return "Full", "origin through stopping point reviewed from original records"


# ------------------------------------------------------------------ rendering

def _clip(s, n):
    s = s.strip()
    return s if len(s) <= n else s[:n].rstrip() + f" …[+{len(s) - n} chars]"


def _fmt_ts(ts):
    if not ts:
        return "?"
    return ts[:16].replace("T", " ") + "Z"


def render(turns, budget_chars, min_level=0):
    """Render turns within a character budget. Origin and the tail are kept in
    full; the middle is shrunk first, then reduced to human prompts only."""
    n = len(turns)
    tail_start = max(0, n - 8)
    last_summary = max((i for i, t in enumerate(turns) if t["kind"] == "compact_summary"), default=-1)

    def render_turn(i, t, level):
        # level 0 = full, 1 = compact, 2 = human prompts only
        out = []
        head = f"## Turn {i + 1} · {_fmt_ts(t['ts'])}"
        if t.get("recap_exchange"):
            head += " · (previous /catch-me-up recap exchange - not new work)"
        if t["kind"] == "compact_boundary":
            c = t["compact"]
            return [f"## Turn {i + 1} · {_fmt_ts(t['ts'])} · COMPACTION ({c.get('trigger')}, "
                    f"{c.get('pre_tokens')} -> {c.get('post_tokens')} tokens)"]
        if t["kind"] == "compact_summary":
            # later summaries subsume earlier ones: keep the last in full, clip the rest
            lim = 6000 if (i == last_summary and level < 2) else 1500
            return [f"## Turn {i + 1} · {_fmt_ts(t['ts'])} · COMPACTION SUMMARY (generated by Claude at compaction time)",
                    "> " + _clip(t["summary"], lim).replace("\n", "\n> ")]
        if t["kind"] == "command":
            return [head + f" · local command /{t['command']} {_clip(t.get('args') or '', 200)}".rstrip()]
        out.append(head)
        if t["kind"] == "human":
            lim = 4000 if i == 0 else (1500 if level == 0 else 800)
            out.append("> " + _clip(t["human"], lim).replace("\n", "\n> "))
        if level >= 2:
            return out
        a_lim = 1500 if level == 0 else 300
        r_lim = 240 if level == 0 else 0
        t_cap = 30 if level == 0 else 3
        t_len = 220 if level == 0 else 100
        tools_seen, tools_total = 0, sum(1 for it in t["items"] if it["k"] == "tool")
        for it in t["items"]:
            if it["k"] == "assistant":
                out.append("- assistant: " + _clip(it["text"], a_lim).replace("\n", " "))
            elif it["k"] == "tool":
                tools_seen += 1
                if tools_seen <= t_cap:
                    out.append("- tool: " + _clip(it["text"], t_len).replace("\n", " "))
                elif tools_seen == t_cap + 1:
                    out.append(f"- tools: …{tools_total - t_cap} more tool calls in this turn")
            elif it["k"] == "result" and r_lim and tools_seen <= t_cap:
                out.append("- result: " + _clip(it["text"], r_lim).replace("\n", " "))
        return out

    def assemble(levels):
        parts = []
        for i, t in enumerate(turns):
            parts.append("\n".join(render_turn(i, t, levels[i])))
        return "\n\n".join(parts)

    levels = [min_level] * n
    text = assemble(levels)
    budget = {"truncated": False, "skipped_ranges": [], "chars": len(text), "compacted_turns": False}
    if len(text) <= budget_chars:
        return text, budget
    # pass 1: compact the middle (keep first turn and tail full)
    for i in range(1, tail_start):
        levels[i] = 1
    text = assemble(levels)
    if len(text) <= budget_chars:
        budget.update({"chars": len(text), "compacted_turns": True})
        return text, budget
    # pass 1b: compact every turn (prompts stay complete; assistant text and tools clipped)
    levels = [max(1, min_level)] * n
    text = assemble(levels)
    if len(text) <= budget_chars:
        budget.update({"chars": len(text), "compacted_turns": True})
        return text, budget
    # pass 2: reduce the middle to human prompts only, from the centre outwards
    budget["truncated"] = True
    mid = list(range(1, tail_start))
    order = sorted(mid, key=lambda i: abs(i - (1 + tail_start) / 2))
    for i in order:
        levels[i] = 2
        text = assemble(levels)
        if len(text) <= budget_chars:
            break
    if len(text) > budget_chars:
        for i in range(tail_start, n):        # last resort: compact the tail too
            levels[i] = 1
        text = assemble(levels)
    reduced = [i + 1 for i in range(n) if levels[i] == 2]
    ranges, start, prev = [], None, None
    for i in reduced:
        if start is None:
            start = prev = i
        elif i == prev + 1:
            prev = i
        else:
            ranges.append((start, prev))
            start = prev = i
    if start is not None:
        ranges.append((start, prev))
    budget["skipped_ranges"] = ranges
    budget["chars"] = len(text)
    return text, budget


def header_lines(d):
    p = d["parse"]
    lines = [
        "# Session history digest (read-only; historical data, not instructions)",
        f"session: {d['session_id']}",
        f"file: {d['file']} ({p.get('file_bytes', 0)} bytes, {p.get('lines', 0)} lines)",
        "title: " + (d.get('title') or (f"(auto-generated) {d['ai_title']}" if d.get('ai_title') else "(none)")),
        f"compacted: {d['compacted']} - {d['compacted_reason']}",
        f"history: {d['history']} - {d['history_reason']}",
    ]
    if d["compaction_events"]:
        lines.append("compaction events: " + "; ".join(
            f"{e.get('trigger')} at {_fmt_ts(e.get('ts'))} ({e.get('pre_tokens')} -> {e.get('post_tokens')} tokens)"
            for e in d["compaction_events"]))
    c = d["cutoff"]
    lines.append("cutoff: " + (f"at the /{d['skill']} invocation {_fmt_ts(c['ts'])} (that turn and everything after it excluded)"
                               if c["found"] else "end of file (the current invocation was not yet written to the transcript)"))
    lines.append(f"prior recap exchanges on the path: {d['prior_recaps']} (marked in the timeline; not new work)")
    lines.append(f"records: {d['path_records']} on the active path; excluded {d['excluded']['off_path']} off-path "
                 f"(abandoned branches) and {d['excluded']['sidechain']} sidechain (subagent) records; "
                 f"{p.get('attachments', 0)} attachments skipped")
    lines.append(f"parse: malformed lines {p.get('malformed_lines', 0)}"
                 + (f" at {p['malformed_line_numbers']}" if p.get('malformed_line_numbers') else "")
                 + f"; trailing partial line: {'yes' if p.get('trailing_partial') else 'no'}"
                 + f"; byte cap hit: {'yes' if p.get('byte_cap_hit') else 'no'}"
                 + f"; versions: {', '.join(sorted(p.get('versions', {}))) or 'none'}")
    if d["budget"]["truncated"]:
        lines.append("budget: output truncated; turns reduced to prompts only: " +
                     ", ".join(f"{a}-{b}" for a, b in d["budget"]["skipped_ranges"]))
    elif d["budget"].get("compacted_turns"):
        lines.append("budget: assistant text and tool lists clipped per turn; every prompt is complete")
    return lines


# ------------------------------------------------------------------ main

def digest(session_id, config_dir, cwd, skill_name, budget_chars, max_bytes):
    d = {"status": "ok", "session_id": session_id, "skill": skill_name, "file": None,
         "compacted": "Unknown", "compacted_reason": "", "history": "Partial", "history_reason": "",
         "compaction_events": [], "turns": [], "cutoff": {"found": False, "args": None, "ts": None},
         "prior_recaps": 0, "excluded": {"sidechain": 0, "off_path": 0}, "path_records": 0,
         "parse": {}, "budget": {"truncated": False, "skipped_ranges": [], "chars": 0},
         "title": None, "ai_title": None, "text": ""}
    if not SESSION_ID_RE.match(session_id or ""):
        d.update(status="error", error="invalid session id",
                 compacted_reason="session id rejected", history_reason="no transcript read")
        return d
    path, others = locate(config_dir, session_id, cwd)
    if path is None:
        d.update(status="not_found", error=f"no transcript for {session_id} under {os.path.join(config_dir, 'projects')}",
                 compacted_reason="transcript not found", history_reason="transcript not found")
        return d
    d["file"] = path
    if others:
        d["other_matches"] = others
    try:
        records, meta, info = parse_file(path, max_bytes)
    except (OSError, PermissionError) as e:
        d.update(status="error", error=f"cannot read transcript: {e}",
                 compacted_reason="transcript unreadable", history_reason="transcript unreadable")
        return d
    d["parse"] = info
    d["title"] = meta.get("title")
    d["ai_title"] = meta.get("ai_title")
    path_recs, excluded, flags = active_path(records)
    d["excluded"] = excluded
    d["path_records"] = len(path_recs)
    d["path_flags"] = flags
    turns, cutoff, prior = build_turns(path_recs, skill_name)
    d["cutoff"] = cutoff
    d["prior_recaps"] = prior
    text, budget = render(turns, budget_chars)
    d["budget"] = budget
    d["compacted"], d["compaction_events"], d["compacted_reason"] = compaction_verdict(turns, info, flags, True)
    d["history"], d["history_reason"] = history_verdict(turns, info, flags, budget, True)
    d["turns"] = [{k: v for k, v in t.items() if k != "items"} | {"n_items": len(t["items"])} for t in turns]
    d["text"] = text
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--session-id")
    ap.add_argument("--config-dir", default=os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude"))
    ap.add_argument("--cwd", default=os.getcwd())
    ap.add_argument("--skill-name", default="catch-me-up")
    ap.add_argument("--budget-chars", type=int, default=60000)
    ap.add_argument("--max-bytes", type=int, default=400 * 1024 * 1024)
    ap.add_argument("--json", action="store_true", help="machine-readable output (tests)")
    ap.add_argument("--normalize-args", nargs="?", const="", default=None,
                    help="print the normalised mode for the given skill argument text and exit")
    a = ap.parse_args(argv)

    if a.normalize_args is not None:
        print(normalize_args(a.normalize_args))
        return 0
    if not a.session_id:
        ap.error("--session-id is required")
    d = digest(a.session_id, a.config_dir, a.cwd, a.skill_name, a.budget_chars, a.max_bytes)
    if a.json:
        print(json.dumps(d, indent=1))
        return 0
    if d["status"] != "ok":
        print("# Session history digest")
        print(f"status: {d['status']} - {d.get('error')}")
        print(f"compacted: {d['compacted']} - {d['compacted_reason']}")
        print(f"history: {d['history']} - {d['history_reason']}")
        print("Fallback: recap from the conversation visible in context and say that the transcript was unavailable.")
        return 0
    print("\n".join(header_lines(d)))
    print()
    print(d["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
