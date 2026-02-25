**Contributing Guidelines**

- Use Python 3.10+ and create a virtual environment.
- Run formatters and linters before pushing: `ruff check .` and `black .`.
- Add or update tests for behavior changes; run `pytest` locally.
- Keep PRs focused and small; describe rationale and testing steps.
- Avoid introducing external services or heavyweight dependencies without discussion.

Setup for contributors:

- `pip install -e .[dev]`
- `pre-commit` is optional; if you use it, configure it to run ruff, black, and pytest.

Code style:

- Prefer explicit names and type hints for public functions.
- Keep functions short and cohesive; avoid premature abstraction.
- Document non-obvious choices inline or in module docstrings.

Scope note:

- This project is an educational simulation. Do not submit changes aimed at real-world, weapons-related, or safety-critical deployment.

