import sys
import statistics
from datetime import datetime

def solve_puzzle(grid, nodes = 0):
    cell = None
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                cell = (row, col)

    if cell == None:
        return True, nodes
    
    r, c = cell
    for val in range(1, 10):
        if try_val(grid, cell, val):
            grid[r][c] = val
            nodes += 1
            solved, nodes = solve_puzzle(grid, nodes)
            if solved:
                return True, nodes
            grid[r][c] = 0
    return False, nodes

def try_val(grid, cell, val):
    r, c = cell
    # check if there are duplicates in the given column
    seen_in_row = val in grid[r]

    # check if there are duplicates in the given column
    seen_in_col = val in [grid[row][c] for row in range(9)]

    # check if there are duplicates in the given square
    square = []
    sr = r - (r%3)
    sc = c - (c%3)
    for i in range(3):
        for j in range(3):
            if grid[sr + i][sc + j] != 0:
                square.append(grid[sr + i][sc + j])
    
    seen_in_square = val in square

            
    return not seen_in_square and not seen_in_col and not seen_in_row

def parse_puzzle(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        grid = []
        for line in lines:
            row = []
            for c in range(len(line.strip())):
                row.append(int(line[c]))
            grid.append(row)
        
    return grid

def print_puzzle(grid):
    for row in range(len(grid)):
        print(str(grid[row][0:3]), " | ", str(grid[row][3:6]), " | ", str(grid[row][6:10]))
        if (row%3 == 2):
            print("--------------------------------------")


def solve():
    start = datetime.now()
    path = sys.argv[1]
    grid = parse_puzzle(path)
    _, nodes = solve_puzzle(grid)
    end = datetime.now()
    # print_puzzle(grid)
    return end - start, nodes


data = []
for i in range(50):
    time, nodes = solve()
    data.append(int(time.total_seconds()* 1000000))
    print(nodes)

print("mean: ", statistics.mean(data))
print("sd: ", statistics.stdev(data))


