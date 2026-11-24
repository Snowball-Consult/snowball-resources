"""Synthetic transcript fixtures for the catch-me-up history helper.

Every fixture is built in memory from small helper functions so the shapes
stay readable. Shapes mirror Claude Code 2.1.27x transcript records
(type/uuid/parentUuid chain, system/compact_boundary with compactMetadata,
isCompactSummary user records, isSidechain flags, <command-name> records).
No real conversation content is used.
"""
import json
import uuid as _uuid

VERSION = "2.1.272"


def _uid():
    return str(_uuid.uuid4())


class Builder:
    """Appends records and keeps the parentUuid chain for you."""

    def __init__(self, session_id, ts_start=1_000_000):
        self.sid = session_id
        self.lines = []          # raw JSON strings (or raw bytes for malformed)
        self.last = None         # uuid of last chain record
        self.ts = ts_start
        self.prompt_id = None

    def _base(self, typ, parent=None, sidechain=False):
        self.ts += 60
        return {
            "parentUuid": self.last if parent is None else parent,
            "isSidechain": sidechain,
            "type": typ,
            "uuid": _uid(),
            "timestamp": f"2026-09-01T00:{(self.ts // 60) % 60:02d}:00.000Z",
            "sessionId": self.sid,
            "version": VERSION,
            "cwd": "/tmp/fixture",
            "userType": "external",
            "entrypoint": "cli",
        }

    def add(self, rec):
        self.lines.append(json.dumps(rec))
        if rec.get("uuid") and not rec.get("isSidechain"):
            self.last = rec["uuid"]
        return rec

    def human(self, text, **extra):
        self.prompt_id = _uid()
        r = self._base("user")
        r.update({"promptId": self.prompt_id, "origin": {"kind": "human"},
                  "promptSource": "typed",
                  "message": {"role": "user", "content": text}})
        r.update(extra)
        return self.add(r)

    def command(self, name, args=""):
        """A typed slash command, as Claude Code records it."""
        self.prompt_id = _uid()
        r = self._base("user")
        r.update({"promptId": self.prompt_id,
                  "message": {"role": "user", "content":
                              f"<command-name>/{name}</command-name>\n"
                              f"            <command-message>{name}</command-message>\n"
                              f"            <command-args>{args}</command-args>"}})
        return self.add(r)

    def skill_expansion(self, text):
        r = self._base("user")
        r.update({"promptId": self.prompt_id, "isMeta": True,
                  "message": {"role": "user", "content": [{"type": "text", "text": text}]}})
        return self.add(r)

    def assistant(self, text=None, tool=None, thinking=None):
        content = []
        if thinking:
            content.append({"type": "thinking", "thinking": thinking, "signature": "x"})
        if text:
            content.append({"type": "text", "text": text})
        tid = None
        if tool:
            tid = "toolu_" + _uid()[:8]
            name, inp = tool
            content.append({"type": "tool_use", "id": tid, "name": name, "input": inp})
        r = self._base("assistant")
        r.update({"requestId": "req_x",
                  "message": {"model": "claude-test", "id": "msg_x", "type": "message",
                              "role": "assistant", "content": content}})
        self.add(r)
        return tid

    def tool_result(self, tid, text):
        r = self._base("user")
        r.update({"promptId": self.prompt_id,
                  "message": {"role": "user", "content": [
                      {"tool_use_id": tid, "type": "tool_result", "content": text}]},
                  "toolUseResult": {"stdout": text}})
        return self.add(r)

    def attachment(self, kind="skill_listing"):
        r = self._base("attachment")
        r.update({"attachment": {"type": kind, "content": "..."}})
        return self.add(r)

    def compact(self, summary_text, trigger="manual", pre=200000, post=20000,
                drop_logical_parent=False):
        logical = self.last
        r = self._base("system")
        r.update({"parentUuid": None, "subtype": "compact_boundary",
                  "logicalParentUuid": "missing-" + _uid() if drop_logical_parent else logical,
                  "content": "Conversation compacted", "level": "info",
                  "compactMetadata": {"trigger": trigger, "preTokens": pre,
                                      "postTokens": post,
                                      "cumulativeDroppedTokens": pre - post,
                                      "durationMs": 1000}})
        self.add(r)
        s = self._base("user")
        self.prompt_id = _uid()
        s.update({"promptId": self.prompt_id, "isVisibleInTranscriptOnly": True,
                  "isCompactSummary": True,
                  "message": {"role": "user", "content":
                              "This session is being continued from a previous conversation "
                              "that ran out of context. The summary below covers the earlier "
                              "portion of the conversation.\n\nSummary:\n" + summary_text}})
        return self.add(s)

    def meta(self, typ, **fields):
        d = {"type": typ, "sessionId": self.sid}
        d.update(fields)
        self.lines.append(json.dumps(d))

    def sidechain(self, text):
        r = self._base("assistant", parent=None, sidechain=True)
        r["parentUuid"] = None
        r["message"] = {"role": "assistant", "content": [{"type": "text", "text": text}]}
        return self.add(r)

    def write(self, path, trailing_partial=None, malformed_at=None):
        lines = list(self.lines)
        if malformed_at is not None:
            lines.insert(malformed_at, '{"type": "user", "uuid": "broken"')
        data = "\n".join(lines) + "\n"
        if trailing_partial:
            data += trailing_partial  # no newline: a write in progress
        with open(path, "w") as fh:
            fh.write(data)
        return path


# ---------------------------------------------------------------- fixtures

def simple(sid):
    """Ordinary single-thread session, uncompacted, ends with agreed next step."""
    b = Builder(sid)
    b.meta("last-prompt", lastPrompt="", leafUuid=None)
    b.attachment("hook_success")
    b.human("I need to dedupe the contacts export before we upload it to the CRM. "
            "Constraint: never drop a row that has a phone number.")
    b.assistant(text="Plan: normalize emails, group by email, keep the row with a phone.",
                thinking="private reasoning must not leak")
    tid = b.assistant(text="Checking the export.", tool=("Bash", {"command": "wc -l export.csv",
                                                                   "description": "Count rows"}))
    b.tool_result(tid, "1204 export.csv")
    b.assistant(text="1204 rows. Wrote dedupe.py. 37 duplicates found, 0 phone rows dropped.")
    b.human("Good. Next step: run it against the March file too, tomorrow.")
    b.assistant(text="Agreed. Stopping here; March file run is the next step.")
    b.meta("custom-title", customTitle="contacts-dedupe")
    return b


def compacted_with_history(sid):
    """Compaction happened; the original records are still in the file."""
    b = simple(sid)
    b.compact("1. Primary request: dedupe contacts export.\n2. Next: run on March file.")
    b.human("Back. Run it on the March file now.")
    b.assistant(text="Ran on March: 12 duplicates, 0 phone rows dropped.")
    return b


def summary_only(sid):
    """Compaction whose pre-compaction records are not in the file."""
    b = Builder(sid)
    b.compact("1. Primary request: migrate the billing cron to the new scheduler.\n"
              "2. Decision: keep the old cron until the first successful run.",
              trigger="auto", drop_logical_parent=True)
    b.human("Where were we?")
    b.assistant(text="Per the summary, the cron migration is pending its first run.")
    return b


def mentions_compaction(sid):
    """Nobody compacted; the text merely talks about compacting."""
    b = Builder(sid)
    b.human("Before we compact, is everything saved? I want to /compact soon.")
    b.assistant(text="Safe to compact. Everything is on disk. Compaction will keep the summary.")
    b.human("ok, holding off on the compaction for now, let's keep going on the parser")
    b.assistant(text="Continuing with the parser.")
    return b


def pivot(sid):
    """Earlier thread left open, then an explicit pivot to a second topic."""
    b = Builder(sid)
    b.human("Design the conflict-handling rules for the sync: CRM edits vs sheet edits.")
    b.assistant(text="Proposal: automatic overwrite from the sheet.")
    b.human("No. Automatic overwrites could erase sales corrections. Use a review queue instead.")
    b.assistant(text="Review queue it is. Draft written to sync-rules.md; still needs the tie-break rule.")
    b.human("Park that. Different topic: the weekly report email is going to the wrong list.")
    b.assistant(text="Found it: the list id in report.py points at the test list. Proposed fix: switch to LIST_PROD.")
    b.human("Don't change it yet, I want to confirm with Sam first.")
    b.assistant(text="Understood. No change made. Waiting on your confirmation with Sam.")
    return b


def with_prior_recap(sid):
    """A previous /catch-me-up exchange, then real work, then the current invocation."""
    b = simple(sid)
    b.command("catch-me-up", "brief")
    b.skill_expansion("Base directory for this skill: /x/catch-me-up\n[expanded instructions]")
    tid = b.assistant(text="Running the history helper.",
                      tool=("Bash", {"command": "python3 /x/scripts/session_history.py"}))
    b.tool_result(tid, "# Session history digest ...")
    b.assistant(text="Dedupe done; next: March file. (recap output)")
    b.human("Correction: the March file must be deduped by phone, not by email.")
    b.assistant(text="Noted: March dedupe keys on phone.")
    b.command("catch-me-up", "full")
    b.skill_expansion("Base directory for this skill: /x/catch-me-up\n[expanded instructions]")
    tid = b.assistant(text="Running helper.", tool=("Bash", {"command": "python3 x"}))
    b.tool_result(tid, "digest")
    return b


def abandoned_branch(sid):
    """A /rewind left dead records: they share the file but not the active path."""
    b = simple(sid)
    fork_point = b.last
    dead = b.human("Actually, also rename the columns.")          # abandoned
    b.assistant(text="Renaming columns... (abandoned work)")
    # rewind: continue from fork_point
    b.last = fork_point
    b.human("Ignore that. Just confirm the row count.")
    b.assistant(text="Row count confirmed: 1204.")
    b.sidechain("Subagent-only chatter that must be excluded.")
    return b


def unknown_schema(sid):
    b = Builder(sid)
    b.human("hello")
    b.assistant(text="hi")
    # a chain record whose version is from an unrecognised major line
    r = b._base("user")
    r["version"] = "9.0.0"
    r["message"] = {"role": "user", "content": "future format"}
    b.add(r)
    return b


def long_session(sid, turns=120):
    """Many turns with bulky tool output, to exercise the output budget."""
    b = Builder(sid)
    b.human("Origin: build the invoice parser for the finance team. Constraint: PDF only.")
    b.assistant(text="Starting with the PDF text extraction.")
    for i in range(turns):
        b.human(f"Turn {i}: handle case {i} of the invoice layouts.")
        tid = b.assistant(text=f"Working on layout {i}. " + ("detail " * 80),
                          tool=("Read", {"file_path": f"/tmp/layout_{i}.pdf"}))
        b.tool_result(tid, "PDF TEXT " * 2000)
        b.assistant(text=f"Layout {i} handled.")
    b.human("Last: the multi-page totals are still wrong on layout 117.")
    b.assistant(text="Found the off-by-one in page merging; fix proposed, not yet applied.")
    return b


FIXTURES = {
    "simple": simple,
    "compacted_with_history": compacted_with_history,
    "summary_only": summary_only,
    "mentions_compaction": mentions_compaction,
    "pivot": pivot,
    "with_prior_recap": with_prior_recap,
    "abandoned_branch": abandoned_branch,
    "unknown_schema": unknown_schema,
    "long_session": long_session,
}
