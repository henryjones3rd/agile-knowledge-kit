"""Flag pages whose last_reviewed date is older than their review_cycle_days.

Usage:
    python tools/check_freshness.py            # fail on stale pages
    python tools/check_freshness.py --warn-days 30   # also warn on pages due soon
    python tools/check_freshness.py --today 2027-06-01  # simulate a future date
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys

from docslib import all_pages, report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--warn-days", type=int, default=30)
    args = parser.parse_args()

    problems: list[str] = []
    pages = all_pages()
    for page in pages:
        reviewed = page.meta.get("last_reviewed")
        cycle = page.meta.get("review_cycle_days")
        if not isinstance(reviewed, dt.date) or not isinstance(cycle, int):
            continue  # check_frontmatter.py reports these
        due = reviewed + dt.timedelta(days=cycle)
        days_left = (due - args.today).days
        owner = page.meta.get("owner", "unknown owner")
        if days_left < 0:
            problems.append(f"{page.rel}: review overdue by {-days_left} days (owner: {owner})")
        elif days_left <= args.warn_days:
            print(f"WARN  {page.rel}: review due in {days_left} days (owner: {owner})")
    return report(problems, f"all {len(pages)} pages are within their review cycle")


if __name__ == "__main__":
    sys.exit(main())
