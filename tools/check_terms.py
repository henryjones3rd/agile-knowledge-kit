"""Catch terminology drift: discouraged terms and abbreviations used before they are defined."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from docslib import all_pages, report, strip_code

TERMS = yaml.safe_load((Path(__file__).parent / "terms.yml").read_text(encoding="utf-8"))
# Quoted examples ("1 point = 1 day") are allowed so pages can show what NOT to say.
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”')
# Headings are titles; the definition is expected in the body text below them.
HEADINGS = re.compile(r"^#{1,6} .*$", re.MULTILINE)


def main() -> int:
    problems: list[str] = []
    rules = [(re.compile(r["pattern"], re.IGNORECASE), r) for r in TERMS["discouraged"]]
    pages = all_pages()
    for page in pages:
        prose = QUOTED.sub("", strip_code(page.body))
        for number, line in enumerate(prose.splitlines(), start=1):
            for regex, rule in rules:
                if match := regex.search(line):
                    problems.append(
                        f"{page.rel}:{number}: '{match.group(0)}' -> use {rule['use']} ({rule['why']})"
                    )
        for abbr, full in TERMS["defined_terms"].items():
            body = HEADINGS.sub("", prose)
            abbr_at = re.search(rf"\b{abbr}\b", body)
            if not abbr_at:
                continue
            full_at = re.search(re.escape(full), body, re.IGNORECASE)
            if not full_at or full_at.start() > abbr_at.start():
                problems.append(f"{page.rel}: '{abbr}' used before '{full}' is spelled out")
    return report(problems, f"terminology consistent across {len(pages)} pages")


if __name__ == "__main__":
    sys.exit(main())
