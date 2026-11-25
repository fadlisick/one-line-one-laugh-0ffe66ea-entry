#!/usr/bin/env python3
"""Publish one funny line for the One Line, One Laugh bounty.

The program takes a single joke line, checks it fits the competition gate
(1 to 200 characters, one line of text), and drops it into the output file
the scorer reads. Nothing else is written anywhere.
"""

import os

JOKE = "My voicemail says I will call you back, which is the longest-running lie I have ever told."

TOP = 200
BOTTOM = 1
FALLBACK_DIR = "/output"
FILE_NAME = "entry.txt"


class LinePublisher:
    """Holds the joke, checks it, and writes it to the output directory."""

    def __init__(self, joke):
        self.joke = joke

    def checked(self):
        line = self.joke.strip()
        if not line:
            raise ValueError("joke is empty")
        if not (BOTTOM <= len(line) <= TOP):
            raise ValueError("joke must be 1 to 200 characters")
        if "\n" in line or "\r" in line:
            raise ValueError("joke must be a single line")
        if not line.endswith("."):
            raise ValueError("joke must end with a full stop")
        return line

    def target(self):
        folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or FALLBACK_DIR
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, FILE_NAME)

    def publish(self):
        line = self.checked()
        path = self.target()
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(line)
        os.chmod(path, 0o644)
        with open(path, encoding="utf-8") as handle:
            stored = handle.read()
        if stored != line:
            raise ValueError("stored line does not match the joke")
        print(line)
        return 0


def run():
    return LinePublisher(JOKE).publish()


if __name__ == "__main__":
    raise SystemExit(run())
