PY?=python
PIP?=pip

.PHONY: install dev lint fmt test sim telemetry docs-serve docs-build clean

install:
	$(PIP) install -e .

dev:
	$(PIP) install -e .[dev]

lint:
	ruff check .
	black --check .

fmt:
	ruff check --fix . || true
	black .

test:
	pytest -q

sim:
	evadex-sim --no-gui --steps 10

telemetry:
	evadex-telemetry --in out/telemetry.csv --save out/telemetry.png --no-gui

docs-serve:
	$(PIP) install -e .[docs]
	mkdocs serve

docs-build:
	$(PIP) install -e .[docs]
	mkdocs build --strict

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info out

