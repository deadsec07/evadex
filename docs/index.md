# EvadeX

EvadeX is an educational 2D/3D pursuit–evasion simulator with a minimal RL environment. It demonstrates sampling-based evasive maneuvering, telemetry logging, and basic visualization. It is not intended for real-world deployment.

- Quickstart: install with `pip install -e .` and run `evadex-sim`.
- Headless mode: `evadex-sim --no-gui` writes `out/telemetry.csv`.
- Plot telemetry: `evadex-telemetry --in out/telemetry.csv --no-gui --save out/plot.png`.

See Usage for CLI details and Scenarios for configuration.

> Safety: Do not use this code to build or integrate operational systems.

