#!/bin/bash
echo "Running A* on small.map"
python src/cli.py --map maps/small.map --algo astar --start 0 0 --goal 4 4

echo "\nRunning UCS on medium.map"
python src/cli.py --map maps/medium.map --algo ucs --start 0 0 --goal 9 9

echo "\nRunning agent on dynamic.map with replanning (A*)"
python src/cli.py --map maps/dynamic.map --algo astar --start 0 0 --goal 3 11
