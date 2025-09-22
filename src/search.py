import heapq
import time
from collections import deque

def neighbors4(r,c):
    return [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]

class Result:
    def __init__(self, path, cost, expanded, time_s):
        self.path = path
        self.cost = cost
        self.expanded = expanded
        self.time = time_s

def bfs(grid, start, goal):
    sr,sc = start
    gr,gc = goal
    start_time = time.time()
    q = deque()
    q.append((sr,sc))
    parent = { (sr,sc): None }
    expanded = 0
    while q:
        r,c = q.popleft()
        expanded += 1
        if (r,c) == (gr,gc):
            break
        for nr,nc in neighbors4(r,c):
            if grid.in_bounds(nr,nc) and grid.is_static_free(nr,nc) and (nr,nc) not in parent:
                parent[(nr,nc)] = (r,c)
                q.append((nr,nc))
    path = []
    node = (gr,gc)
    if node not in parent:
        return Result([], float('inf'), expanded, time.time()-start_time)
    while node:
        path.append(node)
        node = parent[node]
    path.reverse()
    cost = len(path)-1 if path else float('inf')
    return Result(path, cost, expanded, time.time()-start_time)

def ucs(grid, start, goal):
    sr,sc = start
    gr,gc = goal
    start_time = time.time()
    pq = []
    heapq.heappush(pq, (0, sr, sc))
    dist = { (sr,sc): 0 }
    parent = { (sr,sc): None }
    expanded = 0
    while pq:
        cost, r, c = heapq.heappop(pq)
        expanded += 1
        if (r,c) == (gr,gc):
            break
        for nr,nc in neighbors4(r,c):
            if not grid.in_bounds(nr,nc): continue
            if grid.is_wall(nr,nc): continue
            move_cost = grid.grid[nr][nc] if grid.grid[nr][nc] >= 1 else 1
            nd = cost + move_cost
            if (nr,nc) not in dist or nd < dist[(nr,nc)]:
                dist[(nr,nc)] = nd
                parent[(nr,nc)] = (r,c)
                heapq.heappush(pq, (nd, nr, nc))
    node = (gr,gc)
    if node not in parent:
        return Result([], float('inf'), expanded, time.time()-start_time)
    path = []
    while node:
        path.append(node)
        node = parent[node]
    path.reverse()
    return Result(path, dist[(gr,gc)], expanded, time.time()-start_time)

def astar(grid, start, goal, heuristic='manhattan'):
    sr,sc = start
    gr,gc = goal
    start_time = time.time()
    def h(a,b):
        if heuristic == 'manhattan':
            return abs(a[0]-b[0]) + abs(a[1]-b[1])
        return 0
    pq = []
    heapq.heappush(pq, (h((sr,sc),(gr,gc)), 0, sr, sc))
    gscore = { (sr,sc): 0 }
    parent = { (sr,sc): None }
    expanded = 0
    while pq:
        f, cost, r, c = heapq.heappop(pq)
        expanded += 1
        if (r,c) == (gr,gc):
            break
        for nr,nc in neighbors4(r,c):
            if not grid.in_bounds(nr,nc): continue
            if grid.is_wall(nr,nc): continue
            tentative = cost + (grid.grid[nr][nc] if grid.grid[nr][nc]>=1 else 1)
            if (nr,nc) not in gscore or tentative < gscore[(nr,nc)]:
                gscore[(nr,nc)] = tentative
                parent[(nr,nc)] = (r,c)
                heapq.heappush(pq, (tentative + h((nr,nc),(gr,gc)), tentative, nr, nc))
    node = (gr,gc)
    if node not in parent:
        return Result([], float('inf'), expanded, time.time()-start_time)
    path = []
    while node:
        path.append(node)
        node = parent[node]
    path.reverse()
    return Result(path, gscore[(gr,gc)], expanded, time.time()-start_time)

def simulate_with_replanning(grid, start, goal, planner='astar', heuristic='manhattan'):
    # This runs the agent step-by-step. It uses the given planner to compute a path at t=0
    # At each timestep t (starting 0), dynamic obstacles move. If the next step is occupied,
    # agent triggers replanning, logs the event and replans from current position.
    r,c = start
    t = 0
    log = []
    total_expanded = 0
    total_time = 0.0
    plan_result = None
    if planner == 'astar':
        plan_result = astar(grid, (r,c), goal, heuristic=heuristic)
    elif planner == 'ucs':
        plan_result = ucs(grid, (r,c), goal)
    elif planner == 'bfs':
        plan_result = bfs(grid, (r,c), goal)
    else:
        plan_result = astar(grid, (r,c), goal, heuristic=heuristic)
    if not plan_result.path:
        return {'path':[], 'log':log, 'expanded': plan_result.expanded, 'time': plan_result.time}
    path = plan_result.path
    total_expanded += plan_result.expanded
    total_time += plan_result.time
    # follow path step by step
    idx = 1
    while (r,c) != goal and idx < len(path):
        next_r,next_c = path[idx]
        # check if next cell will be occupied at time t+1
        if not grid.is_free_at(next_r,next_c,t+1):
            # replan triggered
            log.append(('replan_triggered', (r,c), (next_r,next_c), t+1))
            # replan from current position at time t+1 (we advance time one step to simulate perception)
            t += 1
            if planner == 'astar':
                plan_result = astar(grid, (r,c), goal)
            elif planner == 'ucs':
                plan_result = ucs(grid, (r,c), goal)
            elif planner == 'bfs':
                plan_result = bfs(grid, (r,c), goal)
            else:
                plan_result = astar(grid, (r,c), goal)
            total_expanded += plan_result.expanded
            total_time += plan_result.time
            if not plan_result.path:
                return {'path':[], 'log':log, 'expanded': total_expanded, 'time': total_time}
            path = plan_result.path
            idx = 1
            continue
        # move to next
        r,c = next_r,next_c
        t += 1
        idx += 1
    return {'path': path, 'log': log, 'expanded': total_expanded, 'time': total_time}

def local_search_simulated(grid, start, goal, max_iters=2000):
    # A simple stochastic hill-climbing on paths: random perturbations + keep better path (by cost)
    import random, math, time
    start_time = time.time()
    # Initialize with greedy BFS path if available, else random walk
    res = bfs(grid, start, goal)
    if not res.path:
        return Result([], float('inf'), res.expanded, time.time()-start_time)
    best_path = res.path
    best_cost = path_cost(grid, best_path)
    expanded = res.expanded
    iters = 0
    while iters < max_iters:
        iters += 1
        # mutate: pick an index and try to re-route locally
        if len(best_path) < 3:
            break
        i = random.randint(1, len(best_path)-2)
        r,c = best_path[i]
        # try random neighbor to replace suffix
        nbrs = [n for n in neighbors4(r,c) if grid.in_bounds(n[0],n[1]) and not grid.is_wall(n[0],n[1])]
        if not nbrs: 
            continue
        nr,nc = random.choice(nbrs)
        # try to connect nr,nc to goal with A*
        res2 = astar(grid, (nr,nc), goal)
        expanded += res2.expanded
        if not res2.path:
            continue
        new_path = best_path[:i] + [(nr,nc)] + res2.path
        new_cost = path_cost(grid, new_path)
        if new_cost < best_cost:
            best_path = new_path
            best_cost = new_cost
    return Result(best_path, best_cost, expanded, time.time()-start_time)

def path_cost(grid, path):
    if not path: return float('inf')
    cost = 0
    for (r,c) in path[1:]:
        cost += (grid.grid[r][c] if grid.grid[r][c] >= 1 else 1)
    return cost
