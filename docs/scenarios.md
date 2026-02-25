# Scenarios

Scenarios define initial conditions and options in JSON:

```
{
  "max_steps": 600,
  "hit_distance": 2.0,
  "boost_cooldown_time": 5,
  "seed": 1337,
  "planner": "dwa",
  "missile": [5.0, -10.0, 2.0, 30.0],
  "interceptors": [[60.0,60.0,2.0], [-40.0,70.0,2.0]]
}
```

- `missile`: `[x, y, speed, heading_deg]`
- `interceptors`: list of `[x, y, speed]`
- `planner`: `dwa` (sampling horizon) or `greedy` (single-step clearance)

Run with a scenario:

```
evadex-sim --no-gui --scenario scenarios/sample_scenario.json
```

