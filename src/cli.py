"""Command-line interface for running planners on maps."""
import argparse
from src.grid import Grid
from src.dynamic_agent import Agent
from src import search
import pprint
import time

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--map', required=True, help='path to map file')
    p.add_argument('--algo', choices=['bfs','ucs','astar','local'], default='astar')
    p.add_argument('--start', type=int, nargs=2, required=True, help='start row col')
    p.add_argument('--goal', type=int, nargs=2, required=True, help='goal row col')
    p.add_argument('--max_steps', type=int, default=500)
    return p.parse_args()

def main():
    args = parse_args()
    grid = Grid.from_file(args.map)
    agent = Agent(grid, algo=args.algo)
    t0=time.time()
    res = agent.execute(tuple(args.start), tuple(args.goal), max_steps=args.max_steps)
    t1=time.time()
    print('=== Run summary ===')
    print('Map:', args.map)
    print('Algorithm:', args.algo)
    print('Start:', args.start, 'Goal:', args.goal)
    print('Result:', res['result'])
    print('Time elapsed (exec):', t1-t0)
    print('Log:')
    for e in res['log'][:500]:
        print(e)

if __name__=='__main__':
    main()
