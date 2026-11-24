"""Deterministic tests for scripts/session_history.py and scripts/check_recap.py.

Run:  python3 -m unittest discover -s tests -v   (from the skill directory)
Only the standard library is used. Fixtures are synthetic (tests/make_fixtures.py).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

import make_fixtures as mf  # noqa: E402

SID = "11111111-2222-4333-8444-555555555555"


class Env:
    """A throwaway config dir laid out like ~/.claude/projects/<project>/<sid>.jsonl."""

    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.config = os.path.join(self.tmp.name, "cfg")
        self.cwd = os.path.join(self.tmp.name, "work dir")
        os.makedirs(self.cwd)
        self.project = os.path.join(self.config, "projects", "-tmp-x-work-dir")
        os.makedirs(self.project)

    def path(self, sid=SID):
        return os.path.join(self.project, sid + ".jsonl")

    def run(self, sid=SID, extra=(), as_json=True):
        cmd = [sys.executable, os.path.join(SCRIPTS, "session_history.py"),
               "--session-id", sid, "--config-dir", self.config, "--cwd", self.cwd]
        if as_json:
            cmd.append("--json")
        cmd += list(extra)
        p = subprocess.run(cmd, capture_output=True, text=True)
        self.assert_no_secret_leak(p.stdout)
        if as_json:
            self.last_raw = p.stdout
            return json.loads(p.stdout)
        return p

    @staticmethod
    def assert_no_secret_leak(out):
        assert "private reasoning must not leak" not in out, "thinking block leaked"

    def cleanup(self):
        self.tmp.cleanup()


def build(env, name, sid=SID, **kw):
    b = mf.FIXTURES[name](sid)
    b.write(env.path(sid), **kw)
    return b


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.env = Env()

    def tearDown(self):
        self.env.cleanup()

    # -- locating the file ------------------------------------------------
    def test_missing_file_is_unknown_not_no(self):
        d = self.env.run()
        self.assertEqual(d["status"], "not_found")
        self.assertEqual(d["compacted"], "Unknown")
        self.assertEqual(d["history"], "Partial")

    def test_bad_session_id_rejected(self):
        d = self.env.run(sid="../../etc/passwd")
        self.assertEqual(d["status"], "error")
        self.assertEqual(d["compacted"], "Unknown")

    def test_finds_file_in_other_project_dir_by_id(self):
        other = os.path.join(self.env.config, "projects", "-elsewhere")
        os.makedirs(other)
        mf.simple(SID).write(os.path.join(other, SID + ".jsonl"))
        d = self.env.run()
        self.assertEqual(d["status"], "ok")
        self.assertTrue(d["file"].endswith(os.path.join("-elsewhere", SID + ".jsonl")))

    def test_honours_config_dir_env(self):
        build(self.env, "simple")
        cmd = [sys.executable, os.path.join(SCRIPTS, "session_history.py"),
               "--session-id", SID, "--cwd", self.env.cwd, "--json"]
        p = subprocess.run(cmd, capture_output=True, text=True,
                           env={**os.environ, "CLAUDE_CONFIG_DIR": self.env.config})
        self.assertEqual(json.loads(p.stdout)["status"], "ok")

    # -- ordinary session -------------------------------------------------
    def test_simple_session_full_and_not_compacted(self):
        build(self.env, "simple")
        d = self.env.run()
        self.assertEqual(d["compacted"], "No")
        self.assertEqual(d["history"], "Full")
        humans = [t["human"] for t in d["turns"] if t["kind"] == "human"]
        self.assertIn("dedupe the contacts export", humans[0])
        self.assertIn("March file", humans[-1])
        self.assertEqual(d["title"], "contacts-dedupe")
        # tool evidence present, bulky stuff bounded, thinking absent
        raw = self.env.last_raw
        self.assertIn("wc -l export.csv", raw)
        self.assertNotIn("private reasoning", raw)

    def test_text_output_has_metadata_header(self):
        build(self.env, "simple")
        p = self.env.run(as_json=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("compacted: No", p.stdout)
        self.assertIn("history: Full", p.stdout)
        self.assertIn("dedupe the contacts export", p.stdout)

    # -- compaction ---------------------------------------------------------
    def test_compaction_with_recovered_history(self):
        build(self.env, "compacted_with_history")
        d = self.env.run()
        self.assertEqual(d["compacted"], "Yes")
        self.assertEqual(d["history"], "Full")
        self.assertEqual(len(d["compaction_events"]), 1)
        self.assertEqual(d["compaction_events"][0]["trigger"], "manual")
        humans = [t["human"] for t in d["turns"] if t["kind"] == "human"]
        self.assertIn("dedupe the contacts export", humans[0])  # origin recovered
        self.assertIn("March file now", humans[-1])
        summaries = [t for t in d["turns"] if t["kind"] == "compact_summary"]
        self.assertEqual(len(summaries), 1)

    def test_summary_only_when_pre_compaction_records_missing(self):
        build(self.env, "summary_only")
        d = self.env.run()
        self.assertEqual(d["compacted"], "Yes")
        self.assertEqual(d["history"], "Summary-only")
        self.assertIn("billing cron", self.env.last_raw)

    def test_text_mentioning_compaction_does_not_trigger_yes(self):
        build(self.env, "mentions_compaction")
        d = self.env.run()
        self.assertEqual(d["compacted"], "No")

    # -- active path ----------------------------------------------------------
    def test_abandoned_branch_and_sidechain_excluded(self):
        build(self.env, "abandoned_branch")
        d = self.env.run()
        self.assertNotIn("abandoned work", self.env.last_raw)
        self.assertNotIn("Subagent-only chatter", self.env.last_raw)
        self.assertIn("Row count confirmed", self.env.last_raw)
        self.assertGreaterEqual(d["excluded"]["off_path"], 2)
        self.assertEqual(d["excluded"]["sidechain"], 1)
        self.assertEqual(d["compacted"], "No")

    def test_cutoff_at_current_invocation_and_prior_recaps_marked(self):
        build(self.env, "with_prior_recap")
        d = self.env.run()
        self.assertTrue(d["cutoff"]["found"])
        self.assertEqual(d["cutoff"]["args"], "full")
        raw = self.env.last_raw
        self.assertNotIn("[expanded instructions]", raw.split('"turns"')[1] if '"turns"' in raw else raw)
        self.assertNotIn('"digest"', raw)          # the current invocation's tool activity
        recap_turns = [t for t in d["turns"] if t.get("recap_exchange")]
        self.assertEqual(len(recap_turns), 1)
        humans = [t["human"] for t in d["turns"] if t["kind"] == "human" and not t.get("recap_exchange")]
        self.assertIn("deduped by phone", humans[-1])  # correction after recap kept as work
        self.assertEqual(d["prior_recaps"], 1)

    def test_cutoff_absent_uses_end_of_file(self):
        build(self.env, "simple")
        d = self.env.run()
        self.assertFalse(d["cutoff"]["found"])

    # -- robustness -------------------------------------------------------------
    def test_trailing_partial_line_does_not_crash_and_stays_full(self):
        build(self.env, "simple", trailing_partial='{"type":"user","uuid":"in-progr')
        d = self.env.run()
        self.assertEqual(d["status"], "ok")
        self.assertTrue(d["parse"]["trailing_partial"])
        self.assertEqual(d["history"], "Full")

    def test_malformed_middle_line_makes_compaction_unknown_and_history_partial(self):
        build(self.env, "simple", malformed_at=3)
        d = self.env.run()
        self.assertEqual(d["status"], "ok")
        self.assertEqual(d["parse"]["malformed_lines"], 1)
        self.assertEqual(d["compacted"], "Unknown")
        self.assertEqual(d["history"], "Partial")

    def test_unknown_schema_version_is_unknown(self):
        build(self.env, "unknown_schema")
        d = self.env.run()
        self.assertEqual(d["compacted"], "Unknown")
        self.assertIn("9.0.0", json.dumps(d["parse"]["versions"]))

    def test_long_session_is_bounded_and_keeps_origin_and_end(self):
        build(self.env, "long_session")
        d = self.env.run(extra=["--budget-chars", "20000"])
        raw = self.env.last_raw
        self.assertLess(len(d["text"]), 24000)
        self.assertIn("build the invoice parser", raw)
        self.assertIn("layout 117", raw)
        self.assertNotIn("PDF TEXT " * 60, raw)  # results are clipped, never dumped
        self.assertTrue(d["budget"]["truncated"])
        self.assertEqual(d["history"], "Partial")
        self.assertTrue(d["budget"]["skipped_ranges"])

    def test_max_bytes_cap_reported(self):
        build(self.env, "long_session")
        d = self.env.run(extra=["--max-bytes", "50000"])
        self.assertTrue(d["parse"]["byte_cap_hit"])
        self.assertEqual(d["compacted"], "Unknown")
        self.assertEqual(d["history"], "Partial")


class RecapCheckerTests(unittest.TestCase):
    BRIEF_OK = """Original purpose was deduping the export; latest position is the March run.

Compacted: No · History: Full · Basis: conversation

### Started
- Dedupe the contacts export without dropping phone rows.

### How we got here
- Normalized emails and grouped; 37 duplicates found.
- You asked for a March run tomorrow.

### Status / left off
- Closed: dedupe script. Open + latest: March run.
- Stopped after agreeing the March run is next.
"""

    def check(self, text, mode="brief"):
        p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "check_recap.py"), "--mode", mode],
                           input=text, capture_output=True, text=True)
        return p.returncode, p.stdout + p.stderr

    def test_valid_brief_passes(self):
        rc, out = self.check(self.BRIEF_OK)
        self.assertEqual(rc, 0, out)
        self.assertIn("OK", out)

    def test_word_limit_enforced(self):
        rc, out = self.check(self.BRIEF_OK.replace("- Normalized", "- " + "word " * 200 + "Normalized"))
        self.assertNotEqual(rc, 0)
        self.assertIn("words", out)

    def test_metadata_line_required(self):
        rc, out = self.check(self.BRIEF_OK.replace("Compacted: No", "Compacted: Maybe"))
        self.assertNotEqual(rc, 0)

    def test_full_metadata_uses_checks(self):
        rc, out = self.check(self.BRIEF_OK, mode="full")
        self.assertNotEqual(rc, 0)  # brief headings and Basis line are wrong for full
        full = self.BRIEF_OK.replace("Basis: conversation", "Checks: Verified") \
            .replace("### Started", "### How this started") \
            .replace("### Status / left off", "### Where we stand\n- Latest: March run open.\n\n### Where we left off")
        rc, out = self.check(full, mode="full")
        self.assertEqual(rc, 0, out)

    def test_progression_must_be_bullets_only(self):
        rc, out = self.check(self.BRIEF_OK.replace("- You asked", "You asked"))
        self.assertNotEqual(rc, 0)
        self.assertIn("How we got here", out)

    def test_tables_code_and_nested_bullets_rejected(self):
        rc, _ = self.check(self.BRIEF_OK.replace("- You asked", "  - You asked"))
        self.assertNotEqual(rc, 0)
        rc, _ = self.check(self.BRIEF_OK + "\n| a | b |\n")
        self.assertNotEqual(rc, 0)
        rc, _ = self.check(self.BRIEF_OK + "\n```\nx\n```\n")
        self.assertNotEqual(rc, 0)

    def test_leading_sentence_must_be_single(self):
        rc, out = self.check(self.BRIEF_OK.replace("latest position is the March run.",
                                                   "latest position is the March run. We also did more."))
        self.assertNotEqual(rc, 0)
        self.assertIn("leading", out.lower())


class ArgTests(unittest.TestCase):
    def norm(self, arg):
        p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "session_history.py"),
                            "--normalize-args", arg], capture_output=True, text=True)
        return p.stdout.strip()

    def test_default_and_case_and_whitespace(self):
        self.assertEqual(self.norm(""), "brief")
        self.assertEqual(self.norm("  BRIEF "), "brief")
        self.assertEqual(self.norm("Full"), "full")

    def test_invalid_gives_usage_only(self):
        self.assertEqual(self.norm("verbose"), "Usage: /catch-me-up [brief|full]")
        self.assertEqual(self.norm("brief; rm -rf /"), "Usage: /catch-me-up [brief|full]")
        self.assertEqual(self.norm("$(id)"), "Usage: /catch-me-up [brief|full]")


if __name__ == "__main__":
    unittest.main()
