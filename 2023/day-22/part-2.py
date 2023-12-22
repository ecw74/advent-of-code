def read_input(file_path):
    """
    Reads the input from a file and parses it into a list of brick coordinates.

    :param file_path: Path to the input file.
    :return: A list of tuples, each representing a brick as ((x1, y1, z1), (x2, y2, z2)).

    Example usage:
    # Assuming 'input.txt' contains the appropriate data
    bricks = read_input("input.txt")
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    bricks = []
    bId = 0
    for line in lines:
        bId += 1
        points = line.strip().split("~")
        start = tuple(map(int, points[0].split(",")))
        end = tuple(map(int, points[1].split(",")))
        bricks.append((bId, start, end))
    return bricks


def create_empty_grid(bricks):
    """
    Creates an empty 3D grid with the maximum size required to place the bricks.

    :param bricks: A list of brick coordinates.
    :return: An empty 3D grid.
    """
    max_x = max(max(x1, x2) for _, (x1, _, _), (x2, _, _) in bricks)
    max_y = max(max(y1, y2) for _, (_, y1, _), (_, y2, _) in bricks)
    max_z = max(max(z1, z2) for _, (_, _, z1), (_, _, z2) in bricks)

    # Create an empty grid with dimensions (max_x + 1) x (max_y + 1) x (max_z + 1)
    return [[[False for _ in range(max_z + 1)] for _ in range(max_y + 1)] for _ in range(max_x + 1)]


def place_bricks(grid, bricks):
    """
    Places the bricks on the grid at their starting position and with the correct orientation.
    Each cell in the grid will contain the brick identifier (index in the bricks list) if occupied.

    :param grid: The 3D grid.
    :param bricks: A list of brick coordinates.
    :return: An updated grid with bricks placed.
    """
    for (brick_id, (x1, y1, z1), (x2, y2, z2)) in bricks:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    grid[x][y][z] = brick_id
    return grid


def shift_bricks_down(bricks, grid):
    """
    Shifts each brick down by 1 in the Z direction until encountering the ground or another brick.

    Args:
    bricks: A list of brick coordinates.
    grid: The 3D grid containing the bricks.

    Returns:
    Updated bricks coordinates and grid.
    """

    def can_move_down(brick):
        bId, (x1, y1, z1), (x2, y2, z2) = brick
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if z1 == z2:  # Horizontal brick
                    if z1 == 1 or grid[x][y][z1 - 1] is not False:
                        return False
                else:  # Vertical brick
                    lowest_z = min(z1, z2)
                    if lowest_z == 1 or grid[x][y][lowest_z - 1] is not False:
                        return False
        return True

    def update_grid(brick, add):
        brick_id, (x1, y1, z1), (x2, y2, z2) = brick
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    if add is True:
                        grid[x][y][z] = brick_id
                    else:
                        grid[x][y][z] = False

    for i, brick in enumerate(bricks):
        while can_move_down(brick):
            update_grid(brick, False)  # Remove brick from old position
            brick = (brick[0], (brick[1][0], brick[1][1], brick[1][2] - 1), (brick[2][0], brick[2][1], brick[2][2] - 1))
            update_grid(brick, True)  # Place brick in new position
        bricks[i] = brick

    return bricks, grid


def get_supports(bricks):
    """
    Calculate which bricks support and are supported by other bricks in a 3D space.

    Each brick is represented by an ID and two 3D coordinates defining its endpoints.
    The function returns two dictionaries:
        - supports: A dictionary mapping each brick ID to a list of IDs of bricks it supports.
        - supportedBy: A dictionary mapping each brick ID to a list of IDs of bricks supporting it.

    Args:
    bricks: List of bricks, each represented by an ID and two 3D coordinates.

    Returns:
    Two dictionaries containing the support relationships.
    """
    supports = {bId: [] for bId, _, _ in bricks}
    supportedBy = {bId: [] for bId, _, _ in bricks}

    settled = {}

    for bId, (x1, y1, z1), (x2, y2, z2) in bricks:
        supporters = set()

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1):
                    below = (x, y, z - 1)
                    if below in settled and settled[below] != bId:
                        supporters.add(settled[below])
                    settled[(x, y, z)] = bId

        for sId in supporters:
            supports[sId].append(bId)
            supportedBy[bId].append(sId)

    return supports, supportedBy


def count_chain_reaction(supports, supportedBy):
    """
    Counts the total number of bricks that would fall in a chain reaction when each brick in the structure is removed.

    Args:
    supports: A dictionary indicating which bricks each brick supports.
    supportedBy: A dictionary indicating which bricks support each brick.

    Returns:
    The total number of bricks that would fall in all simulated chain reactions.
    """
    count = 0
    for bId in supports:
        toCheck = supports[bId].copy()
        falling = {bId}

        while toCheck:
            curId = toCheck.pop(0)

            if all(sId in falling for sId in supportedBy[curId]):
                falling.add(curId)
                toCheck.extend(supports[curId])  # Using extend for efficiency

        count += len(falling) - 1

    return count


if __name__ == '__main__':
    bricks = read_input("input.txt")

    # sort bricks by z
    bricks.sort(key=lambda x: min(x[1][2], x[2][2]))

    empty_grid = create_empty_grid(bricks)
    placed_grid = place_bricks(empty_grid, bricks)
    shifted_bricks, shifted_grid = shift_bricks_down(bricks, placed_grid)
    supports, supportedBy = get_supports(shifted_bricks)
    count = count_chain_reaction(supports, supportedBy)
    print(f"Part 2: {count}")
