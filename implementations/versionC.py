import sys
import copy
from datetime import datetime
import statistics

def find_possibilities(grid, coord):
    row, col = coord
    num_set = set()

    for i in range(9):
        num_set.add(grid[i][col])
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


def get_num_constraints(grid, coord):
    row, col = coord
    constraints = 0
    for i in range(9):
        if grid[row][i] == 0:
            constraints += 1
        if grid[i][col] == 0:
            constraints += 1
        if grid[row - row % 3 - i // 3][col - col % 3 + i % 3] == 0:
            constraints += 1

    return constraints

def get_num_eliminations(grid, coord, val):
    elims = 0
    row, col = coord
    for i in range(9):
        if grid[row][i] == 0 and val in find_possibilities(grid, (row, i)):
            elims += 1
        if grid[i][col] == 0 and val in find_possibilities(grid, (i, col)):
            elims += 1
        if grid[row - row % 3 + i // 3][col - col % 3 + i % 3] == 0 and val in find_possibilities(grid, (row - row % 3 + i // 3, col - col % 3 + i % 3)):
            elims += 1
    return elims


# Least Constraining Value Heuristic 
# Given a variable, choose the least constraining value: the one that rules out the fewest values in the remaining variables
def lcv(grid, row, col):
    possibilities = find_possibilities(grid, (row, col))
    return sorted(possibilities, key=lambda x : get_num_eliminations(grid, (row, col), x))

# Minimum Remaining Values (Most constrained variable) Heuristic
# Choose the variable which has the fewest "legal" moves
def mrv(empty_cells, grid):
    return min(empty_cells, key=lambda x: len(find_possibilities(grid, (x[0], x[1]))))

# Most Constraining Variable Heuristic
# Choose variable with most constraints on remaining variables - used as tie-breaker among most constrained variables
def mcv(empty_cells, grid):
    return max(empty_cells, key=lambda x: get_num_constraints(grid, (x[0], x[1])))

def solve_puzzle(grid, nodes = 0):

    # keep track of all the empty cells in the grid
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                empty_cells.append((row, col))

    # find the possible values for each cell (forward checking)
    possibilities = {}

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                possibilities[(row, col)] = find_possibilities(grid, (row, col))
    

    # If there are no more empty cells then the grid is full and the puzzle has been completed
    if len(empty_cells) == 0:
        return True, nodes
    
    # use the minimum remaining values (Most constrained variable) heuristic to select a cell
    r, c = mrv(empty_cells, grid)

    # use the most constraining variable heuristic to break any ties in the minimum remaining values heuristic
    ties = [coord for coord in empty_cells if len(find_possibilities(grid, coord)) == len(find_possibilities(grid, (r, c)))]
    if ties:
        r, c = mcv(ties, grid)

    # use the least constraining value heuristic to order the values
    values = lcv(grid, r, c)

    for val in values:
        if val in possibilities[(r, c)]:
            if try_val(grid, (r, c), val):
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


    # The value is valid if it was not already in that square, row or column
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

