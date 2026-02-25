import os

from evadex.sim2d import run_simulation
from evadex.config import load_scenario
from evadex.telemetry import read_csv, min_clearance, plot_csv


def test_headless_simulation_tmp_out(tmp_path):
    out_csv = tmp_path / "telemetry.csv"
    ok = run_simulation(max_steps=5, telemetry_path=str(out_csv), show_gui=False, seed=42)
    assert out_csv.exists()
    # whether intercepted or not is not important for smoke test
    assert isinstance(ok, bool)


def test_scenario_loader_and_run(tmp_path):
    # create a tiny scenario inline
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(
        """
        {
          "max_steps": 10,
          "seed": 7,
          "missile": [0.0, 0.0, 1.0, 45.0],
          "interceptors": [[10.0, 10.0, 1.0]]
        }
        """,
        encoding="utf-8",
    )
    out_csv = tmp_path / "telemetry.csv"
    ok = run_simulation(
        max_steps=1,  # overridden by scenario
        telemetry_path=str(out_csv),
        show_gui=False,
        seed=None,
        scenario_path=str(scenario_path),
    )
    assert out_csv.exists()
    assert isinstance(ok, bool)


def test_telemetry_read_and_plot(tmp_path):
    out_csv = tmp_path / "telemetry.csv"
    # Produce telemetry
    ok = run_simulation(max_steps=8, telemetry_path=str(out_csv), show_gui=False, seed=1)
    assert out_csv.exists()
    tele = read_csv(str(out_csv))
    mc = min_clearance(tele)
    assert isinstance(mc, float)
    # Plot headless to PNG
    out_png = tmp_path / "plot.png"
    plot_csv(str(out_csv), show_gui=False, save=str(out_png))
    assert out_png.exists()
