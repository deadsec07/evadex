# Usage

## CLI: Simulation

Run the 2D simulator:

```
evadex-sim                     # GUI
evadex-sim --no-gui            # headless, writes out/telemetry.csv
evadex-sim --steps 800         # steps
evadex-sim --out out/run1.csv  # different output path
evadex-sim --planner greedy    # choose planner (dwa|greedy)
evadex-sim --scenario scenarios/sample_scenario.json
```

## CLI: Telemetry Viewer

```
evadex-telemetry --in out/telemetry.csv           # show plot window
evadex-telemetry --in out/telemetry.csv --no-gui --save out/plot.png
```

