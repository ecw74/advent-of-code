from functools import cache


def read_and_preprocess(input_path):
    """
    Reads and preprocesses the puzzle input into a list of lists.

    :param input_path: Path to the file containing the puzzle input.
    :return: A list of lists representing the grid.
    """
    with open(input_path, 'r') as file:
        return [list(line.strip()) for line in file]


@cache
def rotate_matrix_90_clockwise(matrix):
    """
    Rotates a 2D matrix (list of lists) 90 degrees clockwise.

    Args:
    matrix: A 2D matrix to be rotated.

    Returns:
      The rotated matrix.
    """
    # Transpose the matrix and reverse each row
    return tuple(tuple(row) for row in zip(*matrix[::-1]))


@cache
def move_rock_right(column):
    """
    Moves a rounded rock 'O' to left as far as possible.
    Stop on solid rocks '#'.
    Stop on rounded rocks 'O'

    :param column: A list representing a single column of the grid.
    :return: Modified column with the rock moved north.

    >>> result = move_rock_right(tuple(['O','O','.','O','.','O','.','.','#','#']))
    >>> result == ('.', '.', '.', '.', 'O', 'O', 'O', 'O', '#', '#')
    True

    >>> result = move_rock_right(tuple(['.','.','.','O','O','.','.','.','.','O']))
    >>> result == ('.', '.', '.', '.', '.', '.', '.', 'O', 'O', 'O')
    True

    >>> result = move_rock_right(tuple(['.','O','.','.','.','#','O','.','.','O']))
    >>> result == ('.', '.', '.', '.', 'O', '#', '.', '.', 'O', 'O')
    True

    >>> result = move_rock_right(tuple(['.','O','.','#','.','.','.','.','.','.']))
    >>> result == ('.', '.', 'O', '#', '.', '.', '.', '.', '.', '.')
    True
    """

    # Find the segments separated by '#'
    segments = ''.join(column).split('#')

    @cache
    def move_rocks_in_segment(segment):
        """
        Move all 'O' in a segment to the left as far as possible.

        :param segment: A string representing a segment of the column.
        :return: Modified segment as a string.
        """
        rocks = segment.count('O')
        empty_spaces = len(segment) - rocks
        return '.' * empty_spaces + 'O' * rocks

    # Process each segment
    moved_segments = [move_rocks_in_segment(seg) for seg in segments]

    # Join the segments with '#' and convert back to a list
    moved_column = list('#'.join(moved_segments))

    return tuple(moved_column)


def calculate_load(grid):
    """
    Calculates the total load on the north support beams.

    :param grid: A list of lists representing the grid.
    :return: The total load value.

    >>> grid = [['O', 'O', 'O', 'O', '.', '#', '.', 'O', '.', '.'],
    ...         ['O', 'O', '.', '.', '#', '.', '.', '.', '.', '#'],
    ...         ['O', 'O', '.', '.', 'O', '#', '#', '.', '.', 'O'],
    ...         ['O', '.', '.', '#', '.', 'O', 'O', '.', '.', '.'],
    ...         ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'],
    ...         ['.', '.', '#', '.', '.', '.', '.', '#', '.', '#'],
    ...         ['.', '.', 'O', '.', '.', '#', '.', 'O', '.', 'O'],
    ...         ['.', '.', 'O', '.', '.', '.', '.', '.', '.', '.'],
    ...         ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
    ...         ['#', '.', '.', '.', '.', '#', '.', '.', '.', '.']]
    >>> calculate_load(grid)
    136
    """
    total_load = 0
    height = len(grid)
    for i in range(height):
        total_load += sum(1 for cell in grid[i] if cell == 'O') * (height - i)
    return total_load


def calculate_longterm_load(grid):
    """
    Calculate longterm load for the grid

    :param grid: A list of lists representing the grid.
    :return: Modified grid with all rocks moved north.

    >>> grid = [['O', '.', '.', '.', '.', '#', '.', '.', '.', '.'],
    ...         ['O', '.', 'O', 'O', '#', '.', '.', '.', '.', '#'],
    ...         ['.', '.', '.', '.', '.', '#', '#', '.', '.', '.'],
    ...         ['O', 'O', '.', '#', 'O', '.', '.', '.', '.', 'O'],
    ...         ['.', 'O', '.', '.', '.', '.', '.', 'O', '#', '.'],
    ...         ['O', '.', '#', '.', '.', 'O', '.', '#', '.', '#'],
    ...         ['.', '.', 'O', '.', '.', '#', 'O', '.', '.', 'O'],
    ...         ['.', '.', '.', '.', '.', '.', '.', 'O', '.', '.'],
    ...         ['#', '.', '.', '.', '.', '#', '#', '#', '.', '.'],
    ...         ['#', 'O', 'O', '.', '.', '#', '.', '.', '.', '.']]
    >>> calculate_longterm_load(grid)
    64
    """
    processed_columns = tuple(tuple(row) for row in grid)

    cache = {}
    cycles = 1000000000
    cyc = 0
    while cyc < cycles:
        for i in range(4):
            processed_columns = rotate_matrix_90_clockwise(processed_columns)
            processed_columns = tuple(move_rock_right(row) for row in processed_columns)
        matrix_hash = hash(str(processed_columns))
        if matrix_hash in cache:
            remaining = cycles - cyc
            off = cyc - cache[matrix_hash]
            cyc += remaining // off * off
            cache.clear()
        cache[matrix_hash] = cyc
        cyc += 1
    return calculate_load(processed_columns)

if __name__ == "__main__":
    grid = read_and_preprocess("input.txt")
    longterm_load = calculate_longterm_load(grid)
    print(f"The total load on the north support beams is: {longterm_load}")
