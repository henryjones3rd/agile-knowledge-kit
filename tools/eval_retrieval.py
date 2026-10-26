"""Evaluate whether real questions retrieve the right page, and whether that page holds the answer.

Two failure types are reported separately because they need different fixes:
  - retrieval miss: the right page exists but doesn't rank (fix titles, descriptions, headings)
  - grounding gap: the expected page no longer contains the fact (content drifted or was deleted)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from docslib import ROOT
from search import Index


def main() -> int:
    spec = yaml.safe_load((ROOT / "evals" / "questions.yml").read_text(encoding="utf-8"))
    index = Index()
    by_rel = {p.rel: p for p in index.pages}
    top1 = top3 = 0
    problems: list[str] = []

    for item in spec["questions"]:
        ranked = [h.page.rel for h in index.search(item["q"], k=3)]
        hit1 = bool(ranked) and ranked[0] == item["page"]
        hit3 = item["page"] in ranked
        top1 += hit1
        top3 += hit3
        mark = "PASS" if hit1 else ("TOP3" if hit3 else "MISS")
        print(f"{mark}  {item['q']}\n      got: {ranked[:3]}")
        if not hit3:
            problems.append(f"retrieval miss: '{item['q']}' expected {item['page']}")
        page = by_rel.get(item["page"])
        text = re.sub(r"\s+", " ", page.body.lower()) if page else ""
        for fact in item.get("facts", []):
            if fact.lower() not in text:
                problems.append(f"grounding gap: {item['page']} no longer contains '{fact}'")

    total = len(spec["questions"])
    print(f"\nTop-1 accuracy: {top1}/{total} ({top1 / total:.0%})")
    print(f"Top-3 accuracy: {top3}/{total} ({top3 / total:.0%})")
    for problem in problems:
        print(f"FAIL  {problem}")
    grounding = [p for p in problems if p.startswith("grounding")]
    if top3 / total < spec["threshold_top3"] or grounding:
        print("Eval failed.")
        return 1
    print("OK    retrieval eval passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
