"""Agent that executes a plan and replans when dynamic obstacles intervene."""
import time
from .search import astar, ucs, bfs
from .local_search import local_replan

class Agent:
    def __init__(self, grid, algo='astar', max_plan_horizon=50):
        self.grid = grid
        self.algo = algo
        self.max_plan_horizon = max_plan_horizon
        self.log = []

    def plan(self, start, goal, timestep=0):
        if self.algo=='bfs':
            return bfs(self.grid, start, goal)
        elif self.algo=='ucs':
            return ucs(self.grid, start, goal, timestep)
        elif self.algo=='local':
            # local uses astar to get initial path then local_replan
            initial = astar(self.grid, start, goal)
            improved = local_replan(self.grid, start, goal, initial_path=initial['path'], time_limit=0.3)
            return {'path':improved, 'cost': None, 'nodes':0, 'time':0}
        else:
            return astar(self.grid, start, goal, timestep)

    def execute(self, start, goal, max_steps=100):
        cur = start
        timestep = 0
        plan_info = self.plan(cur, goal, timestep)
        path = plan_info['path']
        if not path:
            self.log.append(('fail_no_path',cur,timestep))
            return {'result':'fail','log':self.log}
        step_index = 1
        while cur != goal and timestep < max_steps:
            # if path exhausted (due to replanning), replan
            if step_index >= len(path):
                plan_info = self.plan(cur, goal, timestep)
                path = plan_info['path']
                step_index = 1
                if not path:
                    self.log.append(('fail_no_path',cur,timestep))
                    return {'result':'fail','log':self.log}
            next_pos = path[step_index]
            # check if next_pos is free at next timestep
            if not self.grid.passable(next_pos, timestep+1):
                # replanning triggered
                self.log.append(('replan_triggered',cur,next_pos,timestep+1))
                plan_info = self.plan(cur, goal, timestep+1)
                path = plan_info['path']
                step_index = 1
                if not path:
                    self.log.append(('fail_no_path_after_replan',cur,timestep+1))
                    return {'result':'fail','log':self.log}
                continue
            # otherwise move
            cur = next_pos
            self.log.append(('move',cur,timestep+1))
            timestep += 1
            step_index += 1
        if cur==goal:
            self.log.append(('success',cur,timestep))
            return {'result':'success','log':self.log}
        else:
            self.log.append(('timeout',cur,timestep))
            return {'result':'timeout','log':self.log}
