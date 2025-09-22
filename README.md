# Autonomous Delivery Agent (2D Grid) - CSA2001 Project

This repository contains a complete implementation (proof-of-concept) of an autonomous delivery agent
that navigates a 2D grid world with static and deterministic dynamic obstacles. It includes
implementations of BFS, Uniform-Cost Search (UCS), A* with an admissible heuristic, and a simple
local-search based replanning (hill-climbing + random restarts / simulated-annealing inspired).

**What you get**
- `src/` : source code (Python)
- `maps/` : 4 maps (small, medium, large, dynamic)
- `tests/` : quick run scripts showing example runs and logs
- `report.md` : short project report (max ~6 pages when printed)
- `requirements.md` : install / run notes for automated evaluation
- `DeliveryAgentProject.zip` : this entire repository zipped (present in the root)

Run example:
```bash
# create a virtual env (recommended)
python -m venv venv
source venv/bin/activate      # mac/linux
venv\Scripts\activate       # windows

pip install -r requirements.txt

# Example run: A* on small map
python src/cli.py --map maps/small.map --algo astar --start 0 0 --goal 4 4
```

See `requirements.md` for additional info related to automated evaluation.

**Academic honesty**
- This project is provided as a full working example for *learning and reference*. The submitter is responsible
for ensuring that the final uploaded work follows their institution's policies for plagiarism and AI-detection.
