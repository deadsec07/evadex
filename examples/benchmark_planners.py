from __future__ import annotations

import glob
import os
from pathlib import Path

from evadex.sim2d import run_simulation
from evadex.telemetry import read_csv, min_clearance, plot_csv


def main() -> None:
    out_dir = Path("out/benchmarks")
    out_dir.mkdir(parents=True, exist_ok=True)

    scenarios = sorted(glob.glob("scenarios/benchmarks/*.json"))
    planners = ["dwa", "greedy"]

    print("Benchmarking planners on scenarios:")
    for sc in scenarios:
        base = Path(sc).stem
        for p in planners:
            out_csv = out_dir / f"{base}_{p}.csv"
            ok = run_simulation(
                telemetry_path=str(out_csv),
                show_gui=False,
                scenario_path=sc,
                planner=p,
            )
            tele = read_csv(str(out_csv))
            clearance = min_clearance(tele)
            out_png = out_dir / f"{base}_{p}.png"
            plot_csv(str(out_csv), show_gui=False, save=str(out_png))
            print(f"- {base:10s} planner={p:6s} evaded={ok} min_clearance={clearance:.2f}")


if __name__ == "__main__":
    main()

