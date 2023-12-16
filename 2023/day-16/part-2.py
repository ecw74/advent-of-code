from collections import deque


def read_input(filename):
    """
    Reads the input file and returns a list of lists representing the grid.

    :param filename: String, the name of the file to read.
    :return: List of lists, representing the grid.

    >>> read_input('test.txt')
    [['.', '|', '.', '.', '.', '\\', '.', '.', '.', '.'], ['|', '.', '-', '.', '\', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '|', '-', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '|', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '\\', '.'], ['.', '.', '.', '/', '.', '\\', '\\', '.', '.', '.'], ['.', '-', '.', '-', '/', '.', '.', '|', '.', '.'], ['.', '|', '.', '.', '.', '.', '-', '|', '.', '\\'], ['.', '.', '/', '/', '.', '|', '.', '.', '.', '.']]
    """
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def change_direction(direction, mirror):
    dr, dc = direction
    if mirror == '/':
        return -dc, -dr
    elif mirror == '\\':
        return dc, dr
    return dr, dc


def is_valid_position(position, map_data):
    r, c = position
    return 0 <= r < len(map_data) and 0 <= c < len(map_data[0])


def propagate_beam(matrix_data, beam):
    visited = set()  # Track visited positions with directions

    rows, cols = len(matrix_data), len(matrix_data[0])
    map = [[0 for _ in range(cols)] for _ in range(rows)]
    queue = deque()

    # Start Conditions
    r, c = beam['position']
    dr, dc = beam['direction']
    cell = matrix_data[r][c]
    if cell in ['/', '\\']:
        dr, dc = change_direction((dr, dc), cell)
        queue.append({'position': (r, c), 'direction': (dr, dc)})
    elif cell == '|' and dc != 0:
        queue.append({'position': (r, c), 'direction': (1, 0)})
        queue.append({'position': (r, c), 'direction': (-1, 0)})
    elif cell == '-' and dr != 0:
        queue.append({'position': (r, c), 'direction': (0, 1)})
        queue.append({'position': (r, c), 'direction': (0, -1)})
    else:
        queue.append(beam)

    map[r][c] = 1

    while queue:
        current_beam = queue.popleft()
        r, c = current_beam['position']
        dr, dc = current_beam['direction']

        while is_valid_position((r + dr, c + dc), matrix_data):
            r += dr
            c += dc

            # Avoid loops by checking if we've already visited this cell with the same direction
            if (r, c, dr, dc) in visited:
                break
            visited.add((r, c, dr, dc))
            map[r][c] = 1
            cell = matrix_data[r][c]

            if cell in ['/', '\\']:
                dr, dc = change_direction((dr, dc), cell)
            elif cell == '|' and dc != 0:
                queue.append({'position': (r, c), 'direction': (1, 0)})
                queue.append({'position': (r, c), 'direction': (-1, 0)})
                break
            elif cell == '-' and dr != 0:
                queue.append({'position': (r, c), 'direction': (0, 1)})
                queue.append({'position': (r, c), 'direction': (0, -1)})
                break

    return sum(sum(row) for row in map)


if __name__ == "__main__":
    matrix = read_input("input.txt")

    rows, cols = len(matrix), len(matrix[0])
    result = 0

    # Corners
    corners = [
        ((0, 0), (0, 1)), ((0, 0), (1, 0)),
        ((0, cols - 1), (0, -1)), ((0, cols - 1), (1, 0)),
        ((rows - 1, 0), (0, 1)), ((rows - 1, 0), (-1, 0)),
        ((rows - 1, cols - 1), (0, -1)), ((rows - 1, cols - 1), (-1, 0))
    ]
    for pos, dir in corners:
        beam = {'position': pos, 'direction': dir}
        result = max(result, propagate_beam(matrix, beam))

    # Borders
    for col in range(cols):
        top_beam = {'position': (0, col), 'direction': (1, 0)}
        bottom_beam = {'position': (rows - 1, col), 'direction': (-1, 0)}
        result = max(result, propagate_beam(matrix, top_beam), propagate_beam(matrix, bottom_beam))

    for row in range(rows):
        left_beam = {'position': (row, 0), 'direction': (-1, 0)}
        right_beam = {'position': (row, cols - 1), 'direction': (0, -1)}
        result = max(result, propagate_beam(matrix, left_beam), propagate_beam(matrix, right_beam))

    print(f"Part 2: {result}")
