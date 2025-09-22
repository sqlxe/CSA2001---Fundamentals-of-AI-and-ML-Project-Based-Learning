"""Implementations of BFS, UCS, and A* with statistics reporting."""
import time
from collections import deque
import heapq
from typing import Tuple, Dict, List
from math import inf

def bfs(grid, start, goal):
    start_time = time.time()
    frontier = deque([start])
    came_from = {start: None}
    nodes_expanded = 0
    while frontier:
        current = frontier.popleft()
        nodes_expanded += 1
        if current==goal:
            break
        for n in grid.neighbors(current):
            if n not in came_from:
                came_from[n]=current
                frontier.append(n)
    end_time = time.time()
    path = reconstruct_path(came_from, start, goal)
    cost = sum(grid.cost(p) for p in path[1:]) if path else None
    return {'path':path, 'cost':cost, 'nodes':nodes_expanded, 'time':end_time-start_time}

def ucs(grid, start, goal, timestep=0):
    start_time = time.time()
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0
    while frontier:
        cur_cost, current = heapq.heappop(frontier)
        nodes_expanded += 1
        if current==goal:
            break
        for n in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n]=new_cost
                heapq.heappush(frontier, (new_cost, n))
                came_from[n]=current
    end_time = time.time()
    path = reconstruct_path(came_from, start, goal)
    cost = cost_so_far.get(goal, None)
    return {'path':path, 'cost':cost, 'nodes':nodes_expanded, 'time':end_time-start_time}

def heuristic(a,b):
    # Manhattan
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar(grid, start, goal, timestep=0):
    start_time = time.time()
    frontier = []
    heapq.heappush(frontier, (0 + heuristic(start,goal), 0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    nodes_expanded = 0
    while frontier:
        _, cur_cost, current = heapq.heappop(frontier)
        nodes_expanded += 1
        if current==goal:
            break
        for n in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(n)
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n]=new_cost
                priority = new_cost + heuristic(n, goal)
                heapq.heappush(frontier, (priority, new_cost, n))
                came_from[n]=current
    end_time = time.time()
    path = reconstruct_path(came_from, start, goal)
    cost = cost_so_far.get(goal, None)
    return {'path':path, 'cost':cost, 'nodes':nodes_expanded, 'time':end_time-start_time}

def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None
    cur = goal
    path = []
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path
