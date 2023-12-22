import sys


def read_map(filename):
    """
    Reads the hiking trail map from a file and returns it as a list of lists.

    :param filename: The name of the file containing the map.
    :return: A list of lists representing the map.
    """
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


def is_valid_move(map, x, y, destination):
    rows, cols = len(map), len(map[0])
    if 0 <= x < rows and 0 <= y < cols:
        if map[x][y] == '.' and (x, y) == destination:
            return "destination"  # Special case for destination
        return map[x][y] not in ['#', 'X']
    return False


def dfs(map, x, y, destination, is_start=False):
    max_length = 0
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1), '.': [(1, 0), (0, 1), (-1, 0), (0, -1)]}

    if not is_start:
        if map[x][y] == '.':
            for dx, dy in directions['.']:
                next_x, next_y = x + dx, y + dy
                valid_move = is_valid_move(map, next_x, next_y, destination)
                if valid_move == "destination":
                    return 1  # Found the destination, return the length of this path
                elif valid_move:
                    temp, map[x][y] = map[x][y], 'X'
                    length = 1 + dfs(map, next_x, next_y, destination)
                    max_length = max(max_length, length)
                    map[x][y] = temp  # Backtrack
        elif map[x][y] in directions:
            dx, dy = directions[map[x][y]]
            next_x, next_y = x + dx, y + dy
            valid_move = is_valid_move(map, next_x, next_y, destination)
            if valid_move == "destination":
                return 1
            elif valid_move:
                temp, map[x][y] = map[x][y], 'X'
                length = 1 + dfs(map, next_x, next_y, destination)
                max_length = max(max_length, length)
                map[x][y] = temp  # Backtrack
    else:
        for dx, dy in directions['.']:
            next_x, next_y = x + dx, y + dy
            valid_move = is_valid_move(map, next_x, next_y, destination)
            if valid_move == "destination":
                return 1
            elif valid_move:
                temp, map[x][y] = map[x][y], 'X'
                length = 1 + dfs(map, next_x, next_y, destination)
                max_length = max(max_length, length)
                map[x][y] = temp  # Backtrack

    return max_length


def find_longest_hike(map):
    """
    Finds the length of the longest hike through the hiking trails.

    :param map: The hiking trail map.
    :return: Length of the longest hike.
    """
    start_x, start_y = next((x, y) for x in range(len(map)) for y in range(len(map[0])) if map[x][y] == '.')
    destination = next((x, y) for x in range(len(map) - 1, -1, -1) for y in range(len(map[0]) - 1, -1, -1) if
                       map[x][y] == '.' and (x, y) != (start_x, start_y))
    return dfs(map, start_x, start_y, destination, is_start=True)


def main():
    sys.setrecursionlimit(10000)
    map = read_map("input.txt")
    result = find_longest_hike(map)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
