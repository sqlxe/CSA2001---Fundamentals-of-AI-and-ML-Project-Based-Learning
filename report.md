# Project Report — Autonomous Delivery Agent (short)

**Course:** CSA2001 — Fundamentals of AI and ML  
**Project:** Autonomous delivery agent on 2D grid  
**Author:** (Replace with your name)  
**Date:** (Replace with date)

---

## 1. Environment model
- The environment is a 2D grid (rows x cols). Each cell contains either:
  - `-1` : static obstacle (impassable)
  - `1`  : free cell with movement cost 1
  - `2+` : terrain with integer movement cost >= 2
  - `M`  : moving obstacle (dynamic map only)
- The agent moves 4-connected (up, down, left, right). Movement cost to enter a cell = that cell's integer value.
- Dynamic obstacles in `maps/dynamic.map` are deterministic: they "bounce" horizontally between boundaries each timestep.
  The agent is given knowledge of this schedule for planning up to a fixed horizon.

## 2. Agent design
- The agent has a planner module which can run BFS (ignores costs), UCS (cost optimal), A* (using admissible Manhattan heuristic), or a local-search-based replanner.
- Execution is step-by-step: the agent computes a path then moves one step per timestep.
  If a dynamic obstacle appears on the planned path or next intended cell, the agent triggers a replanning routine.

## 3. Heuristics
- A* uses Manhattan distance multiplied by the minimum traversable cell cost (min_cost=1) — admissible for 4-connected grids with integer costs >=1.
- For experiments we compare A*, UCS, and BFS on path cost, nodes expanded, and wall-clock planning time.

## 4. Local search replanning
- Implemented a hill-climbing with random restarts that tries to improve an initial path by:
  - randomly selecting a subsegment of the path,
  - attempting to re-route that subsegment using A* restricted to a local bounding box,
  - accepting improvements. Restarts allow escaping local optima.
- This is used primarily for unpredictable dynamic obstacles or when a full replan is expensive.

## 5. Experimental results (example)
- Run the scripts in `tests/` to reproduce example runs. Results are printed in console logs including:
  - path cost, nodes expanded, planning time, and whether replanning happened on dynamic map.

## 6. Conclusion
- **UCS** guarantees cheapest-cost path but can expand many nodes when costs vary.
- **A\*** with Manhattan heuristic balances optimality and speed in practice on grid maps.
- **BFS** is only suitable for unit-cost maps.
- **Local-search** can be useful for fast, on-the-fly replanning but may not find globally optimal paths.

(Replace or augment this report with your own experiments and tables to stay within the 6-page limit.)
