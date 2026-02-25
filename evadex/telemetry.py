from __future__ import annotations

import csv
from dataclasses import dataclass

import numpy as np


@dataclass
class Telemetry:
    time: np.ndarray
    missile: np.ndarray  # shape (N,2)
    interceptors: list[np.ndarray]  # each (N,2)


def read_csv(path: str) -> Telemetry:
    with open(path, newline="") as f:
        reader = csv.reader(f)
        _ = next(reader, None)
        rows = [list(map(float, r)) for r in reader]

    if not rows:
        raise ValueError("Empty telemetry")
    arr = np.array(rows)
    t = arr[:, 0]
    missile = arr[:, 1:3]
    # remaining columns alternate X,Y for each interceptor
    rest = arr[:, 3:]
    ints: list[np.ndarray] = []
    for i in range(0, rest.shape[1], 2):
        ints.append(rest[:, i : i + 2])
    return Telemetry(time=t, missile=missile, interceptors=ints)


def min_clearance(tele: Telemetry) -> float:
    m = tele.missile
    dmins = []
    for k in range(len(tele.time)):
        dmin = np.inf
        for ip in tele.interceptors:
            d = float(np.linalg.norm(m[k] - ip[k]))
            dmin = min(dmin, d)
        dmins.append(dmin)
    return float(np.min(dmins))


def plot_csv(path: str, show_gui: bool = True, save: str | None = None) -> None:
    tele = read_csv(path)
    if not show_gui:
        import matplotlib

        matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(tele.missile[:, 0], tele.missile[:, 1], "b-", label="Missile")
    for i, ip in enumerate(tele.interceptors):
        ax.plot(ip[:, 0], ip[:, 1], "r--", alpha=0.8, label=("Interceptor" if i == 0 else None))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Telemetry Trajectories")
    ax.grid(True)
    ax.legend(loc="upper left")

    if save:
        fig.savefig(save, bbox_inches="tight")
    if show_gui:
        plt.show()


def main(argv: list[str] | None = None) -> int:  # simple CLI wrapper
    import argparse

    p = argparse.ArgumentParser(description="Plot EvadeX telemetry.csv")
    p.add_argument("--in", dest="inp", required=True, help="Path to telemetry CSV")
    p.add_argument("--save", dest="save", default=None, help="Optional PNG path to save")
    p.add_argument("--no-gui", action="store_true", help="Do not open a window")
    args = p.parse_args(argv)

    plot_csv(args.inp, show_gui=not args.no_gui, save=args.save)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
