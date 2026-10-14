# Build and test — what a build runner runs for this repository.
#
#   make build   byte-compile the package and build a wheel into dist/
#   make test    run the test suite
#   make check   both
#
# Needs python3 (3.10 or later). The first run creates .venv and installs pytest into it;
# nothing is installed outside this directory.

PYTHON ?= python3
VENV   := .venv
BIN    := $(VENV)/bin

.PHONY: check build test clean

check: build test

$(BIN)/pytest:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --quiet --disable-pip-version-check "pytest>=8" "setuptools>=68" wheel

build: $(BIN)/pytest
	$(BIN)/python -m compileall -q src
	$(BIN)/pip wheel --quiet --no-deps --no-build-isolation --wheel-dir dist .

test: $(BIN)/pytest
	$(BIN)/pytest -q

clean:
	rm -rf $(VENV) dist build src/*.egg-info .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
