#!/usr/bin/env python3
"""Check that generated WeChat HTML preserves source visible text.

For strict content-preserving layout, the agent may change containers,
spacing, quote blocks, and emphasis, but must not add/rewrite visible copy.
This script compares normalized visible body text from a source Markdown file
with normalized visible text extracted from the generated clean HTML.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import re
import sys


FRONTMATTER_BOUNDARY = re.compile(r"^\s*---\s*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"script", "style", "head", "title"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "head", "title"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = data.strip()
        if text:
            self.parts.append(text)


def strip_frontmatter(lines: list[str]) -> list[str]:
    if not lines or not FRONTMATTER_BOUNDARY.match(lines[0]):
        return lines
    for index in range(1, len(lines)):
        if FRONTMATTER_BOUNDARY.match(lines[index]):
            return lines[index + 1 :]
    return lines


def markdown_visible_text(markdown: str, keep_h1: bool = False) -> str:
    markdown = HTML_COMMENT.sub("", markdown)
    lines = strip_frontmatter(markdown.splitlines())
    output: list[str] = []
    first_h1_skipped = False
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            if not keep_h1 and not first_h1_skipped:
                first_h1_skipped = True
                continue
            line = line[2:].strip()
        else:
            line = re.sub(r"^#{2,6}\s+", "", line)
        if re.fullmatch(r"!\[[^\]]*\]\([^)]+\)", line):
            continue
        line = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"^>\s*", "", line)
        line = re.sub(r"^\s*[-*+]\s+", "", line)
        line = re.sub(r"^\s*\d+[.)]\s+", "", line)
        line = line.replace("**", "").replace("__", "")
        line = line.replace("`", "")
        if line:
            output.append(line)
    return "\n".join(output)


def html_visible_text(html: str) -> str:
    parser = TextParser()
    parser.feed(html)
    return "\n".join(parser.parts)


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_md", help="Source Markdown file")
    parser.add_argument("generated_html", help="Generated clean HTML file")
    parser.add_argument(
        "--keep-h1",
        action="store_true",
        help="Include the first H1 in source visible text comparison",
    )
    args = parser.parse_args()

    with open(args.source_md, encoding="utf-8", errors="replace") as handle:
        source = markdown_visible_text(handle.read(), keep_h1=args.keep_h1)
    with open(args.generated_html, encoding="utf-8", errors="replace") as handle:
        generated = html_visible_text(handle.read())

    source_norm = normalize(source)
    generated_norm = normalize(generated)
    print(f"source visible chars: {len(source_norm)}")
    print(f"html visible chars:   {len(generated_norm)}")
    if source_norm == generated_norm:
        print("OK: visible text matches")
        return 0

    print("ERROR: visible text differs", file=sys.stderr)
    print("\n--- source preview ---", file=sys.stderr)
    print(source[:500], file=sys.stderr)
    print("\n--- html preview ---", file=sys.stderr)
    print(generated[:500], file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
