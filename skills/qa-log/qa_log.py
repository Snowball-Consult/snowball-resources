#!/usr/bin/env python3
"""Q&A Learning Log: capture questions you ask and revisit them via spaced repetition.

One markdown card per question. Frontmatter holds the scheduling state
(SM-2-lite); the body holds the question, the answer, a one-line "why it
matters", and a review-history table.

Two skills drive this tool:
  - /learned  -> `add`            (capture a card from the conversation)
  - /quiz     -> `due` + `review` (run a review session, record grades)

See qa-log/README.md for the methodology and card format.
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path


# --- repo-root resolution (walk up to the .git/ dir) so this works
# regardless of cwd ---
def _repo_root():
    p = Path(__file__).resolve()
    for parent in [p, *p.parents]:
        if (parent / ".git").exists():
            return parent
    # Fallback: assume this file lives in <root>/qa-log/
    return p.parent.parent


ROOT = _repo_root()
QA_DIR = ROOT / "qa-log"
CARDS_DIR = QA_DIR / "cards"

# Order in which frontmatter keys are written (flat scalars only - keeps the
# parser trivial and the git diffs readable).
FM_ORDER = [
    "id", "created", "source", "tags", "type",
    "interval", "ease", "reps", "next_review", "last_reviewed", "last_grade",
]
NUMERIC_KEYS = {"interval", "ease", "reps"}

VALID_SOURCES = ["terminal", "claude.ai", "google", "other"]
VALID_TYPES = ["recall", "recognition"]

# Grade vocabulary. The /quiz skill grades free recall semantically and maps
# its judgement onto one of these. "again" = missed it, "hard" = partial,
# "good" = got it, "easy" = instant/confident.
GRADES = {"again": 0, "hard": 1, "good": 2, "easy": 3}


def _today():
    return date.today()


def _parse_date(s):
    s = (s or "").strip()
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%d").date()


def _slug(text, max_len=48):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:max_len].rstrip("-") or "card"


# --- frontmatter read / write ------------------------------------------------
def _read_card(path):
    """Return (frontmatter dict, body str) for a card file."""
    raw = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.DOTALL)
    if not m:
        raise ValueError(f"{path.name}: missing frontmatter")
    fm = {}
    for line in m.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    # normalise types
    fm["tags"] = [t.strip() for t in fm.get("tags", "").split(",") if t.strip()]
    for k in NUMERIC_KEYS:
        if k in fm and fm[k] != "":
            fm[k] = float(fm[k]) if k == "ease" else int(float(fm[k]))
    return fm, m.group(2)


def _render_frontmatter(fm):
    lines = ["---"]
    for key in FM_ORDER:
        val = fm.get(key, "")
        if key == "tags":
            val = ", ".join(val) if isinstance(val, list) else (val or "")
        elif key == "ease" and val != "":
            val = f"{float(val):.2f}"
        elif val is None:
            val = ""
        lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def _write_card(path, fm, body):
    path.write_text(_render_frontmatter(fm) + "\n" + body)


def _all_cards():
    out = []
    for path in sorted(CARDS_DIR.glob("qa-*.md")):
        try:
            fm, body = _read_card(path)
            out.append((path, fm, body))
        except ValueError as e:
            print(f"qa_log: skipping {e}", file=sys.stderr)
    return out


def _next_id():
    max_num = 0
    for path in CARDS_DIR.glob("qa-*.md"):
        m = re.match(r"qa-(\d+)", path.name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"qa-{max_num + 1:03d}"


# --- spaced-repetition scheduling (SM-2-lite) --------------------------------
def _schedule(interval, ease, reps, grade):
    """Return (new_interval_days, new_ease, new_reps) given a grade 0..3.

    grade: 0 again (missed), 1 hard (partial), 2 good (got it), 3 easy.
    A miss resets the card to a 1-day interval and drops ease. Otherwise the
    interval grows (1 -> 3 -> interval*ease...), with ease nudged by quality.
    """
    interval = interval or 0
    ease = ease or 2.5
    reps = reps or 0

    if grade == 0:  # again
        return 1, round(max(1.3, ease - 0.20), 2), 0

    reps += 1
    if reps == 1:
        new_interval = 1
    elif reps == 2:
        new_interval = 3 if grade >= 2 else 2
    else:
        mult = {1: 1.2, 2: ease, 3: ease + 0.15}[grade]
        new_interval = max(1, round(interval * mult))

    if grade == 1:      # hard
        ease = max(1.3, ease - 0.15)
    elif grade == 3:    # easy
        ease = ease + 0.10
    # grade == 2 (good) leaves ease unchanged
    return new_interval, round(ease, 2), reps


# --- commands ----------------------------------------------------------------
CARD_BODY_TEMPLATE = """
## Question

{question}

## Answer

{answer}

**Why it matters:** {why}

## Review history

| Date | Grade | Interval (d) | Next review |
|------|-------|--------------|-------------|
"""


def cmd_add(args):
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    today = _today().isoformat()
    cid = _next_id()
    source = args.source if args.source in VALID_SOURCES else "terminal"
    ctype = args.type if args.type in VALID_TYPES else "recall"
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]

    fm = {
        "id": cid,
        "created": today,
        "source": source,
        "tags": tags,
        "type": ctype,
        "interval": 0,
        "ease": 2.5,
        "reps": 0,
        "next_review": today,   # new cards are due immediately
        "last_reviewed": "",
        "last_grade": "",
    }
    body = CARD_BODY_TEMPLATE.format(
        question=args.question.strip(),
        answer=args.answer.strip(),
        why=(args.why or "").strip(),
    )
    path = CARDS_DIR / f"{cid}_{_slug(args.question)}.md"
    _write_card(path, fm, body)

    result = {"id": cid, "path": str(path.relative_to(ROOT)), "next_review": today}
    if args.json:
        print(json.dumps(result))
    else:
        print(f"Captured {cid} -> {result['path']}")
    return 0


def _card_summary(fm, body, include_answer=False):
    q = _extract_section(body, "Question")
    out = {
        "id": fm["id"],
        "question": q,
        "type": fm.get("type", "recall"),
        "tags": fm.get("tags", []),
        "next_review": fm.get("next_review", ""),
        "reps": fm.get("reps", 0),
    }
    if include_answer:
        out["answer"] = _extract_section(body, "Answer")
        out["why"] = _extract_why(body)
    return out


def _extract_section(body, name):
    m = re.search(rf"## {re.escape(name)}\n+(.*?)(?:\n## |\n\*\*Why|\Z)", body, re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_why(body):
    m = re.search(r"\*\*Why it matters:\*\*\s*(.*)", body)
    return m.group(1).strip() if m else ""


def cmd_due(args):
    today = _today()
    rows = []
    for path, fm, body in _all_cards():
        nr = _parse_date(fm.get("next_review"))
        is_due = nr is not None and nr <= today
        is_new = (fm.get("reps", 0) == 0)
        created = _parse_date(fm.get("created"))
        is_recent = (
            args.recent and created is not None
            and created >= today - timedelta(days=args.recent)
        )
        if is_due or (args.include_new and is_new) or is_recent:
            rows.append((nr or today, fm, body))
    # earliest-due first, then by id
    rows.sort(key=lambda r: (r[0], r[1]["id"]))
    if args.limit:
        rows = rows[: args.limit]
    cards = [_card_summary(fm, body, include_answer=True) for _, fm, body in rows]
    if args.json:
        print(json.dumps({"count": len(cards), "cards": cards}))
    else:
        if not cards:
            print("Nothing due. Inbox zero on recall.")
            return 0
        print(f"{len(cards)} card(s) due:")
        for c in cards:
            tag = f" [{', '.join(c['tags'])}]" if c["tags"] else ""
            print(f"  {c['id']}  {c['question']}{tag}")
    return 0


def cmd_review(args):
    grade_name = args.grade.lower()
    if grade_name not in GRADES:
        print(f"qa_log: unknown grade '{args.grade}' (use {'/'.join(GRADES)})", file=sys.stderr)
        return 2
    grade = GRADES[grade_name]

    matches = list(CARDS_DIR.glob(f"{args.id}_*.md")) or list(CARDS_DIR.glob(f"{args.id}.md"))
    if not matches:
        print(f"qa_log: no card {args.id}", file=sys.stderr)
        return 1
    path = matches[0]
    fm, body = _read_card(path)

    interval, ease, reps = _schedule(
        fm.get("interval", 0), fm.get("ease", 2.5), fm.get("reps", 0), grade
    )
    today = _today()
    next_review = today + timedelta(days=interval)

    fm["interval"] = interval
    fm["ease"] = ease
    fm["reps"] = reps
    fm["next_review"] = next_review.isoformat()
    fm["last_reviewed"] = today.isoformat()
    fm["last_grade"] = grade_name

    # append a row to the Review history table
    row = f"| {today.isoformat()} | {grade_name} | {interval} | {next_review.isoformat()} |\n"
    if "## Review history" in body and "|------|" in body:
        body = body.rstrip() + "\n" + row
    else:
        body = body.rstrip() + "\n\n## Review history\n\n| Date | Grade | Interval (d) | Next review |\n|------|-------|--------------|-------------|\n" + row

    _write_card(path, fm, body)
    result = {"id": fm["id"], "grade": grade_name, "interval": interval,
              "ease": ease, "next_review": next_review.isoformat()}
    if args.json:
        print(json.dumps(result))
    else:
        print(f"{fm['id']}: {grade_name} -> next review {next_review.isoformat()} (interval {interval}d)")
    return 0


def cmd_list(args):
    cards = _all_cards()
    if args.json:
        print(json.dumps([_card_summary(fm, body) for _, fm, body in cards]))
        return 0
    if not cards:
        print("No cards yet. Use /learned to capture one.")
        return 0
    for _, fm, body in cards:
        q = _extract_section(body, "Question")
        q = (q[:70] + "...") if len(q) > 73 else q
        print(f"  {fm['id']}  due {fm.get('next_review','?'):<12} {q}")
    return 0


def cmd_stats(args):
    today = _today()
    cards = _all_cards()
    total = len(cards)
    new = sum(1 for _, fm, _ in cards if fm.get("reps", 0) == 0)
    due = sum(1 for _, fm, _ in cards
              if (_parse_date(fm.get("next_review")) or today) <= today)
    reviewed = total - new
    eases = [fm.get("ease", 2.5) for _, fm, _ in cards if fm.get("reps", 0) > 0]
    avg_ease = round(sum(eases) / len(eases), 2) if eases else None
    longest = max((fm.get("interval", 0) for _, fm, _ in cards), default=0)
    stats = {"total": total, "new": new, "reviewed": reviewed,
             "due_today": due, "avg_ease": avg_ease, "longest_interval_d": longest}
    if args.json:
        print(json.dumps(stats))
    else:
        print(f"cards: {total}  |  new: {new}  |  reviewed: {reviewed}  |  due today: {due}")
        if avg_ease:
            print(f"avg ease: {avg_ease}  |  longest interval: {longest}d")
    return 0


def cmd_nudge(args):
    """SessionStart hook: a one-line reminder when cards are due (/quiz) or
    capture has gone stale (/learned). Emits the SessionStart hook JSON shape
    so the message surfaces at session start. Stays silent when there
    is nothing to nudge, and never fails the session - any error prints nothing
    and exits 0.
    """
    try:
        if not CARDS_DIR.exists():
            return 0
        today = _today()
        cards = _all_cards()
        if not cards:  # empty store stays quiet until you start using it
            return 0

        due = sum(1 for _, fm, _ in cards
                  if (_parse_date(fm.get("next_review")) or today) <= today)
        created = [d for d in (_parse_date(fm.get("created")) for _, fm, _ in cards) if d]
        stale_days = (today - max(created)).days if created else 0

        parts = []
        if due > 0:
            parts.append(f"{due} card{'s' if due != 1 else ''} due - /quiz")
        if stale_days >= 7:
            parts.append(f"no new card in {stale_days}d - /learned to capture")
        if not parts:
            return 0

        msg = "📚 Q&A log: " + "; ".join(parts)
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart", "additionalContext": msg}}))
        return 0
    except Exception:
        return 0


def main():
    p = argparse.ArgumentParser(description="Q&A learning log + spaced repetition")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("add", help="capture a new card")
    pa.add_argument("--question", required=True)
    pa.add_argument("--answer", required=True)
    pa.add_argument("--why", default="")
    pa.add_argument("--source", default="terminal", choices=VALID_SOURCES)
    pa.add_argument("--tags", default="", help="comma-separated")
    pa.add_argument("--type", default="recall", choices=VALID_TYPES)
    pa.add_argument("--json", action="store_true")
    pa.set_defaults(func=cmd_add)

    pd = sub.add_parser("due", help="list cards due for review")
    pd.add_argument("--limit", type=int, default=0)
    pd.add_argument("--recent", type=int, default=0,
                    help="also include cards created in the last N days")
    pd.add_argument("--include-new", action="store_true",
                    help="include never-reviewed cards")
    pd.add_argument("--json", action="store_true")
    pd.set_defaults(func=cmd_due)

    pr = sub.add_parser("review", help="record a grade and reschedule")
    pr.add_argument("id", help="card id, e.g. qa-001")
    pr.add_argument("--grade", required=True, help="again|hard|good|easy")
    pr.add_argument("--json", action="store_true")
    pr.set_defaults(func=cmd_review)

    pl = sub.add_parser("list", help="list all cards")
    pl.add_argument("--json", action="store_true")
    pl.set_defaults(func=cmd_list)

    ps = sub.add_parser("stats", help="summary counts")
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(func=cmd_stats)

    pn = sub.add_parser("nudge", help="SessionStart reminder (JSON for the hook)")
    pn.set_defaults(func=cmd_nudge)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
