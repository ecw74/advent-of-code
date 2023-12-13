def read_data(filepath):
    """
    Reads the input file and returns a list of patterns.

    Each pattern is a list of strings, where each string represents a row of the pattern.

    :param filepath: Path to the file containing the patterns.
    :return: List of patterns.
    """
    pattern = []
    with open(filepath, 'r') as file:
        for p in file.read().strip().split('\n\n'):
            pattern.append(p.split('\n') )
    return pattern


def find_reflection_line(matrix, ignored=-1):
    """
    Finds the line of horizontal reflection in the pattern.

    :param matrix: A list of strings representing the pattern.
    :return: Index of the horizontal line of reflection, or 0 if not found.

    >>> find_reflection_line(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'])
    4
    >>> find_reflection_line(['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'])
    0
    """
    num_rows = len(matrix)

    for middle_row in range(1, num_rows):
        if middle_row != ignored:
            is_reflection_line = True
            for offset in range(min(middle_row, num_rows - middle_row)):
                if matrix[middle_row + offset] != matrix[middle_row - offset - 1]:
                    is_reflection_line = False
                    break
            if is_reflection_line:
                return middle_row
    return 0


def calculate_reflection(pattern, old_vertical=-1, old_horitzontal=-1):
    """
    Calculates the summary of all patterns based on their lines of reflection.

    :param patterns: List of patterns.
    :return: The final summary number.

    >>> calculate_reflection(['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'])
    5

    >>> calculate_reflection(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'])
    400

    >>> calculate_reflection(['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'], 5, -1)
    0

    >>> calculate_reflection(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'], -1, 4)
    0
    """
    horizontal = find_reflection_line(pattern, old_horitzontal)
    vertical = find_reflection_line(list(zip(*pattern)), old_vertical)
    return horizontal * 100 + vertical


def toggle_character(pattern, row, col):
    """Toggle a character in the pattern at the specified row and column."""
    chars = list(pattern[row])
    chars[col] = '.' if chars[col] == '#' else '#'
    if chars[col] == '.':
        chars[col] == '#'
    else:
        chars[col] == '.'
    pattern[row] = ''.join(chars)


def calculate_smudge(pattern):
    """
    Calculate a specific value by manipulating each character in the pattern and
    using the calculate_reflection function.

    Args:
    pattern (List[str]): A list of strings representing the pattern.

    Returns:
    int: The calculated value.

    Examples:
    >>> calculate_smudge(['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'])
    300
    >>> calculate_smudge(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'])
    100
    """
    old_horizontal = find_reflection_line(pattern)
    old_vertical = find_reflection_line(list(zip(*pattern)))

    for row_index in range(len(pattern)):
        for col_index, curr_char in enumerate(pattern[row_index]):
            toggle_character(pattern, row_index, col_index)
            new_value = calculate_reflection(pattern, old_vertical, old_horizontal)
            toggle_character(pattern, row_index, col_index)  # Restore the original character
            if new_value != 0:
                return new_value

    return 0


def calculate_summary(patterns):
    """
    Calculates the summary of all patterns based on their lines of reflection.

    :param patterns: List of patterns.
    :return: The final summary number.

    >>> calculate_summary([['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'], ['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#']])
    400
    """
    return sum(calculate_smudge(pattern) for pattern in patterns)


# Running doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    patterns = read_data("input.txt")
    result = calculate_summary(patterns)
    print(f"Part 2: {result}")
