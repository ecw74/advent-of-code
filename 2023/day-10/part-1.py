from collections import deque


def read_data(filename):
    """
    Reads data from a file and converts it into a matrix.

    Doctest using 'test.txt' with content:
    .....
    .S-7.
    .|.|.
    .L-J.
    .....

    >>> read_data('test.txt')
    [['.', '.', '.', '.', '.'],
     ['.', 'S', '-', '7', '.'],
     ['.', '|', '.', '|', '.'],
     ['.', 'L', '-', 'J', '.'],
     ['.', '.', '.', '.', '.']]
    """
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file.readlines()]
    return matrix


def find_startpoint(matrix):
    """
    Finds the start point 'S' in the matrix.

    >>> find_startpoint([['.', '.', '.', '.', '.'],
    ...                  ['.', 'S', '-', '7', '.'],
    ...                  ['.', '|', '.', '|', '.'],
    ...                  ['.', 'L', '-', 'J', '.'],
    ...                  ['.', '.', '.', '.', '.']])
    (1, 1)
    """
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)
    return None


def valid_move(x, y, direction, matrix):
    """
    Checks if moving in a given direction from a tile is valid.

    Args:
    x (int): X-coordinate of the tile.
    y (int): Y-coordinate of the tile.
    direction (str): The direction of movement ('N', 'S', 'E', 'W').
    matrix (list): The 2D matrix representing the pipes.

    Returns:
    bool: True if the move is valid, False otherwise.
    """
    if direction == 'N' and matrix[x][y] in ['|', 'L', 'J']:
        return True
    if direction == 'S' and matrix[x][y] in ['|', '7', 'F']:
        return True
    if direction == 'E' and matrix[x][y] in ['-', 'L', 'F']:
        return True
    if direction == 'W' and matrix[x][y] in ['-', 'J', '7']:
        return True
    return False


def get_neighbors(x, y, matrix):
    """
    Gets valid neighbors of a tile in all four directions.

    Args:
    x (int): X-coordinate of the tile.
    y (int): Y-coordinate of the tile.
    matrix (list): The 2D matrix representing the pipes.

    Returns:
    list: A list of valid neighboring tiles.
    """
    neighbors = []
    if x > 0 and matrix[x - 1][y] != '.' and valid_move(x - 1, y, 'S', matrix):
        neighbors.append((x - 1, y))
    if x < len(matrix) - 1 and matrix[x + 1][y] != '.' and valid_move(x + 1, y, 'N', matrix):
        neighbors.append((x + 1, y))
    if y > 0 and matrix[x][y - 1] != '.' and valid_move(x, y - 1, 'E', matrix):
        neighbors.append((x, y - 1))
    if y < len(matrix[0]) - 1 and matrix[x][y + 1] != '.' and valid_move(x, y + 1, 'W', matrix):
        neighbors.append((x, y + 1))
    return neighbors


def follow_pipes(matrix):
    """
    Follows the pipes from the start point using BFS and returns the step count to the farthest point.

    Example 1:
    >>> follow_pipes([['.', '.', '.', '.', '.'],
    ...               ['.', 'S', '-', '7', '.'],
    ...               ['.', '|', '.', '|', '.'],
    ...               ['.', 'L', '-', 'J', '.'],
    ...               ['.', '.', '.', '.', '.']])
    4

    Example 2:
    >>> follow_pipes([['.', '.', 'F', '7', '.'],
    ...               ['.', 'F', 'J', '|', '.'],
    ...               ['S', 'J', '.', 'L', '7'],
    ...               ['|', 'F', '-', '-', 'J'],
    ...               ['L', 'J', '.', '.', '.']])
    8
    """
    start = find_startpoint(matrix)
    if not start:
        return None

    queue = deque([(start[0], start[1], 0)])  # (x, y, step count)
    visited = set()
    max_distance = 0

    while queue:
        x, y, distance = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        max_distance = max(max_distance, distance)

        neighbors = get_neighbors(x, y, matrix)
        for next_x, next_y in neighbors:
            if (next_x, next_y) not in visited:
                queue.append((next_x, next_y, distance + 1))

    return max_distance


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Read data from file
    matrix = read_data('input.txt')

    # Follow pipes and print result
    result = follow_pipes(matrix)
    print(f"Part 1: {result}")
