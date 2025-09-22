import math

class Grid:
    def __init__(self, grid, dynamic_positions=None):
        # grid: list of lists with integers: 0=free,1=wall, 2=dynamic obstacle marker
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows>0 else 0
        # dynamic_positions: list of (r,c) initial positions for D markers
        self.dynamic_initial = dynamic_positions or []
    @classmethod
    def from_file(cls, filename):
        grid = []
        dynamic_positions = []
        with open(filename, 'r', encoding='utf-8') as f:
            header = f.readline().strip()
            if not header:
                raise ValueError('Empty map file or missing header')
            rows_cols = header.split()
            if len(rows_cols) < 2:
                raise ValueError('Header must contain rows and cols, e.g. "20 20"')
            rows, cols = map(int, rows_cols[:2])
            for r in range(rows):
                line = f.readline()
                if line is None:
                    raise ValueError(f'Expected {rows} rows but file ended early')
                line = line.strip()
                # allow commas, tabs, multiple spaces
                tokens = line.replace('\t',' ').replace(',',' ').split()
                if len(tokens) != cols:
                    raise ValueError(f'Row {r} has {len(tokens)} tokens but expected {cols}: {tokens}')
                row = []
                for c, tk in enumerate(tokens):
                    tk = tk.strip()
                    if tk.upper() == 'D':
                        row.append(2)
                        dynamic_positions.append((r,c))
                    else:
                        # parse ints safely
                        row.append(int(tk))
                grid.append(row)
        if len(grid) != rows:
            raise ValueError(f'Grid has {len(grid)} rows but expected {rows}')
        return cls(grid, dynamic_positions)
    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols
    def is_static_free(self, r, c):
        return self.in_bounds(r,c) and self.grid[r][c] == 0
    def is_wall(self, r, c):
        return not self.in_bounds(r,c) or self.grid[r][c] == 1
    def dynamic_positions_at(self, t):
        # simple deterministic schedule: each dynamic obstacle moves right by t steps modulo cols
        positions = []
        for (r,c0) in self.dynamic_initial:
            c = (c0 + t) % self.cols
            positions.append((r,c))
        return set(positions)
    def is_free_at(self, r, c, t):
        if not self.in_bounds(r,c): 
            return False
        if self.grid[r][c] == 1:
            return False
        if (r,c) in self.dynamic_positions_at(t):
            return False
        return True
