# Delivery Agent Project (Fixed Package)

This repository contains a small delivery-agent project implementing BFS, UCS, A*, and a local-search planner.
It includes dynamic obstacle handling with a simple deterministic schedule (dynamic obstacles marked as 'D' move right each timestep).

## Quick start (from project root)
Assuming Python 3.8+ and you are at project root:
```bash
python -m src.cli --map maps/small.map --algo astar --start 0 0 --goal 4 4
python -m src.cli --map maps/medium.map --algo ucs --start 0 0 --goal 9 9
python -m src.cli --map maps/large.map --algo bfs --start 0 0 --goal 19 19
python -m src.cli --map maps/dynamic.map --algo astar --start 0 0 --goal 7 11
python -m src.cli --map maps/dynamic.map --algo local --start 0 0 --goal 7 11
python experiments/run_all.py
```

## Files created / fixed
- src/grid.py (robust parser + dynamic handling)
- src/search.py (BFS/UCS/A*/local + dynamic replanning simulate function)
- src/cli.py (command-line interface)
- maps/*.map (small, medium, large, dynamic)
- experiments/run_all.py (runs the requested experiments and writes CSV)
- docs/report.md (short report)
