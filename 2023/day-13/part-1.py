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


def find_reflection_line(matrix):
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
        is_reflection_line = True

        for offset in range(min(middle_row, num_rows - middle_row)):
            if matrix[middle_row + offset] != matrix[middle_row - offset - 1]:
                is_reflection_line = False
                break

        if is_reflection_line:
            return middle_row

    return 0


def calculate_reflection(pattern):
    """
    Calculates the summary of all patterns based on their lines of reflection.

    :param patterns: List of patterns.
    :return: The final summary number.

    >>> calculate_reflection(['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'])
    5

    >>> calculate_reflection(['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#'])
    400
    """
    horizontal = find_reflection_line(pattern)
    vertical = find_reflection_line(list(zip(*pattern)))
    return horizontal * 100 + vertical


def calculate_summary(patterns):
    """
    Calculates the summary of all patterns based on their lines of reflection.

    :param patterns: List of patterns.
    :return: The final summary number.

    >>> calculate_summary([['#.##..##.', '..#.##.#.', '##......#', '##......#', '..#.##.#.', '..##..##.', '#.#.##.#.'], ['#...##..#', '#....#..#', '..##..###', '#####.##.', '#####.##.', '..##..###', '#....#..#']])
    405
    """
    return sum(calculate_reflection(pattern) for pattern in patterns)


# Running doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    patterns = read_data("input.txt")
    result = calculate_summary(patterns)
    print(f"Part 1: {result}")
