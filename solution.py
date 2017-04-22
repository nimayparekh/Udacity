import itertools

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
      for unit in unitlist:
        # Identifies all boxes with pair prospectss
        pairs = [box for box in unit if len(values[box]) == 2]
        # Possible combinations of naked twins
        naked_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
        
        for pair in naked_twins:
            
            box1 = pair[0]
            box2 = pair[1]
            
            if values[box1] == values[box2]:
                for box in unit:
                    if box != box1 and box != box2:
                        for digit in values[box1]:
                            values[box] = values[box].replace(digit,'')
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    
    cross_product = [a+b for a in A for b in B]
    return cross_product

boxes = cross(rows, cols)
# Generates a list of all the units in a sudoku
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
# Maps all peers of each box
units = dict((a, [u for u in unitlist if a in u]) for a in boxes)
peers = dict((a, set(sum(units[a],[]))-set([a])) for a in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789'
        else:
            sudoku_grid[key] = val
    return sudoku_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
     width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()
    
def eliminate(values):
new_values = values.copy()
    for box in values:
        if len(values[box]) == 1:
            for p in peers[box]:
                assign_value(evalues, p, evalues[p].replace(values[box], ''))
    return new_values

def only_choice(values):
    new_values = values.copy()
    for unit in diag_unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in new_values[box]]
            if len(dplaces) == 1:
                new_values[dplaces[0]] = digit
                assign_value(new_values, dplaces[0], new_values[dplaces[0]]) # viz
    return new_values

def reduce_puzzle(values):
    new_values = values.copy()
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Eliminating via exclusion
        values = eliminate(values)
        values = naked_twins(values)
        # Creating a reductionist strategy to a single remainder option
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # Reduce the puzzle using the function reduce_puzzle
    new_values = reduce_puzzle(values.copy())
    if new_values is False:
        return False 
    if all(len(new_values[s]) == 1 for s in squares):
        return new_values
    # Selection of blank squares 
    n,s = min((len(new_values[s]), s) for s in squares if len(new_values[s]) > 1)
    #Solve for remainder sudokus
    for value in new_values[s]:
        new_sudoku = new_values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    return search(grid)

    #Solves for Sudoku Grid
    if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    #Exceptions
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
        except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
