import sys
from solution import solve

def main():
    data = sys.stdin.read().rstrip('\n')
    # Many graders pass input via stdin; we pass the raw string to solve()
    # The solve() function should read from sys.stdin directly or accept a string input.
    # Here we pass the raw text and let solve() parse it.
    if data == "":
        # No input; still call solve to allow interactive testing
        solve()
    else:
        solve(data)

if __name__ == "__main__":
    main()
