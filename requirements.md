# Requirements & Automated Evaluation Notes

- Python 3.9+
- No external heavy dependencies required. The code uses only Python standard library.
- For plotting (optional) matplotlib is used; tests do not require plotting.
- If your automated evaluation environment requires a single requirements file, include:
  - requirements.txt (we include it)
- For automated evaluation:
  - `src/cli.py` is the primary entrypoint. The evaluation script can call it with:
    `python src/cli.py --map <mapfile> --algo <bfs|ucs|astar|local> --start r c --goal r c`
  - Dynamic maps: `maps/dynamic.map` uses moving obstacles that follow a deterministic "bounce" schedule
    known to the agent for a finite horizon (documented in `report.md`).
