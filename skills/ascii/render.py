#!/usr/bin/env python3
"""Render a word as bold ASCII block art, auto-fitted to terminal width.

Usage: python3 render.py [--width N] <word or phrase>

Each letter is rendered using its own character as the fill,
auto-scaled to fit the terminal, with vertical doubling for visual weight.
Supports A-Z, 0-9, common punctuation, and emoji (hearts, stars).
Wraps to multiple art-rows if the phrase is too wide for the terminal.
"""
import argparse
import shutil
import sys

import pyfiglet

FONT_NAME = "banner3"
MAX_HEIGHT = 7  # banner3 standard letter height
MAX_H_SCALE = 5
V_SCALE = 2
MIN_GAP = 2
OUTPUT_FILE = str(__import__("pathlib").Path(__file__).parent / "output.txt")

# Trailing punctuation that should attach closely to the preceding character
ATTACHED_PUNCT = set(",.!?:;")

# Emoji to renderable character mapping
EMOJI_MAP = {
    "\u2764\ufe0f": "\u2665",  # ❤️ -> ♥
    "\u2764": "\u2665",        # ❤  -> ♥
    "\u2665": "\u2665",        # ♥  -> ♥
    "\U0001f499": "\u2665",    # 💙 -> ♥
    "\U0001f49a": "\u2665",    # 💚 -> ♥
    "\U0001f49b": "\u2665",    # 💛 -> ♥
    "\U0001f49c": "\u2665",    # 💜 -> ♥
    "\U0001f5a4": "\u2665",    # 🖤 -> ♥
    "\U0001f497": "\u2665",    # 💗 -> ♥
    "\U0001f496": "\u2665",    # 💖 -> ♥
    "\U0001f495": "\u2665",    # 💕 -> ♥
    "\U0001f498": "\u2665",    # 💘 -> ♥
    "\u2b50": "\u2605",        # ⭐ -> ★
    "\U0001f31f": "\u2605",    # 🌟 -> ★
    "\u2728": "\u2605",        # ✨ -> ★
}

# Custom shape overrides (# = fill placeholder, replaced with the character)
FONT_OVERRIDES = {
    "Y": [
        "##     ##",
        " ##   ## ",
        "  ## ##  ",
        "   ###   ",
        "   ###   ",
        "   ###   ",
        "   ###   ",
    ],
    "\u2665": [  # ♥ heart
        " ##   ## ",
        "#### ####",
        "#########",
        "#########",
        " ####### ",
        "  #####  ",
        "   ###   ",
    ],
    "\u2605": [  # ★ star
        "    #    ",
        "   ###   ",
        "#########",
        " ####### ",
        "  #####  ",
        " ##   ## ",
        "##     ##",
    ],
}


def parse_input(text):
    """Parse input text, mapping emoji to renderable characters."""
    result = []
    i = 0
    while i < len(text):
        matched = False
        for emoji in sorted(EMOJI_MAP.keys(), key=len, reverse=True):
            if text[i:].startswith(emoji):
                result.append(EMOJI_MAP[emoji])
                i += len(emoji)
                matched = True
                break
        if not matched:
            c = text[i]
            if c.isalpha() or c.isdigit() or c in " !?.-+&,><:;/'\"()#@_=":
                result.append(c)
            i += 1
    return "".join(result)


def get_letter_rows(char):
    """Render a single character and return normalized rows."""
    if char in FONT_OVERRIDES:
        rows = [r.replace("#", char) for r in FONT_OVERRIDES[char]]
        return rows

    fig = pyfiglet.figlet_format(char, font=FONT_NAME)
    rows = fig.rstrip("\n").split("\n")

    # Check if all rows are blank (unsupported character)
    if not any(r.strip() for r in rows):
        return None

    # Keep exactly MAX_HEIGHT rows to preserve vertical positioning
    # (e.g., comma sits at bottom, hyphen sits in middle)
    rows = rows[:MAX_HEIGHT]
    while len(rows) < MAX_HEIGHT:
        rows.append("")

    max_w = max((len(r.rstrip()) for r in rows if r.strip()), default=1)
    rows = [r[:max_w].ljust(max_w) for r in rows]

    rows = [r.replace("#", char) for r in rows]
    return rows


def build_letter_data(text):
    """Build letter data list from parsed text."""
    letter_data = []
    for c in text:
        if c == " ":
            letter_data.append({"char": " ", "rows": None, "width": 0})
        else:
            rows = get_letter_rows(c)
            if rows is None:
                continue
            letter_data.append({"char": c, "rows": rows, "width": len(rows[0])})
    return letter_data


def split_into_words(letter_data):
    """Split letter_data into words (groups separated by space entries)."""
    words = []
    current = []
    for ld in letter_data:
        if ld["char"] == " ":
            if current:
                words.append(current)
                current = []
        else:
            current.append(ld)
    if current:
        words.append(current)
    return words


def word_width(word_letters, h_scale):
    """Calculate rendered width of a word (list of letter_data) at given scale."""
    if not word_letters:
        return 0
    total = sum(ld["width"] * h_scale for ld in word_letters)
    n_gaps = len(word_letters) - 1
    gap = max(MIN_GAP, h_scale)
    total += n_gaps * gap
    return total


def render_line(letter_data, max_width):
    """Render a single line of letter_data, auto-scaled to fit max_width."""
    if not letter_data:
        return ""

    n_letter_gaps = 0
    for i in range(1, len(letter_data)):
        if letter_data[i]["char"] != " " and letter_data[i - 1]["char"] != " ":
            n_letter_gaps += 1

    n_word_gaps = sum(1 for ld in letter_data if ld["char"] == " ")
    total_base_width = sum(ld["width"] for ld in letter_data if ld["char"] != " ")

    # Find optimal scale
    h_scale = 1
    for s in range(MAX_H_SCALE, 0, -1):
        scaled_w = total_base_width * s
        est_letter_gaps = n_letter_gaps * max(MIN_GAP, s)
        est_word_gaps = n_word_gaps * max(MIN_GAP, s * 3)
        if scaled_w + est_letter_gaps + est_word_gaps <= max_width:
            h_scale = s
            break

    # Calculate gap sizes
    scaled_width = total_base_width * h_scale
    remaining = max_width - scaled_width
    total_gap_units = n_letter_gaps + n_word_gaps * 2
    if total_gap_units > 0:
        unit_size = remaining // total_gap_units
        gap_size = max(MIN_GAP, unit_size)
        gap_size = min(gap_size, h_scale * 3 + 2)
        word_gap_size = max(gap_size * 2, h_scale * 3)
    else:
        gap_size = 0
        word_gap_size = 0

    # Scale and compose
    scaled_letters = []
    for ld in letter_data:
        if ld["char"] == " ":
            empty_row = " " * word_gap_size
            scaled_letters.append([empty_row] * (MAX_HEIGHT * V_SCALE))
            continue

        scaled_rows = []
        for row in ld["rows"]:
            s = "".join(c * h_scale for c in row)
            scaled_rows.append(s)

        max_w = max(len(r) for r in scaled_rows)
        scaled_rows = [r.ljust(max_w) for r in scaled_rows]

        expanded = []
        for row in scaled_rows:
            for _ in range(V_SCALE):
                expanded.append(row)
        scaled_letters.append(expanded)

    height = max(len(sl) for sl in scaled_letters)
    gap = " " * gap_size
    punct_gap = " " * max(1, gap_size // 3)  # minimal gap for attached punctuation
    output_lines = []

    for row_idx in range(height):
        parts = []
        for i, sl in enumerate(scaled_letters):
            if i > 0 and letter_data[i]["char"] != " " and letter_data[i - 1]["char"] != " ":
                if letter_data[i]["char"] in ATTACHED_PUNCT:
                    parts.append(punct_gap)
                else:
                    parts.append(gap)
            if row_idx < len(sl):
                parts.append(sl[row_idx])
            else:
                parts.append(" " * len(sl[0]))
        line = "".join(parts)
        output_lines.append(line.rstrip())

    return "\n".join(output_lines)


def render(text, max_width=80):
    """Render text as ASCII block art, word-wrapping if needed."""
    text = parse_input(text.upper())
    if not text:
        return None

    letter_data = build_letter_data(text)
    if not letter_data:
        return None

    words = split_into_words(letter_data)
    if not words:
        return None

    # Check if everything fits on one line at scale 1
    total_min = sum(word_width(w, 1) for w in words)
    word_gap_min = (len(words) - 1) * max(MIN_GAP, 3)  # minimum word gap
    fits_one_line = (total_min + word_gap_min) <= max_width

    if fits_one_line:
        return render_line(letter_data, max_width)

    # Word-wrap: greedily pack words into lines
    lines = []
    current_words = []
    current_width = 0

    for word in words:
        w = word_width(word, 1)
        if not current_words:
            # First word on line always fits
            current_words.append(word)
            current_width = w
        else:
            needed = current_width + max(MIN_GAP, 3) + w  # word gap + new word
            if needed <= max_width:
                current_words.append(word)
                current_width = needed
            else:
                # Flush current line
                line_data = []
                for j, cw in enumerate(current_words):
                    if j > 0:
                        line_data.append({"char": " ", "rows": None, "width": 0})
                    line_data.extend(cw)
                lines.append(line_data)
                current_words = [word]
                current_width = w

    # Flush last line
    if current_words:
        line_data = []
        for j, cw in enumerate(current_words):
            if j > 0:
                line_data.append({"char": " ", "rows": None, "width": 0})
            line_data.extend(cw)
        lines.append(line_data)

    # Render each line and join with a blank separator
    rendered = []
    for line_data in lines:
        rendered.append(render_line(line_data, max_width))

    return "\n\n".join(rendered)


def main():
    parser = argparse.ArgumentParser(description="Render ASCII block art")
    parser.add_argument("text", nargs="*", help="Text to render")
    parser.add_argument("--width", type=int, default=None, help="Terminal width")
    args = parser.parse_args()

    if not args.text:
        print("Usage: python3 render.py [--width N] <word or phrase>")
        sys.exit(1)

    text = " ".join(args.text)

    # Determine width: explicit flag > shutil detection > conservative default
    if args.width and args.width > 40:
        max_width = args.width
    else:
        try:
            max_width = shutil.get_terminal_size(fallback=(80, 24)).columns
        except Exception:
            max_width = 80

    max_width = max(40, min(300, max_width))

    result = render(text, max_width=max_width)
    if result:
        with open(OUTPUT_FILE, "w") as f:
            f.write(result + "\n")
        print(OUTPUT_FILE)
    else:
        print("Error: could not render the input text", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
