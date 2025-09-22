"""A simple local-search based replanner (hill-climbing with random restarts)."""
import random
import time
from copy import deepcopy
from .search import astar, reconstruct_path

def path_cost(grid, path):
    if not path:
        return float('inf')
    return sum(grid.cost(p) for p in path[1:])

def local_replan(grid, start, goal, initial_path=None, time_limit=0.5, restarts=5):
    # initial_path: list of coordinates. We'll try to improve it by replacing random subsegments
    start_time = time.time()
    best = initial_path or astar(grid, start, goal)['path']
    if not best:
        return None
    best_cost = path_cost(grid, best)
    attempts = 0
    while time.time() - start_time < time_limit:
        attempts += 1
        # random restart occasionally
        if attempts % 10 == 0:
            # random restart with small randomized detour
            cur_path = best[:]
        else:
            cur_path = best[:]
        # pick a random subsegment to try to re-route
        if len(cur_path) < 4:
            break
        i = random.randint(0, max(0, len(cur_path)-3))
        j = random.randint(i+2, min(len(cur_path)-1, i+6))
        a = cur_path[i]
        b = cur_path[j]
        # try A* between a and b constrained in small bounding box
        new_segment = astar(grid, a, b)['path']
        if new_segment:
            new_path = cur_path[:i] + new_segment + cur_path[j+1:]
            new_cost = path_cost(grid, new_path)
            if new_cost < best_cost:
                best = new_path
                best_cost = new_cost
        # restarts limit
        if attempts > restarts*20:
            break
    return best
