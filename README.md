# Agile Delivery Knowledge Kit

Field-tested playbooks, decision guides, and templates for distributed
engineering teams, built and published as **docs-as-code** with automated
quality checks and AI-ready packaging.

**Live site:** `https://<your-github-username>.github.io/agile-knowledge-kit/`

## What's inside

| Path | What it is |
| --- | --- |
| `docs/` | Markdown content with required front matter (owner, review cycle, tags) |
| `tools/check_frontmatter.py` | Validates required metadata on every page |
| `tools/check_freshness.py` | Flags pages past their review cycle, naming the owner |
| `tools/check_links.py` | Validates internal links **and heading anchors** (`--external` for URLs) |
| `tools/check_terms.py` + `terms.yml` | Catches terminology drift and undefined abbreviations |
| `tools/build_llms_txt.py` | Generates [`llms.txt`](https://llmstxt.org/) and `llms-full.txt` for AI assistants |
| `tools/search.py` | Dependency-free TF-IDF retrieval shared by the eval and the MCP server |
| `evals/questions.yml` + `tools/eval_retrieval.py` | Retrieval eval: real questions → expected page → required facts |
| `mcp_server/server.py` | MCP server exposing `search_docs`, `get_page`, and the `llms.txt` resource |
| `.vale.ini`, `.vale/` | Prose linting with a house style and vocabulary |
| `.github/workflows/docs.yml` | CI: every check on each PR, weekly freshness run, auto-deploy to GitHub Pages |

## Design choices

- **Fix the class of problem, not the instance.** Each check exists because a
  specific failure kept recurring: stale pages, broken anchors, drifting terms.
- **The eval separates two failures.** A *retrieval miss* means the right page
  exists but doesn't rank (fix titles and descriptions). A *grounding gap*
  means the page no longer holds the fact (content drifted). They need
  different fixes, so they're reported differently.
- **One retriever, two uses.** The eval measures exactly what the MCP server
  serves, so passing the eval means agents get the right page.
- **Freshness runs on a schedule**, not only on commits, because docs go stale
  when nobody touches them.

## Quick start

```bash
python -m pip install -r requirements.txt
make check        # every check plus a strict build
make serve        # preview at http://127.0.0.1:8000
```

### Try the MCP server

```bash
python -m pip install -r mcp_server/requirements.txt
```

Add to your MCP client config (for example `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "agile-kit": {
      "command": "python",
      "args": ["/absolute/path/to/agile-knowledge-kit/mcp_server/server.py"]
    }
  }
}
```

Then ask: *"Using agile-kit, how should we plan capacity when part of the team
has holidays?"*

## Results (current)

- 12 pages, 25 internal links, 0 broken
- Retrieval eval: 14/14 top-1 (100%)
- Vale: 0 errors, 0 warnings

## Author

Henry Jones III · Henry.Jones3rd@gmail.com
