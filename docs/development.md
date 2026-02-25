# Development

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Tasks

```
make fmt       # format (ruff+black)
make lint      # lint
make test      # tests
make docs-serve
```

## Tests

- Smoke tests cover headless run and scenario loader.
- Add tests under `tests/` and run with `pytest -q`.

## Safety

This is an educational simulator; do not add features aimed at real-world weaponization or operational use.

