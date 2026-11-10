PYTHON ?= python
NOTEBOOKS := $(shell find shelves -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' 2>/dev/null)

.PHONY: install install-dl install-tracking demo figure test lint notebooks scan check

# the toolbox, everything the chapters import, and the dev tools
install:
	$(PYTHON) -m pip install -q -e ".[books,dev]"

# torch for the deep-learning chapters, the CPU wheel
install-dl:
	$(PYTHON) -m pip install -q torch --index-url https://download.pytorch.org/whl/cpu

# MLflow for the run log; without it, tracking writes JSON to runs/
install-tracking:
	$(PYTHON) -m pip install -q -e ".[tracking]"

# the four challenges, offline, each printing its number (about three minutes)
demo:
	$(PYTHON) scripts/demo.py

# docs/results.png from the committed results
figure:
	$(PYTHON) scripts/figure.py

test:
	$(PYTHON) -m pytest --cov --cov-report=term-missing:skip-covered --cov-fail-under=90

lint:
	$(PYTHON) -m ruff check .

# every chapter re-executed offline -- a chapter that does not run is not on the shelf
notebooks:
ifeq ($(strip $(NOTEBOOKS)),)
	@echo "no notebooks yet"
else
	$(PYTHON) -m pytest --nbmake --nbmake-timeout=600 -p no:cacheprovider $(NOTEBOOKS)
endif

scan:
	$(PYTHON) scripts/check_private_terms.py

check: lint test notebooks scan
