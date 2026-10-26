"""Tiny dependency-free TF-IDF search over the docs.

Used by the retrieval eval and the MCP server, so both measure and serve the same thing.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from docslib import Page, all_pages

TOKEN = re.compile(r"[a-z0-9]+")
STOPWORDS = set(
    "a an and are as at be by can do does for from how i if in into is it of on or our "
    "should so that the their them they this to we what when where which who why will "
    "with you your".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


@dataclass
class Hit:
    page: Page
    score: float


class Index:
    def __init__(self, pages: list[Page] | None = None) -> None:
        self.pages = [p for p in (pages or all_pages()) if not p.error]
        self.vectors: list[dict[str, float]] = []
        docs = []
        for page in self.pages:
            # Title and description are weighted up: they are written for retrieval.
            head = f"{page.meta.get('title', '')} {page.meta.get('description', '')}"
            docs.append(Counter(tokenize(head) * 3 + tokenize(page.body)))
        df = Counter(term for doc in docs for term in doc)
        n = len(docs)
        self.idf = {term: math.log((1 + n) / (1 + count)) + 1 for term, count in df.items()}
        for doc in docs:
            vec = {t: (1 + math.log(c)) * self.idf[t] for t, c in doc.items()}
            norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
            self.vectors.append({t: v / norm for t, v in vec.items()})

    def search(self, query: str, k: int = 3) -> list[Hit]:
        terms = Counter(tokenize(query))
        qvec = {t: (1 + math.log(c)) * self.idf.get(t, 0.0) for t, c in terms.items()}
        norm = math.sqrt(sum(v * v for v in qvec.values())) or 1.0
        scored = [
            Hit(page, sum(w / norm * vec.get(t, 0.0) for t, w in qvec.items()))
            for page, vec in zip(self.pages, self.vectors)
        ]
        scored.sort(key=lambda h: h.score, reverse=True)
        return [h for h in scored[:k] if h.score > 0]
