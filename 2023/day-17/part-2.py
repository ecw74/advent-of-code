import heapq


def read_map(filename):
    """
    Reads the map from a file and converts it into a 2D list of integers.

    :param filename: Name of the file containing the map.
    :return: 2D list representing the heat loss values of each block.

    >>> map_data = read_map("test.txt")
    >>> expected_map_data=[[2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
    ...                    [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
    ...                    [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
    ...                    [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
    ...                    [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
    ...                    [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
    ...                    [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
    ...                    [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
    ...                    [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
    ...                    [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
    ...                    [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
    ...                    [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
    ...                    [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3]]
    >>> expected_map_data == map_data
    True
    """
    with open(filename, 'r') as file:
        return [[int(char) for char in line.strip()] for line in file]


def calculate_cost_for_next_steps(r, c, direction, steps_required, map_data):
    """
    Calculates the cost for the next specified number of steps in the given direction.

    :param r: Current row.
    :param c: Current column.
    :param direction: Current direction ('U', 'D', 'L', 'R').
    :param steps_required: Number of steps to look ahead.
    :param map_data: 2D list representing the heat loss values of each block.
    :return: Total cost for the next steps or infinity if it crosses the border.

    >>> map_data=[[2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
    ...           [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
    ...           [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
    ...           [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
    ...           [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
    ...           [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
    ...           [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
    ...           [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
    ...           [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
    ...           [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
    ...           [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
    ...           [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
    ...           [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3]]
    >>> rows, cols = len(map_data), len(map_data[0])
    >>> calculate_cost_for_next_steps(0, 0, 'R', 1, map_data)
    4
    >>> calculate_cost_for_next_steps(0, 0, 'D', 4, map_data)
    13
    >>> calculate_cost_for_next_steps(rows-3, cols-3, 'R', 4, map_data)  # Crosses border
    inf
    """
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    dr, dc = directions[direction]
    cost = 0
    for _ in range(steps_required):
        r, c = r + dr, c + dc
        if not (0 <= r < len(map_data) and 0 <= c < len(map_data[0])):
            return float('inf')  # Crosses border, high cost
        cost += map_data[r][c]
    return cost


def get_neighbors(r, c, direction, steps, map_data, min_step, max_step):
    """
    Yields potential next steps from the current position and direction.

    :param r: Current row.
    :param c: Current column.
    :param direction: Current direction ('U', 'D', 'L', 'R').
    :param steps: Current number of steps in the given direction.
    :param map_data: 2D list representing the heat loss values of each block.
    :param min_step: Minimum consecutive steps before turning.
    :param max_step: Maximum consecutive steps allowed in one direction.
    :return: Yields tuples representing possible next steps.



    >>> map_data=[[2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
    ...           [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
    ...           [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
    ...           [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
    ...           [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
    ...           [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
    ...           [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
    ...           [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
    ...           [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
    ...           [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
    ...           [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
    ...           [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
    ...           [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3]]
    >>> rows, cols = len(map_data), len(map_data[0])
    >>> list(get_neighbors(0, 0, 'R', 1, map_data, 1, 3))
    [(0, 1, 'R', 2, 4), (1, 0, 'D', 1, 3)]
    >>> list(get_neighbors(0, cols - 3, 'R', 10, map_data, 4, 10))
    [(4, 10, 'D', 4, 17)]
    """
    directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    turns = {'U': ['L', 'R'], 'D': ['L', 'R'], 'L': ['U', 'D'], 'R': ['U', 'D']}

    rows, cols = len(map_data), len(map_data[0])

    # Continue in the same direction if steps are less than 3
    if steps < max_step:
        dr, dc = directions[direction]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            next_cost = map_data[nr][nc]
            yield nr, nc, direction, steps + 1, next_cost

    for d in turns[direction]:
        dr, dc = directions[d]
        nr, nc = r + min_step * dr, c + min_step * dc
        if 0 <= nr < rows and 0 <= nc < cols:
            next_cost = calculate_cost_for_next_steps(r, c, d, min_step, map_data)
            yield nr, nc, d, min_step, next_cost


def min_heat_loss(map_data, min_step, max_step):
    """
    Computes the minimum heat loss using djikstar.

    :param map_data: 2D list representing the heat loss values of each block.
    :param min_step: Minimum required step size after turn.
    :param min_step: Maximum allowed steps heading in on direction.
    :return: Minimum heat loss value.

    >>> map_data=[[2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
    ...           [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
    ...           [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
    ...           [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
    ...           [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
    ...           [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
    ...           [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
    ...           [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
    ...           [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
    ...           [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
    ...           [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
    ...           [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
    ...           [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3]]
    >>> min_heat_loss(map_data, 1, 3)
    102
    >>> min_heat_loss(map_data, 4, 10)
    94
    """
    rows, cols = len(map_data), len(map_data[0])
    start = (0, 0, 'R', 0)  # Start at (0,0) facing right with 0 steps
    end = (rows - 1, cols - 1)
    queue = [(0, start)]
    visited = set()

    while queue:
        cost, (r, c, direction, steps) = heapq.heappop(queue)
        if (r, c) == end:
            return cost
        if (r, c, direction, steps) in visited:
            continue
        visited.add((r, c, direction, steps))

        for nr, nc, nd, nsteps, ncosts in get_neighbors(r, c, direction, steps, map_data, min_step, max_step):
            if (nr, nc, nd, nsteps) not in visited:
                new_cost = cost + ncosts
                heapq.heappush(queue, (new_cost, (nr, nc, nd, nsteps)))

    return float('inf')


if __name__ == "__main__":
    map_data = read_map("input.txt")
    result = min_heat_loss(map_data, 4, 10)
    print(f"Part 2: {result}")
