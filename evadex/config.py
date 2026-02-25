from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Scenario:
    max_steps: int = 500
    hit_distance: float = 2.0
    boost_cooldown_time: int = 5
    seed: int | None = None
    planner: str | None = None
    missile: tuple[float, float, float, float] | None = None  # x, y, speed, heading_deg
    interceptors: list[tuple[float, float, float]] | None = None  # x, y, speed


def load_scenario(path: str | Path) -> Scenario:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    def _tuple_or_none(key: str, n: int):
        v = data.get(key)
        if v is None:
            return None
        if not (isinstance(v, list) and len(v) == n):
            raise ValueError(f"scenario field '{key}' must be a list of length {n}")
        return tuple(float(x) for x in v)

    def _list_tuples_or_none(key: str, n: int):
        v = data.get(key)
        if v is None:
            return None
        if not isinstance(v, list):
            raise ValueError(f"scenario field '{key}' must be a list")
        items = []
        for i, item in enumerate(v):
            if not (isinstance(item, list) and len(item) == n):
                raise ValueError(f"scenario field '{key}[{i}]' must be a list of length {n}")
            items.append(tuple(float(x) for x in item))
        return items

    return Scenario(
        max_steps=int(data.get("max_steps", 500)),
        hit_distance=float(data.get("hit_distance", 2.0)),
        boost_cooldown_time=int(data.get("boost_cooldown_time", 5)),
        seed=(int(data["seed"]) if data.get("seed") is not None else None),
        planner=(str(data["planner"]).strip() if data.get("planner") else None),
        missile=_tuple_or_none("missile", 4),
        interceptors=_list_tuples_or_none("interceptors", 3),
    )
