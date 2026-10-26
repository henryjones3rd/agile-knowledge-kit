"""Fail if any page is missing required front matter or has malformed values."""

from __future__ import annotations

import datetime as dt
import sys

from docslib import all_pages, report

REQUIRED = {
    "title": str,
    "description": str,
    "owner": str,
    "last_reviewed": dt.date,
    "review_cycle_days": int,
    "tags": list,
}
MAX_DESCRIPTION = 200


def main() -> int:
    problems: list[str] = []
    pages = all_pages()
    for page in pages:
        if page.error:
            problems.append(f"{page.rel}: {page.error}")
            continue
        for key, expected in REQUIRED.items():
            if key not in page.meta:
                problems.append(f"{page.rel}: missing '{key}'")
            elif not isinstance(page.meta[key], expected):
                problems.append(f"{page.rel}: '{key}' should be {expected.__name__}")
        desc = page.meta.get("description", "")
        if isinstance(desc, str) and len(desc) > MAX_DESCRIPTION:
            problems.append(f"{page.rel}: description over {MAX_DESCRIPTION} characters")
    return report(problems, f"front matter valid on {len(pages)} pages")


if __name__ == "__main__":
    sys.exit(main())
