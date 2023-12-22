from collections import deque


def read_map(filename):
    """
    Reads the hiking trail map from a file and returns it as a list of lists.

    :param filename: The name of the file containing the map.
    :return: A list of lists representing the map.
    """
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file.readlines()]


def create_map_point_set(map):
    """
    Extracts and creates a set of points from a 2D map array based on specific characters.

    This function processes a two-dimensional map array, identifying points that contain certain
    characters and adding their coordinates to a set. The characters used for selection represent
    specific features or properties in the map, such as navigable or notable locations.

    Parameters:
    - map (list of lists): A two-dimensional array representing the map. Each element in the array
                           is a character, with the map organized into rows and columns.

    Returns:
    - set of tuples: A set containing the coordinates (x, y) of points in the map that contain one
                     of the specified characters (".", "<", "^", "v", ">").

    Usage:
    - This function is useful for grid-based maps, particularly in applications like games, simulations,
      or pathfinding algorithms, where identifying specific types of points is crucial for further
      operations like movement, exploration, or analysis.
    """
    map_point_set = set()
    rows, cols = len(map), len(map[0])
    for x in range(rows):
        for y in range(cols):
            if map[x][y] in [".", "<", "^", "v", ">"]:
                map_point_set.add((x, y))
    return map_point_set


def create_junction_set(map_point_set):
    """
    Identify and create a list of junction points from a set of map points.

    This function processes a set of points, each representing a location in a map or network, and
    identifies which points qualify as junctions. A junction is defined as a point that has three or
    more neighboring points in the provided set.

    Parameters:
    - map_point_set (set of tuples): A set of tuples, where each tuple represents the coordinates (x, y) of a point.

    Returns:
    - list of tuples: A sorted list of points that qualify as junctions in the map. Each tuple in the list
                      represents the coordinates (x, y) of a junction.

    Note:
    - Neighboring points are determined by checking adjacent locations in four directions: up, down, left, and right.
    """
    junction_list = []
    for point in map_point_set:
        junction_count = 0
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = point[0] + dx, point[1] + dy
            if (nx, ny) in map_point_set:
                junction_count += 1
        if junction_count >= 3:
            junction_list.append(point)
    junction_list.sort()
    return junction_list


def bfs_junction(junction, junction_list, map_point_set, start, end, junction_neighbors, junction_distance):
    """
    Perform a breadth-first search (BFS) to map junctions and calculate distances in a network.

    This function traverses a network starting from a given junction, mapping the connections between
    junctions and calculating the distances to specified start and end points. It is particularly useful
    for creating or updating a graph of interconnected junctions based on their spatial relationships.

    Parameters:
    - junction (tuple): The starting junction coordinates (x, y) for the BFS.
    - junction_list (list of tuples): A list of all junctions in the network, each represented by coordinates (x, y).
    - map_point_set (set of tuples): A set containing all points in the network, including junctions and other points.
    - start (tuple): The coordinates (x, y) of the starting point for distance calculation.
    - end (tuple): The coordinates (x, y) of the ending point for distance calculation.
    - junction_neighbors (dict): A dictionary to be updated with neighbors for each junction. Keys are junction indices,
                                 and values are sets of indices of neighboring junctions.
    - junction_distance (dict): A dictionary to be updated with distances between junctions. Keys are tuples of junction
                                indices, and values are distances.

    Returns:
    - tuple: A tuple of two tuples: (start_junctions, end_junctions). Each sub-tuple contains the index of the junction in
             junction_list and the distance from the 'junction' parameter to the 'start' or 'end'.

    Note:
    - The function assumes a grid-like network where movement is possible in four directions: up, down, left, and right.
    - It's designed to avoid revisiting nodes, optimizing the exploration of the network.
    """
    visited_junctions = set()
    queue = deque()

    junction_idx = junction_list.index(junction)
    junction_set = set(junction_list)

    queue.append(((junction), 0))

    start_junctions = tuple()
    end_junctions = tuple()

    while queue:
        junction, distance = queue.popleft()
        if junction == start:
            start_junctions = (junction_idx, distance)
            continue
        elif junction == end:
            end_junctions = (junction_idx, distance)
            continue
        visited_junctions.add(junction)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = junction[0] + dx, junction[1] + dy
            if (nx, ny) in visited_junctions or (nx, ny) not in map_point_set:
                continue
            if (nx, ny) in junction_set:
                idx = junction_list.index((nx, ny))
                if junction_idx not in junction_neighbors:
                    junction_neighbors[junction_idx] = set()
                junction_neighbors[junction_idx].add(idx)
                junction_distance[(junction_idx, idx)] = distance + 1
                continue
            queue.append(((nx, ny), distance + 1))

    return start_junctions, end_junctions


def longest_junction_path(junction_distance, junction_neighbors, start_junction, end_junction):
    """
    Calculate the longest path between two junctions in a network.

    This function determines the longest path between a start junction and an end junction in a graph-like structure,
    taking into account additional distances from the actual start and end points to their respective junctions.

    Parameters:
    - junction_distance (dict): A dictionary where keys are tuples representing junction pairs (junction_a, junction_b),
                                and values are distances between these junctions.
    - junction_neighbors (dict): A dictionary where each key is a junction and its value is a list of neighboring junctions.
    - start_junction (tuple): A tuple (junction, distance) representing the starting junction and its distance
                              from the actual starting point.
    - end_junction (tuple): A tuple (junction, distance) representing the ending junction and its distance
                            from the actual ending point.

    Returns:
    - int: The length of the longest path from the actual start to the actual end, including the distances from
           start to start_junction and from end_junction to end.

    Note:
    - The function assumes that the graph does not contain cycles that would lead to infinitely long paths.
    - This function is designed for scenarios where the longest route is necessary, rather than the shortest path.
    """
    junction_queue = deque()
    junction_queue.append((tuple([start_junction[0]]), start_junction[1]))
    latest_distance = 0
    while junction_queue:
        junction_history_tuple, current_distance = junction_queue.popleft()
        current_junction = junction_history_tuple[-1]
        junction_history_list = list(junction_history_tuple)
        for g in junction_neighbors[current_junction]:
            if g in junction_history_tuple:
                continue
            dist = current_distance + junction_distance[(current_junction, g)]
            if g == end_junction[0]:
                latest_distance = max(latest_distance, dist)
                continue
            junction_history_list.append(g)
            junction_queue.append((tuple(junction_history_list), dist))
            junction_history_list.pop()
    return latest_distance + end_junction[1]


def find_longest_hike(map):
    """
    Finds the length of the longest hike through the hiking trails.

    :param map: The hiking trail map.
    :return: Length of the longest hike.
    """
    start_point = next((0, y) for y in range(len(map[0])) if map[0][y] == '.')
    target_point = next((len(map) - 1, y) for y in range(len(map[0])) if map[len(map) - 1][y] == '.')

    map_point_set = create_map_point_set(map)
    junction_list = create_junction_set(map_point_set)

    junction_neighbors = {}
    junction_distance = {}

    for j in junction_list:
        s, e = bfs_junction(j, junction_list, map_point_set, start_point, target_point, junction_neighbors,
                            junction_distance)
        if s:
            start_junction = s
        if e:
            end_junction = e

    return longest_junction_path(junction_distance, junction_neighbors, start_junction, end_junction)


def main():
    map = read_map("input.txt")
    result = find_longest_hike(map)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    main()
