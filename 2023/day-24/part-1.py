import itertools


def read_data(filename):
    """
    Reads the hailstone data from a file and returns a list of tuples.

    Each tuple contains position and velocity information in the format:
    (px, py, pz, vx, vy, vz)

    :param filename: str, name of the file containing the data
    :return: list of tuples
    """
    hailstones = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split('@')
            position = tuple(map(int, parts[0].split(',')))
            velocity = tuple(map(int, parts[1].split(',')))
            hailstones.append(position + velocity)
    return hailstones


def line_intersection(start1, vel1, start2, vel2):
    """
    Calculate the intersection point of two lines.

    Each line is defined by a start point and a velocity vector.

    Args:
    start1: The x, y start coordinates of the first line.
    vel1: The x, y velocity of the first line.
    start2: The x, y start coordinates of the second line.
    vel2: The x, y velocity of the second line.

    Returns:
    The intersection point (x, y) if it exists, otherwise None.
    """
    x1, y1 = start1
    vx1, vy1 = vel1
    x2, y2 = start2
    vx2, vy2 = vel2

    # Solving the equations:
    # x1 + t1 * vx1 = x2 + t2 * vx2
    # y1 + t1 * vy1 = y2 + t2 * vy2
    # for t1 and t2
    det = vx1 * vy2 - vy1 * vx2
    if det == 0:
        return None  # Lines are parallel or coincident

    t1 = ((x2 - x1) * vy2 + (y1 - y2) * vx2) / det
    # We can find the intersection point using either line's equation
    intersection_x = x1 + t1 * vx1
    intersection_y = y1 + t1 * vy1

    return (intersection_x, intersection_y)


def count_intersections(hailstones, x_bounds, y_bounds):
    """
    Counts the number of intersections within the specified bounds.

    :param hailstones: list of tuples, containing position and velocity data
    :param x_bounds: tuple, (min_x, max_x) for the test area
    :param y_bounds: tuple, (min_y, max_y) for the test area
    :return: int, count of intersections within the test area
    """
    intersections = 0
    for (h1, h2) in itertools.combinations(hailstones, 2):
        px1, py1, _, vx1, vy1, _ = h1
        px2, py2, _, vx2, vy2, _ = h2

        intersection = line_intersection((px1, py1), (vx1, vy1), (px2, py2), (vx2, vy2))

        if intersection is None:
            continue

        x, y = intersection

        dx = x - px1
        dy = y - py1
        if not ((dx > 0) == (vx1 > 0) and (dy > 0) == (vy1 > 0)):
            continue

        dx = x - px2
        dy = y - py2
        if not ((dx > 0) == (vx2 > 0) and (dy > 0) == (vy2 > 0)):
            continue

        if x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]:
            intersections += 1

    return intersections


def main():
    hailstones = read_data("input.txt")
    x_bounds = (200000000000000, 400000000000000)
    y_bounds = (200000000000000, 400000000000000)
    result = count_intersections(hailstones, x_bounds, y_bounds)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
