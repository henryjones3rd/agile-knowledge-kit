"""MCP server that lets AI agents search and read the knowledge kit.

Run locally:   python mcp_server/server.py
Claude Desktop config (claude_desktop_config.json):
  {"mcpServers": {"agile-kit": {"command": "python", "args": ["/path/to/agile-knowledge-kit/mcp_server/server.py"]}}}
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

try:  # MCP Python SDK 2.x
    from mcp.server.mcpserver import MCPServer as Server
except ImportError:  # MCP Python SDK 1.x
    from mcp.server.fastmcp import FastMCP as Server

from docslib import DOCS  # noqa: E402
from search import Index  # noqa: E402

mcp = Server("agile-knowledge-kit")
index = Index()


@mcp.tool()
def search_docs(query: str, limit: int = 3) -> list[dict]:
    """Search the agile delivery playbooks. Returns matching pages with path, title, and description."""
    return [
        {
            "path": hit.page.rel,
            "title": hit.page.meta.get("title"),
            "description": hit.page.meta.get("description"),
            "score": round(hit.score, 3),
        }
        for hit in index.search(query, k=max(1, min(limit, 10)))
    ]


@mcp.tool()
def get_page(path: str) -> str:
    """Return the full Markdown of one page, by the path returned from search_docs."""
    target = (DOCS / path).resolve()
    if not str(target).startswith(str(DOCS)) or target.suffix != ".md" or not target.exists():
        return f"No page at '{path}'. Use search_docs to find valid paths."
    return target.read_text(encoding="utf-8")


@mcp.resource("docs://llms.txt")
def llms_index() -> str:
    """The llms.txt index of every page."""
    return (DOCS / "llms.txt").read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run()
