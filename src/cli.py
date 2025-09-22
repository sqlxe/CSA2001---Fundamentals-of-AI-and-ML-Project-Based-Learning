import argparse, json, sys
from .grid import Grid
from . import search

def parse_args():
    p = argparse.ArgumentParser(description='Delivery Agent CLI')
    p.add_argument('--map', required=True, help='map file path under maps/')
    p.add_argument('--algo', required=True, choices=['bfs','ucs','astar','local'], help='planner')
    p.add_argument('--start', required=True, nargs=2, type=int, help='start r c')
    p.add_argument('--goal', required=True, nargs=2, type=int, help='goal r c')
    return p.parse_args()

def main():
    args = parse_args()
    grid = Grid.from_file(args.map)
    start = (args.start[0], args.start[1])
    goal = (args.goal[0], args.goal[1])
    if args.algo == 'bfs':
        res = search.bfs(grid, start, goal)
        print(f'BFS result: cost={res.cost if hasattr(res, "cost") else res.cost}, nodes_expanded={res.expanded}, time={res.time:.4f}s')
        print('path:', res.path)
    elif args.algo == 'ucs':
        res = search.ucs(grid, start, goal)
        print(f'UCS result: cost={res.cost if hasattr(res, "cost") else res.cost}, nodes_expanded={res.expanded}, time={res.time:.4f}s')
        print('path:', res.path)
    elif args.algo == 'astar':
        # For dynamic map, run simulation with replanning
        if any(cell==2 for row in grid.grid for cell in row):
            sim = search.simulate_with_replanning(grid, start, goal, planner='astar')
            print('A* with dynamic replanning simulation:')
            print('final path:', sim['path'])
            print('log:', sim['log'])
            print(f"expanded_total={sim['expanded']}, time_total={sim['time']:.4f}s")
        else:
            res = search.astar(grid, start, goal)
            print(f'A* result: cost={res.cost if hasattr(res, "cost") else res.cost}, nodes_expanded={res.expanded}, time={res.time:.4f}s')
            print('path:', res.path)
    elif args.algo == 'local':
        res = search.local_search_simulated(grid, start, goal)
        print(f'Local search result: cost={res.cost if hasattr(res, "cost") else res.cost}, nodes_expanded={res.expanded}, time={res.time:.4f}s')
        print('path length:', len(res.path))
        print('path:', res.path)

if __name__ == '__main__':
    main()
