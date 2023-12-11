import queue

def read_and_preprocess_data(filename):
    """
    Reads data from a file and preprocesses it into a 2D matrix.

    Args:
    filename (str): The name of the file to read from.

    Returns:
    list: A 2D list representing the matrix.

    Doctest:
    >>> read_and_preprocess_data('test.txt')
    [['.', '.', '.', '.', '.'], ['.', 'S', '-', '7', '.'], ['.', '|', '.', '|', '.'], ['.', 'L', '-', 'J', '.'], ['.', '.', '.', '.', '.']]
    """
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]

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
    if x > 0 and matrix[x-1][y] != '.' and valid_move(x-1, y, 'S', matrix):
        neighbors.append((x-1, y))
    if x < len(matrix)-1 and matrix[x+1][y] != '.' and valid_move(x+1, y, 'N', matrix):
        neighbors.append((x+1, y))
    if y > 0 and matrix[x][y-1] != '.' and valid_move(x, y-1, 'E', matrix):
        neighbors.append((x, y-1))
    if y < len(matrix[0])-1 and matrix[x][y+1] != '.' and valid_move(x, y+1, 'W', matrix):
        neighbors.append((x, y+1))
    return neighbors


def process_pipes(matrix):
    """
    Process the matrix to calculate the steps from the starting position.

    Args:
    matrix (list): The 2D matrix representing the pipes.

    Returns:
    list: The matrix with updated step counts.

    Doctest:
    >>> process_pipes([['.', '.', '.', '.', '.'], ['.', 'S', '-', '7', '.'], ['.', '|', '.', '|', '.'], ['.', 'L', '-', 'J', '.'], ['.', '.', '.', '.', '.']])
    [['.', '.', '.', '.', '.'], ['.', '0', '1', '2', '.'], ['.', '1', '.', '3', '.'], ['.', '2', '3', '4', '.'], ['.', '.', '.', '.', '.']]
    >>> process_pipes([['.', '.', 'F', '7', '.'], ['.', 'F', 'J', '|', '.'], ['S', 'J', '.', 'L', '7'], ['|', 'F', '-', '-', 'J'], ['L', 'J', '.', '.', '.']])
    [['.', '.', '4', '5', '.'], ['.', '2', '3', '6', '.'], ['0', '1', '.', '7', '8'], ['1', '4', '5', '6', '7'], ['2', '3', '.', '.', '.']]
    """
    start_x, start_y = next((x, y) for x in range(len(matrix)) for y in range(len(matrix[0])) if matrix[x][y] == 'S')
    q = queue.Queue()
    q.put((start_x, start_y, 0))

    # Added: Matrix to keep track of the highest step count reached at each tile
    max_steps = [[-1 for _ in row] for row in matrix]
    max_steps[start_x][start_y] = 0

    while not q.empty():
        x, y, step = q.get()
        matrix[x][y] = str(step)

        for neighbor in get_neighbors(x, y, matrix):
            nx, ny = neighbor

            # Check if the new step count is higher than the currently recorded step count
            if step + 1 > max_steps[nx][ny]:
                max_steps[nx][ny] = step + 1
                q.put((nx, ny, step + 1))

    return matrix

def find_max_step(matrix):
    """
    Finds the maximum step count in the processed pipe matrix.

    Args:
    matrix (list): The 2D matrix representing the processed pipes.

    Returns:
    int: The maximum step count in the matrix.

    Doctest:
    >>> find_max_step([['.', '.', '.', '.', '.'], ['.', '0', '1', '2', '.'], ['.', '1', '.', '3', '.'], ['.', '2', '3', '4', '.'], ['.', '.', '.', '.', '.']])
    4
    >>> find_max_step([['.', '.', '4', '5', '.'], ['.', '2', '3', '6', '.'], ['0', '1', '.', '7', '8'], ['1', '4', '5', '6', '7'], ['2', '3', '.', '.', '.']])
    8
    """
    max_step = 0
    for row in matrix:
        for cell in row:
            if cell.isdigit():
                max_step = max(max_step, int(cell))
    return max_step


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    data = read_and_preprocess_data("input.txt")
    step_matrix = process_pipes(data)
    max_step = find_max_step(step_matrix)
    print(f"Part 1: {max_step}")
