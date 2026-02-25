import argparse
import os
from .sim2d import run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evadex-sim",
        description="EvadeX 2D evasion simulator (educational research demo)",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=500,
        help="Maximum simulation steps (default: 500)",
    )
    parser.add_argument(
        "--out",
        default=os.path.join("out", "telemetry.csv"),
        help="Path to write telemetry CSV (default: out/telemetry.csv)",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run without opening a matplotlib window",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: None)",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default=None,
        help="Optional path to a JSON scenario file",
    )
    parser.add_argument(
        "--planner",
        type=str,
        choices=["dwa", "greedy"],
        default="dwa",
        help="Planner to use (default: dwa)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    ok = run_simulation(
        max_steps=args.steps,
        telemetry_path=args.out,
        show_gui=not args.no_gui,
        seed=args.seed,
        scenario_path=args.scenario,
        planner=args.planner,
    )
    return 0 if ok else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
