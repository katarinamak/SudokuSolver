import copy

def parse_puzzles():
    puzzle_path = "data/sudoku_grids.txt"
    with open(puzzle_path, 'r') as f:
        lines = f.readlines()
    puzzles = []
    for i in range(0, len(lines), 10):
        grid = []
        for j in range(1, 10): 
            grid.append([int(x) for x in lines[i+j].strip()])
        puzzles.append(grid)
    return puzzles

def solve_sudoku(grid):
    possibilities = {} # maps each empty entry in the grid to a set of possible values
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                find_possibilities(grid, (i, j), possibilities)

    # for i in possibilities:
    #     print(i, possibilities[i])

    while len(possibilities) > 0:
        fill_in(grid, possibilities)

    return grid

def find_possibilities(grid, square, possibilities):
    row, col = square
    s = set(range(1,10))
    # remove items that are in the same row or column
    for i in range(9):
        if grid[row][i] != 0 and grid[row][i] in s:
            s.remove(grid[row][i])
        
        if grid[i][col] != 0 and grid[i][col] in s:
            s.remove(grid[i][col])
    
    # remove items that are in the same square
    for offset_x in range(3):
        for offset_y in range(3):
            if grid[3*(row // 3) + offset_x][3*(col // 3) + offset_y] != 0 and grid[3*(row // 3) + offset_x][3*(col // 3) + offset_y] in s:
                s.remove(grid[3*(row // 3) + offset_x][3*(col // 3) + offset_y])
    
    possibilities[(row, col)] = s
    return possibilities

def fill_in(grid, possibilities):
    if len(possibilities) == 0:
        return grid
    
    # sort possibilities by increasing number of possibilities
    sorted_possibilities = sorted(possibilities.items(), key=lambda x:len(x[1]))

    for i in range(len(sorted_possibilities)):
        print(i, sorted_possibilities[i])

    print("--------------------------------------")

    if len(sorted_possibilities[0]) > 1:
        for sp in sorted_possibilities:
            for val in sp[1]:
                possibilities_copy = copy.deepcopy(dict(sorted_possibilities))
                grid_copy = copy.deepcopy(grid)
                find_possibilities(grid_copy, sp[0], possibilities_copy)
                fill_in(grid_copy, possibilities_copy)

    remove = []
    for p in possibilities:
        # if there is only one possible value, update the entry with that value
        if len(possibilities[p]) == 1: 
            grid[p[0]][p[1]] = next(iter(possibilities[p]))
            # print(p)
            remove.append(p)

    for k in remove: 
        del possibilities[k]

    for i in possibilities:
        find_possibilities(grid, i, possibilities)
        # print(i, possibilities[i])
    
    return grid

def print_grid(grid):
    for row in grid:
        print(row)


def solve_puzzles():
    puzzles = parse_puzzles()
    solved = solve_sudoku(puzzles[0])
    print_grid(solved)
    solved = solve_sudoku(puzzles[1])
    print_grid(solved)
    # for i, puzzle in enumerate(puzzles):
    #     print("Puzzle #{}".format(i+1))
    #     print("Before:")
    #     # print_grid(puzzle)
    #     solved = solve_sudoku(puzzle)
    #     print("After:")
        # print_grid(solved)


solve_puzzles()