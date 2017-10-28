'''
udacity aind-submission

sources: https://github.com/udacity/aind-sudoku
https://github.com/udacity/aind-sudoku

'''

#Todo: udacity-pa passing

assignments = []


def assign_value(values, box, value):
    """
    Function to update our values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    '''
    Eliminate values using the naked twins strategy.
    # Find all instances of naked twins
    '''
    nakedunits = row_units + column_units + square_units
    unitNKD = dict((s, [u for u in nakedunits if s in u]) for s in boxes)
    NKDpeers = dict((s, set(sum(unitNKD[s], [])) - set([s])) for s in boxes)

    # get all candidates for naked twins.
    boxlist = [boxtry for boxtry in values.keys() if len(values[boxtry]) == 2]
    # filter canadidates, such that they form maked twins.
    nakedtwins = {(box1, box2) for box1 in boxlist for box2 in NKDpeers[box1] if set(values[box1]) == set(values[box2])}

    # ALGO/DEBUG
    # print("\n Candidates for NKEDTWIN Boxes are: ",boxlist)
    # print("\n REAL Candidates for NKEDTWIN Boxes are: ",nakedtwins)

    # finding waldo.
    for pairs in nakedtwins:
        peerX = NKDpeers[pairs[0]]
        peerY = NKDpeers[pairs[1]]
        # intersection for common peers
        peerNET = (peerX & peerY).difference(x for x in pairs)
        # print("\n\n PEERNET: ",peerNET, "\n PAIRS:" ,pairs) #ALGO/DEBUG
        for peer in peerNET:
            # deletion at len of str > 1, (or 2?)
            if len(values[peer]) > 2:
                for VAL in str(values[pairs[0]]):
                    if VAL in str(values[peer]):
                        values = assign_value(values, peer, values[peer].replace(VAL, ''))

    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]


def grid_values(grid):
    '''
    '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    returns a dictionary, zipped from grid and boxes, such that we have a indexed grid/
    dictionary of {Boxes:values}
    '''
    setx = '123456789'
    try:
        assert len(grid) == 81
        newgrid = dict(zip(boxes, grid))
        for x in newgrid.keys():
            if newgrid[x] == '.':
                newgrid[x] = setx
        return newgrid
    except AssertionError:
        print('invalid size!')


def display(values):
    """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the       values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """

    solved_values = values.keys()
    # the current state

    for box in solved_values:
        if len(values[box]) == 1:
            digit = values[box]
            for peer in peers[box]:
                value = values[peer].replace(digit, "")  # eliminating values
                values = assign_value(values, peer, value)  # updating value!
        else:
            continue
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box,          assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    valucopy = values.copy()
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                valucopy = assign_value(valucopy, dplaces[0], digit)
    return valucopy


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values,       return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved = [box for box in values.keys() if len(values[box]) == 1]
    stalemated = False

    while not stalemated:
        # Check how many boxes have a determined value
        resolution = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Your code here: Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        resolved = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalemated = resolution == resolved
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def delta(values1, values2):
    newdict = dict()

    assert values1.keys() == values2.keys()
    for chk in values1.keys():
        if not values1[chk] == values2[chk]:
            newdict[chk] = (values1[chk], values2[chk])
        else:
            continue
    return newdict

def solve(grid):
    """
    Find the solution to a Sudoku grid.
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.                                  ............3'
    Output: The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    new_values = search(values)
    return new_values



'''
Vars
'''

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
reverse_cols = cols[::-1]
diag1 = [rows[i] + cols[i] for i in range(len(rows))]
diag2 = [rows[i] + reverse_cols[i] for i in range(len(rows))]
diag_units = [diag1, diag2]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
