---
title: Contributing
description: The docs-as-code workflow for this kit, including required front matter and the automated checks every pull request must pass.
owner: Henry Jones III
last_reviewed: 2026-10-26
review_cycle_days: 365
tags: [docs-as-code, contributing]
---

# Contributing

Every page is Markdown in Git. Changes go through a pull request and must pass
automated checks before they publish.

## Required front matter

```yaml
---
title: Page title
description: One sentence. Used for search, llms.txt, and AI retrieval.
owner: Person accountable for accuracy
last_reviewed: YYYY-MM-DD
review_cycle_days: 180
tags: [topic]
---
```

## Checks run on every pull request

| Check | Command | Fails when |
| --- | --- | --- |
| Front matter | `python tools/check_frontmatter.py` | A required field is missing or malformed |
| Freshness | `python tools/check_freshness.py` | A page is past its review cycle |
| Links | `python tools/check_links.py` | An internal link or anchor is broken |
| Terminology | `python tools/check_terms.py` | A discouraged term appears |
| Prose style | Vale | A style rule is violated |
| Retrieval eval | `python tools/eval_retrieval.py` | An eval question doesn't retrieve its expected page |
| Build | `mkdocs build --strict` | MkDocs reports any warning |

Run them all locally with `make check`.

## Writing rules

- Lead with the point. First sentence answers the question.
- One idea per page. Link instead of repeating.
- Define a term the first time you use it.
- Prefer tables for comparisons and numbered lists for steps.
