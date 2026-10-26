"""Generate llms.txt (an index for AI assistants) and llms-full.txt (all content) from the docs.

Follows the llms.txt proposal: https://llmstxt.org/
    python tools/build_llms_txt.py          # write docs/llms.txt and docs/llms-full.txt
    python tools/build_llms_txt.py --check  # fail if the committed files are out of date (CI)
"""

from __future__ import annotations

import argparse
import sys

import yaml

from docslib import DOCS, ROOT, load_page

LOADER = yaml.SafeLoader
# mkdocs.yml uses a python tag for mermaid fences; ignore it when reading nav.
LOADER.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)


def nav_entries(nav, section: str = "Overview"):
    for item in nav:
        for label, value in item.items():
            if isinstance(value, list):
                yield from nav_entries(value, label)
            else:
                yield section, label, value


def build() -> tuple[str, str]:
    config = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=LOADER)
    base = (config.get("site_url") or "").rstrip("/")
    lines = [f"# {config['site_name']}", "", f"> {config['site_description']}", ""]
    full = [f"# {config['site_name']}", ""]
    current = None
    for section, label, rel in nav_entries(config["nav"]):
        page = load_page(DOCS / rel)
        url_path = rel[:-3] + "/" if rel != "index.md" else ""
        url = f"{base}/{url_path}" if base else url_path or "./"
        if section != current:
            lines += ["", f"## {section}", ""] if current else [f"## {section}", ""]
            current = section
        lines.append(f"- [{label}]({url}): {page.meta.get('description', '')}")
        full += [f"\n---\nsource: {rel}\ntitle: {page.meta.get('title', label)}\n---\n", page.body.strip()]
    return "\n".join(lines) + "\n", "\n".join(full) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = dict(zip(("llms.txt", "llms-full.txt"), build()))
    stale = []
    for name, content in outputs.items():
        path = DOCS / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote docs/{name} ({len(content):,} characters)")
    if stale:
        print(f"FAIL  out of date: {', '.join(stale)}. Run: python tools/build_llms_txt.py")
        return 1
    if args.check:
        print("OK    llms.txt files are current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
