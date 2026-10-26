"""Shared helpers for the docs quality tools: page discovery and front matter parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class Page:
    path: Path
    meta: dict = field(default_factory=dict)
    body: str = ""
    error: str | None = None

    @property
    def rel(self) -> str:
        return self.path.relative_to(DOCS).as_posix()


def load_page(path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if not match:
        return Page(path, body=text, error="missing front matter block")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return Page(path, body=text[match.end():], error=f"invalid YAML: {exc}")
    return Page(path, meta=meta, body=text[match.end():])


def all_pages() -> list[Page]:
    return [load_page(p) for p in sorted(DOCS.rglob("*.md"))]


def strip_code(markdown: str) -> str:
    """Remove fenced and inline code so checks ignore examples."""
    markdown = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    return re.sub(r"`[^`\n]+`", "", markdown)


def report(problems: list[str], ok_message: str) -> int:
    for problem in problems:
        print(f"FAIL  {problem}")
    if problems:
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print(f"OK    {ok_message}")
    return 0
