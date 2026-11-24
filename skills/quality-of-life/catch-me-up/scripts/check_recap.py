#!/usr/bin/env python3
"""Validate a drafted /catch-me-up recap against the output contract.

Usage:  python3 check_recap.py --mode brief|full < draft.md
Prints "OK (<n> words)" and exits 0, or one FAIL line per violation and exits 1.
Standard library only. Reads stdin only; writes nothing.
"""
import argparse
import re
import sys

LIMITS = {"brief": 200, "full": 300}
HEADINGS = {
    "brief": ["### Started", "### How we got here", "### Status / left off"],
    "full": ["### How this started", "### How we got here", "### Where we stand", "### Where we left off"],
}
META = {
    "brief": re.compile(r"^Compacted: (Yes|No|Unknown) · History: (Full|Partial|Summary-only) · Basis: conversation$"),
    "full": re.compile(r"^Compacted: (Yes|No|Unknown) · History: (Full|Partial|Summary-only) · Checks: (Verified|Partial|Unavailable|Not applicable)$"),
}
WORD = re.compile(r"[A-Za-z0-9]")


def count_words(text):
    return sum(1 for tok in text.split() if WORD.search(tok))


def check(text, mode):
    fails = []
    lines = text.strip("\n").split("\n")
    nonblank = [(i, l) for i, l in enumerate(lines) if l.strip()]
    if len(nonblank) < 3:
        return ["FAIL: recap too short to validate"]
    # leading sentence
    i0, lead = nonblank[0]
    if lead.startswith("#") or lead.startswith("-") or lead.startswith("Compacted:"):
        fails.append("FAIL: first line must be the leading sentence (no heading, bullet, or metadata first)")
    if re.search(r"[.!?]\s+[A-Z(\"']", lead.strip()):
        fails.append("FAIL: leading line must be exactly one sentence")
    if not re.search(r"[.!?]$", lead.strip()):
        fails.append("FAIL: leading sentence must end with a period")
    # metadata line
    i1, meta = nonblank[1]
    if not META[mode].match(meta.strip()):
        fails.append(f"FAIL: second line must be the {mode} metadata line, got: {meta.strip()[:80]}")
    if i1 != i0 + 2 or lines[i0 + 1].strip():
        fails.append("FAIL: one blank line between the leading sentence and the metadata line")
    # headings, order
    heads = [l.strip() for l in lines if l.startswith("### ")]
    if heads != HEADINGS[mode]:
        fails.append(f"FAIL: headings must be exactly {HEADINGS[mode]} in order; got {heads}")
    # sections
    section, sections = None, {}
    for l in lines:
        if l.startswith("### "):
            section = l.strip()
            sections[section] = []
        elif section:
            sections[section].append(l)
    for h, body in sections.items():
        for l in body:
            if not l.strip():
                continue
            if l.startswith(" ") or l.startswith("\t"):
                fails.append(f"FAIL: nested bullet or indented line under {h}: {l.strip()[:60]}")
            elif not l.startswith("- "):
                if h == "### How we got here":
                    fails.append(f"FAIL: '{h}' must contain bullet points only: {l.strip()[:60]}")
                elif h in HEADINGS[mode]:
                    fails.append(f"FAIL: non-bullet line under {h}: {l.strip()[:60]}")
    # global prohibitions
    if any(l.strip().startswith("|") for l in lines):
        fails.append("FAIL: tables are not allowed")
    if any(l.strip().startswith("```") for l in lines):
        fails.append("FAIL: code blocks are not allowed")
    if "—" in text:
        fails.append("FAIL: em dash found")
    n = count_words(text)
    if n > LIMITS[mode]:
        fails.append(f"FAIL: {n} words exceeds the {mode} limit of {LIMITS[mode]} words")
    return fails, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("brief", "full"), required=True)
    a = ap.parse_args()
    text = sys.stdin.read()
    result = check(text, a.mode)
    if isinstance(result, list):
        print("\n".join(result))
        return 1
    fails, n = result
    if fails:
        print("\n".join(fails))
        print(f"({n} words)")
        return 1
    print(f"OK ({n} words, limit {LIMITS[a.mode]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
