from typing import List

def is_adjacent_to_symbol(matrix: List[List[str]], row: int, col: int) -> bool:
    """
    Checks if the number at the specified position in the matrix is adjacent to a symbol.
    Symbols are any characters other than '.' and digits.

    Args:
    matrix (List[List[str]]): The matrix to be checked.
    row (int): The row index of the number.
    col (int): The column index of the number.

    Returns:
    bool: True if the number is adjacent to a symbol, False otherwise.

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
    >>> is_adjacent_to_symbol(matrix, 0, 2)  # 7 at (0,2)
    True
    >>> is_adjacent_to_symbol(matrix, 5, 7)  # 5 at (5,7)
    False
    >>> is_adjacent_to_symbol(matrix, 5, 8)  # 8 at (5,8)
    False
    >>> is_adjacent_to_symbol(matrix, 0, 5)  # 1 at (0,5)
    False
    >>> is_adjacent_to_symbol(matrix, 0, 6)  # 1 at (0,6)
    False
    >>> is_adjacent_to_symbol(matrix, 0, 7)  # 4 at (0,7)
    False
    >>> is_adjacent_to_symbol(matrix, 2, 2)  # 3 at (2,2)
    True
    >>> is_adjacent_to_symbol(matrix, 2, 3)  # 5 at (2,3)
    True
    >>> is_adjacent_to_symbol(matrix, 9, 1)  # 6 at (9,1)
    False
    >>> is_adjacent_to_symbol(matrix, 9, 2)  # 6 at (9,2)
    True
    >>> is_adjacent_to_symbol(matrix, 9, 3)  # 4 at (9,3)
    True
    >>> is_adjacent_to_symbol(matrix, 9, 5)  # 5 at (9,5)
    True
    >>> is_adjacent_to_symbol(matrix, 9, 6)  # 9 at (9,6)
    True
    >>> is_adjacent_to_symbol(matrix, 9, 7)  # 8 at (9,7)
    False
    """
    # Check if the position is within the matrix boundaries
    if not (0 <= row < len(matrix) and 0 <= col < len(matrix[0])):
        return False

    # Defining the relative positions to check (8 surrounding cells)
    adjacent_positions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    # Check each adjacent position
    for dr, dc in adjacent_positions:
        adj_row, adj_col = row + dr, col + dc
        if 0 <= adj_row < len(matrix) and 0 <= adj_col < len(matrix[0]):
            if matrix[adj_row][adj_col] not in "0123456789.":
                return True

    return False


def extract_numbers_adjacent_to_symbols(matrix: List[List[str]]) -> List[int]:
    """
    Extracts all numbers from the matrix where at least one digit of the number is adjacent to a symbol.

    Args:
    matrix (List[List[str]]): The matrix to be scanned.

    Returns:
    List[int]: A list of numbers that meet the condition.

    Example:
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
    >>> extract_numbers_adjacent_to_symbols(matrix)
    [467, 35, 633, 617, 592, 755, 664, 598]
    """
    extracted_numbers = []
    rows, cols = len(matrix), len(matrix[0])

    def is_digit(ch: str) -> bool:
        """ Check if a character is a digit. """
        return ch.isdigit()

    for i in range(rows):
        j = 0
        while j < cols:
            if is_digit(matrix[i][j]):
                number = int(matrix[i][j])
                j += 1
                while j < cols and is_digit(matrix[i][j]):
                    number = number * 10 + int(matrix[i][j])
                    j += 1

                # Check if any digit of the number is adjacent to a symbol
                for k in range(len(str(number))):
                    if is_adjacent_to_symbol(matrix, i, j - len(str(number)) + k):
                        extracted_numbers.append(number)
                        break
            else:
                j += 1

    return extracted_numbers

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


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    part_number_matrix=read_matrix_from_file("input.txt")
    part_number=extract_numbers_adjacent_to_symbols(part_number_matrix)
    part_number_sum=sum(part_number)
    print(f"Part 1: {part_number_sum}")
