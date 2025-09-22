"""Grid environment representation and utilities."""
from typing import List, Tuple, Dict
import math

class Grid:
    def __init__(self, grid, moving_obstacles=None):
        # grid: List[List[int]] where -1 = wall, >=1 = movement cost
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows>0 else 0
        self.moving_obstacles = moving_obstacles or []

    @classmethod
    def from_file(cls, path):
        # supports simple map format. Lines beginning with '#' are comments.
        # Each row: space separated tokens.
        # tokens: -1 for wall, integer>=1 for cost, 'M' for moving obstacle cell (treated as free cost 1 but tracked)
        grid = []
        moving = []
        with open(path,'r') as f:
            for r,line in enumerate(f):
                line=line.strip()
                if not line or line.startswith('#'): continue
                parts = line.split()
                row=[]
                for c,tk in enumerate(parts):
                    if tk.upper()=='M':
                        row.append(1)
                        moving.append((r,c))
                    else:
                        val = int(tk)
                        row.append(val)
                grid.append(row)
        return cls(grid, moving)

    def in_bounds(self, pos):
        r,c = pos
        return 0<=r<self.rows and 0<=c<self.cols

    def passable(self, pos, timestep=None):
        r,c = pos
        if not self.in_bounds(pos): return False
        if self.grid[r][c]==-1: return False
        # moving obstacles: treat them as occupying positions at timestep using a simple bounce model
        if timestep is not None:
            for (mr,mc) in self.moving_obstacles:
                # simple deterministic horizontal bounce: obstacle moves right each timestep, bounces at borders
                period = (self.cols-1)*2 if self.cols>1 else 1
                offset = (timestep) % period
                if offset <= (self.cols-1):
                    cur_c = (mc + offset)
                else:
                    cur_c = (mc + period - offset)
                cur_c = cur_c % self.cols
                if (mr, cur_c)==pos:
                    return False
        return True

    def cost(self, to_node):
        r,c = to_node
        return self.grid[r][c]

    def neighbors(self, pos):
        r,c = pos
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = r+dr, c+dc
            if 0<=nr<self.rows and 0<=nc<self.cols and self.grid[nr][nc]!=-1:
                yield (nr,nc)
