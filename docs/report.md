# Delivery Agent Project - Short Report (Proof-of-concept)

## Environment model
- Grid: rectangular cells. Header is `rows cols` followed by rows lines of integer tokens.
- Tokens: `0` free, `1` static obstacle (wall), `2` dynamic internal marker (in file written as `D`).
- Movement: 4-connected (up/down/left/right).
- Terrain costs: integer cell cost >=1. If cell value >=1 it is used as movement cost (1 for free cells).

## Dynamic obstacles
- Dynamic obstacles (marked `D` in map) move deterministically: they shift right by 1 cell every timestep (modulo map width).
- Planner simulates agent step-by-step; if next cell will be occupied at t+1, replanning is triggered and logged as:
('replan_triggered', (r,c), (next_r,next_c), timestep)

## Agents and planners
- BFS: breadth-first search on static map (returns shortest in steps).
- UCS: uniform cost search (accounts for terrain costs).
- A*: informed with Manhattan heuristic (admissible for grid with unit costs).
- Local search: stochastic hill-climbing that mutates existing path and tries improvements via A* on suffixes.

## Experiments & results
See `experiments/run_all.py` which runs 5 scenario cases and writes `experiments/experiments_output.csv`.

## Analysis (short)
- BFS is good on unweighted uniform-cost grids (fast, minimal expansions for few obstacles).
- UCS handles varying terrain costs; A* with good heuristic expands fewer nodes than UCS while being optimal with admissible heuristics.
- Dynamic replanning required when moving obstacles block the planned path; A* with replanning shows overhead but remains effective for sparse dynamic events.
- Local search can find improved-cost paths quickly in some maps but is not guaranteed or optimal; useful when replanning quickly and time-limited.

## Demo & reproducibility
Run the CLI commands from README. `experiments/run_all.py` automates the main scenarios and collects outputs.
