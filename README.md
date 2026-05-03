# EvadeX: Evasion Simulation & RL Environment

[![Docs](https://img.shields.io/badge/docs-live-blue.svg)](https://deadsec07.github.io/evadex/)
[![CI](https://github.com/deadsec07/evadex/actions/workflows/ci.yml/badge.svg)](https://github.com/deadsec07/evadex/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/release/deadsec07/evadex?display_name=tag&sort=semver&label=version)](https://github.com/deadsec07/evadex/releases)

EvadeX is an educational pursuit-evasion simulator and minimal RL environment by A A Hasnat. It demonstrates simple evasive maneuvering in 2D and 3D, telemetry export, and research-oriented simulation workflows. It is not intended for real-world deployment or integration into physical or weapons-related systems.

Links:
- Live docs: https://deadsec07.github.io/evadex/
- GitHub: https://github.com/deadsec07/evadex
- Main site: https://hnetechnologies.com/
- Creator profile: https://deadsec07.github.io/

## Features

- Real-time 2D evasion simulation with optional GUI
- Dynamic Window-style evasive heuristic
- Telemetry CSV export for analysis and replay
- Minimal Gym environment for RL experiments
- 3D example visualizations

## Safety Notice

- This repository is for research and learning only.
- Do not use EvadeX to design, build, deploy, or integrate systems intended to cause harm.
- The maintainers disclaim any fitness for operational or safety-critical applications.

## Quickstart

Prerequisites: Python 3.10+

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Run the 2D simulation:

```bash
evadex-sim --no-gui
evadex-sim --steps 800
evadex-sim --out out/run1.csv
```

## Development

```bash
pip install -e .[dev]
ruff check .
black --check .
pytest -q
```

## Releases & Docs

- Tag a release such as `v0.1.0` to trigger the release workflow.
- Docs are published via GitHub Pages at https://deadsec07.github.io/evadex/
