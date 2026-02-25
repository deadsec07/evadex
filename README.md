# EvadeX: Evasion Simulation & RL Environment

[![Docs](https://img.shields.io/badge/docs-live-blue.svg)](https://deadsec07.github.io/evadex/)
[![CI](https://github.com/deadsec07/evadex/actions/workflows/ci.yml/badge.svg)](https://github.com/deadsec07/evadex/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/release/deadsec07/evadex?display_name=tag&sort=semver&label=version)](https://github.com/deadsec07/evadex/releases)

EvadeX is an educational simulation that demonstrates simple evasive maneuvering in 2D/3D and a minimal reinforcement-learning environment for research. It is not intended for real-world deployment or integration into any physical or weapons-related system. See Safety Notice below.

---

## Features

- Real-time 2D evasion simulation with optional GUI
- Dynamic Window–style evasive heuristic (sampling-based)
- Telemetry CSV export for analysis and replay
- Minimal Gym environment for RL experiments (optional)
- 3D example visualizations (examples)

---

## Safety Notice

- This repository is for research and learning only and does not provide guidance for real-world or weapons-related use.
- Do not use EvadeX to design, build, deploy, or integrate systems intended to cause harm or to evade safety, law-enforcement, or monitoring systems.
- The maintainers disclaim any fitness for operational or safety-critical applications.

---

## Quickstart

Prerequisites: Python 3.10+

1) Create a virtual environment and install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -e .
```

2) Run the 2D simulation

```bash
evadex-sim --no-gui             # headless, writes out/telemetry.csv
evadex-sim --steps 800          # change steps
evadex-sim --out out/run1.csv   # change output path
evadex-sim --planner greedy     # choose planner (dwa|greedy)
evadex-sim --scenario scenarios/sample_scenario.json  # use a scenario file
```

3) Show the GUI (requires a display)

```bash
evadex-sim                      # opens a matplotlib window
```

Artifacts are written to `out/`.

---

## Project Layout

```
evadex/
  __init__.py
  cli.py            # console entry: evadex-sim
  sim2d.py          # 2D simulation and GUI
  missile.py        # kinematics model
  interceptor.py    # simple pure-pursuit model
  evasion_ai.py     # DWA-style evasive policy
  env.py            # Gym environment (optional)
examples/           # 3D visualization scripts (see files in repo root)
tests/              # basic tests
```

---

## Development

Install dev tools and run checks:

```bash
pip install -e .[dev]
ruff check .
black --check .
pytest -q
```

Makefile shortcuts:

```
make fmt      # format
make lint     # lint
make test     # tests
make sim      # quick headless sim
make telemetry # plot latest telemetry to PNG
```

---

## Optional: RL Training

The minimal Gym environment is provided for experimentation.

```bash
pip install -e .[rl]
python train_rl.py
```

---

## Telemetry Viewer

```
evadex-telemetry --in out/telemetry.csv           # show plot window
evadex-telemetry --in out/telemetry.csv --no-gui --save out/plot.png
```

---

## Docker

```
docker build -t evadex .
docker run --rm -it evadex evadex-sim --no-gui --steps 50
```

---

## Contributing

Please see CONTRIBUTING.md. For security disclosures, see SECURITY.md.

---

## License

All rights reserved by the project owner unless stated otherwise. No license is granted for operational defense use. Contact the owner for permissions.

---

## Releases & Docs

- Tag a release (e.g., `v0.1.0`) to trigger the Release workflow. It builds wheels/sdist and attaches them to the GitHub release.
- Docs are published via GitHub Pages at: https://deadsec07.github.io/evadex/
- CI builds docs on every push. The Deploy Docs workflow publishes the `site/` output to Pages.
