#!/usr/bin/env bash
# Example evaluation script that runs tests and prints result
set -e
python3 -m pytest -q
echo "Tests passed."
