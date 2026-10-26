"""Validate internal Markdown links and heading anchors across the docs.

External links are checked only with --external, since network calls make CI flaky.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

from docslib import DOCS, all_pages, report, strip_code

LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def slugify(heading: str) -> str:
    """Match MkDocs' default toc slugs."""
    slug = re.sub(r"[^\w\s-]", "", heading.lower())
    return re.sub(r"[\s]+", "-", slug).strip("-")


def anchors_for(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        text = strip_code(path.read_text(encoding="utf-8"))
        cache[path] = {slugify(h) for h in HEADING.findall(text)}
    return cache[path]


def check_external(url: str) -> str | None:
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "docs-link-check"})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return None if response.status < 400 else f"HTTP {response.status}"
    except Exception as exc:  # noqa: BLE001 - report any failure
        return str(exc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external", action="store_true", help="also check http(s) links")
    args = parser.parse_args()

    problems: list[str] = []
    cache: dict[Path, set[str]] = {}
    count = 0
    for page in all_pages():
        for target in LINK.findall(strip_code(page.body)):
            count += 1
            if target.startswith(("http://", "https://")):
                if args.external and (error := check_external(target)):
                    problems.append(f"{page.rel}: {target} -> {error}")
                continue
            if target.startswith("mailto:"):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (page.path.parent / file_part).resolve() if file_part else page.path
            if not dest.exists():
                problems.append(f"{page.rel}: broken link -> {target}")
                continue
            if not str(dest).startswith(str(DOCS)):
                problems.append(f"{page.rel}: link escapes docs/ -> {target}")
            elif anchor and anchor not in anchors_for(dest, cache):
                problems.append(f"{page.rel}: missing anchor #{anchor} in {file_part or page.rel}")
    return report(problems, f"{count} links checked, all resolve")


if __name__ == "__main__":
    sys.exit(main())
