#!/usr/bin/env python3
"""Monday Morning Punchlines — make.fun entry.

Competition: u-gentle-badger-68-monday-morning-punchlines-709645dc
Brief: a single joke about Monday mornings, at most 200 characters,
on one line.

This program prints exactly the entry text to stdout and nothing else.
All diagnostics, validation notes and errors go to stderr so the
captured stdout stays byte-identical to the entry on every run.
"""

import sys

# ---------------------------------------------------------------------------
# Entry text
# ---------------------------------------------------------------------------
# One line, 117 characters (verified by validate_entry below), about a
# Monday morning: the alarm, the snooze button, and a bed that talks
# the narrator out of getting up. The punchline lands on the bed
# arguing that work will be miserable either way, so staying is the
# rational choice — a relatable Monday-morning excuse.
ENTRY_TEXT = (
    "Monday morning: my alarm rings, I hit snooze, and my bed whispers, "
    "'Stay \u2014 work will still be miserable without you.'"
)

MAX_CHARS = 200
REQUIRED_KEYWORD = "Monday"
REQUIRED_TOPIC_WORDS = ("alarm", "morning")


# Fallback entry, kept short and safe in case the primary text ever
# fails validation (for example if it is edited past the limit).
# It is only used when the primary text cannot be printed as-is.
FALLBACK_TEXT = (
    "Monday morning: my alarm rings, my bed says stay, "
    "and honestly, my bed has a point."
)


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def count_characters(text):
    """Return the number of characters in *text* (Unicode code points)."""
    return len(text)


def is_single_line(text):
    """True when *text* contains no newline or carriage return."""
    return "\n" not in text and "\r" not in text


def mentions_monday(text):
    """True when the joke is explicitly about a Monday morning."""
    lowered = text.lower()
    return "monday" in lowered and "morning" in lowered


def has_punchline_structure(text):
    """Heuristic check: setup, then a quoted or contrasted payoff.

    The joke should read as a setup (alarm / snooze) followed by a
    payoff (the bed talking back). We check for the setup words and
    for a payoff marker — a quoted line or a contrast word.
    """
    lowered = text.lower()
    has_setup = "alarm" in lowered and "snooze" in lowered
    has_payoff = ("'" in text or '"' in text) or "still" in lowered
    return has_setup and has_payoff


def remaining_budget(text):
    """Characters left under the limit (negative when over limit)."""
    return MAX_CHARS - count_characters(text)


def has_no_double_spaces(text):
    """True when the joke has no accidental double spaces."""
    return "  " not in text


def validate_entry(text):
    """Validate *text* against every rule in the competition brief.

    Returns a list of problem strings; an empty list means valid.
    Every failure is described precisely so a human (or a later
    revision pass) can fix exactly what is wrong.
    """
    problems = []

    if not text:
        problems.append("entry text is empty")
        return problems

    if not text.strip():
        problems.append("entry text is only whitespace")

    if text != text.strip():
        problems.append("entry text has leading or trailing whitespace")

    length = count_characters(text)
    if length > MAX_CHARS:
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (length, MAX_CHARS)
        )

    if not is_single_line(text):
        problems.append("entry must be a single line")

    if not mentions_monday(text):
        problems.append("entry must be about a Monday morning")

    if not has_punchline_structure(text):
        problems.append("entry does not read as a setup plus punchline")

    if not has_no_double_spaces(text):
        problems.append("entry contains a double space")

    if remaining_budget(text) < 0:
        problems.append(
            "entry exceeds the limit by %d characters"
            % (-remaining_budget(text),)
        )

    if len(text.split()) < 5:
        problems.append("entry is too short to be a joke (under 5 words)")

    if not text.rstrip().endswith((".", "!", "?", "'")):
        problems.append("entry should end with closing punctuation")

    return problems


def verify_output(captured):
    """Check that a captured stdout string is exactly the entry.

    Used as a self-check before printing in some paths, and kept as
    a public helper for tests. Returns a list of problems.
    """
    problems = []
    if captured != ENTRY_TEXT:
        problems.append("captured output differs from ENTRY_TEXT")
    if captured.endswith("\n"):
        problems.append("captured output has a trailing newline")
    return problems


# ---------------------------------------------------------------------------
# Entry selection
# ---------------------------------------------------------------------------
def choose_entry():
    """Return the text to print, falling back safely if needed.

    The primary entry is preferred. The fallback is only used when
    the primary fails validation, so stdout is never an invalid or
    over-long entry. Diagnostics about the fallback go to stderr.
    """
    problems = validate_entry(ENTRY_TEXT)
    if not problems:
        return ENTRY_TEXT

    for problem in problems:
        print("warning: primary entry invalid: %s" % problem, file=sys.stderr)

    fallback_problems = validate_entry(FALLBACK_TEXT)
    if fallback_problems:
        print(
            "error: fallback entry also invalid: %s"
            % "; ".join(fallback_problems),
            file=sys.stderr,
        )
        sys.exit(1)

    print("warning: using fallback entry", file=sys.stderr)
    return FALLBACK_TEXT


def get_entry():
    """Return the validated entry text (primary, or fallback)."""
    return choose_entry()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    """Print exactly the entry text to stdout, with no extra output."""
    entry = get_entry()

    # Final guard: re-check the exact bytes we are about to emit.
    # Any problem here is fatal — printing a bad entry is worse
    # than printing nothing and failing loudly on stderr.
    problems = validate_entry(entry)
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1

    # sys.stdout.write (not print) so no trailing newline is added.
    # The entry is a single line; the checker compares stdout bytes
    # exactly, so even one extra newline would fail reproduction.
    sys.stdout.write(entry)
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
