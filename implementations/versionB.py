import sys
import copy
import statistics
from datetime import datetime

def find_possibilities(grid, coord):
    row, col = coord
    num_set = set()

    for i in range(9):
        num_set.add(grid[i][col])

    for i in range(9):
        num_set.add(grid[row][i])

    for i in range(3):
        for j in range(3):
            num_set.add(grid[i + 3*(row//3)][j + 3*(col//3)])

    return set(range(10)) - num_set


def update_possibilities(possibilities, new_coords, new_val):
    row, col = new_coords
    possibilities.pop(new_coords)
    for k, v in possibilities.items():
        if row == k[0] or col == k[1] or (row//3 == k[0]//3 and col//3 == k[1]//3):
           possibilities[k] = v - {new_val}

    possibilities = {k: v for k, v in possibilities.items() if len(v) > 0}
    return possibilities


def solve_puzzle(grid, nodes=0):
    # find the possible values for each cell (forward checking)
    possibilities = {}

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                possibilities[(row, col)] = find_possibilities(grid, (row, col))

    cell = None
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                cell = (row, col)

    # if there are no empty cells left then the puzzle is complete
    if cell == None:
        return True, nodes
    
    r, c = cell
    for val in range(1, 10):
        if val in possibilities[(r, c)]:
            if try_val(grid, cell, val):
                grid[r][c] = val
                possibilities_copy = copy.deepcopy(possibilities)
                possibilities_copy = update_possibilities(possibilities_copy, cell, val)
                nodes += 1
                solved, nodes = solve_puzzle(grid, nodes)
                if solved:
                    possibilities = copy.deepcopy(possibilities_copy)
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
    print_puzzle(grid)
    return end - start, nodes


data = []
for i in range(50):
    time, nodes = solve()
    data.append(int(time.total_seconds()* 1000000))
    print(nodes)

print("mean: ", statistics.mean(data))
print("sd: ", statistics.stdev(data))


