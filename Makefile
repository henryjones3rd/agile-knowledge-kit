PY ?= python3

.PHONY: install check llms serve build

install:
	$(PY) -m pip install -r requirements.txt

check: llms
	$(PY) tools/check_frontmatter.py
	$(PY) tools/check_freshness.py
	$(PY) tools/check_links.py
	$(PY) tools/check_terms.py
	$(PY) tools/eval_retrieval.py
	mkdocs build --strict

llms:
	$(PY) tools/build_llms_txt.py

serve:
	mkdocs serve

build:
	mkdocs build --strict
