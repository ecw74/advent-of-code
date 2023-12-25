from typing import List

from typing import List

def find_possible_gear_positions(matrix: List[List[str]]) -> List[List[int]]:
    """
    Finds all asterisks (*) in the matrix that are adjacent to at least one digit.
    Adjacent means either horizontal, vertical, or diagonal.

    Args:
    matrix (List[List[str]]): The matrix to be checked.

    Returns:
    List[List[int]]: A list of coordinates [row, col] of asterisks adjacent to digits.

    Examples:
    >>> matrix = [
    ...     list("467..114.."),
    ...     list("...*......"),
    ...     list("..35..633."),
    ...     list("......#..."),
    ...     list("617*......"),
    ...     list(".....+.58."),
    ...     list("..592....."),
    ...     list("......755."),
    ...     list("...$.*...."),
    ...     list(".664.598..")
    ... ]
    >>> find_possible_gear_positions(matrix)
    [[1, 3], [4, 3], [8, 5]]
    """
    def is_digit(char: str) -> bool:
        return char.isdigit()

    adjacent_positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    result = []
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == '*':
                for dr, dc in adjacent_positions:
                    adj_row, adj_col = row + dr, col + dc
                    if 0 <= adj_row < len(matrix) and 0 <= adj_col < len(matrix[0]):
                        if is_digit(matrix[adj_row][adj_col]):
                            result.append([row, col])
                            break  # Break after finding the first adjacent digit

    return result

def find_gear_ratios(matrix: List[List[str]], asterisks: List[List[int]]) -> List[List[int]]:
    """
    Finds all numbers adjacent to specified asterisks in the matrix.
    Adjacent means either horizontal, vertical, or diagonal.

    Args:
    matrix (List[List[str]]): The matrix to be checked.
    asterisks (List[List[int]]): Coordinates of asterisks.

    Returns:
    List[List[int]]: A list of lists, each containing numbers adjacent to an asterisk.

    Examples:
    >>> matrix = [
    ...     list("467..114.."),
    ...     list("...*......"),
    ...     list("..35..633."),
    ...     list("......#..."),
    ...     list("617*......"),
    ...     list(".....+.58."),
    ...     list("..592....."),
    ...     list("......755."),
    ...     list("...$.*...."),
    ...     list(".664.598..")
    ... ]
    >>> asterisks = [[1, 3], [4, 3], [8, 5]]
    >>> sorted_lists = [sorted(lst) for lst in find_gear_ratios(matrix, sorted(asterisks))]
    >>> expected = [[35, 467], [617], [598, 755]]
    >>> all(sorted(lst) == sorted(exp) for lst, exp in zip(sorted_lists, expected))
    True
    """
    def get_number_at(matrix, row, col):
        number = ''
        # Check horizontally
        if col > 0 and matrix[row][col-1].isdigit():
            i = col-1
            while i >= 0 and matrix[row][i].isdigit():
                number = matrix[row][i] + number
                i -= 1
        # Check vertically
        if row > 0 and matrix[row-1][col].isdigit():
            i = row-1
            while i >= 0 and matrix[i][col].isdigit():
                number = matrix[i][col] + number
                i -= 1
        number += matrix[row][col]
        # Extend horizontally
        i = col+1
        while i < len(matrix[0]) and matrix[row][i].isdigit():
            number += matrix[row][i]
            i += 1
        # Extend vertically
        i = row+1
        while i < len(matrix) and matrix[i][col].isdigit():
            number += matrix[i][col]
            i += 1
        return int(number)

    adjacent_positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    result = []
    for asterisk in asterisks:
        asterisk_row, asterisk_col = asterisk
        adjacent_numbers = set()
        for dr, dc in adjacent_positions:
            adj_row, adj_col = asterisk_row + dr, asterisk_col + dc
            if 0 <= adj_row < len(matrix) and 0 <= adj_col < len(matrix[0]):
                if matrix[adj_row][adj_col].isdigit():
                    number = get_number_at(matrix, adj_row, adj_col)
                    adjacent_numbers.add(number)
        result.append(list(adjacent_numbers))

    return [lst for lst in result if len(lst) == 2]


def read_matrix_from_file(file_path: str) -> List[List[str]]:
    """
    Reads a matrix from a text file where each row of the matrix is on a new line.

    Args:
    file_path (str): The path to the text file containing the matrix.

    Returns:
    List[List[str]]: The matrix read from the file.
    """
    with open(file_path, 'r') as file:
        matrix = [list(line.strip()) for line in file if line.strip()]
    return matrix


# To run the doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    part_number_matrix = read_matrix_from_file("input.txt")
    possible_gear_locations=find_possible_gear_positions(part_number_matrix)
    gear_ratios=find_gear_ratios(part_number_matrix, possible_gear_locations)
    sum_gear_ratios = [pair[0] * pair[1] for pair in gear_ratios if len(pair) == 2]

    print(f"Part 2: {sum(sum_gear_ratios)}")