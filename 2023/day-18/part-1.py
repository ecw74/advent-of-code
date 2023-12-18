import numpy as np


def read_instructions(file_path):
    """
    Reads and parses the instructions from the file.

    :param file_path: Path to the file containing the dig plan.
    :return: A list of tuples with direction and magnitude.
    """
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            direction = parts[0]
            magnitude = int(parts[1])
            instructions.append((direction, magnitude))
    return instructions


def create_polygon(instructions):
    """
    Creates a polygon from a list of instructions provided as tuples.

    Each tuple consists of a direction ('R', 'L', 'U', 'D') and an integer indicating the steps.

    Parameters:
    instructions (List[Tuple[str, int]]): A list of tuples with instructions.

    Returns:
    List[Tuple[int, int]]: A list of tuples representing the vertices of the polygon.
    """
    # Starting point
    x = np.uint64(0)
    y = np.uint64(0)

    # List to store the vertices of the polygon
    vertices = [(x, y)]

    # Process each instruction
    for direction, steps in instructions:

        if direction == 'R':
            x += steps
        elif direction == 'L':
            x -= steps
        elif direction == 'U':
            y += steps
        elif direction == 'D':
            y -= steps

        vertices.append((x, y))

    return vertices


def calculate_polygon_area(vertices):
    """
    Calculates the area of a polygon using the shoelace formula.

    Parameters:
    vertices (List[Tuple[int, int]]): A list of tuples representing the vertices of the polygon.

    Returns:
    float: The area of the polygon.
    """

    # Calculate area using the shoelace formula
    shoelace_area = np.uint64(0)
    for i in range(len(vertices) - 1):
        x0, y0 = vertices[i]
        x1, y1 = vertices[i + 1]
        border_length = max(abs(x1 - x0), abs(y1 - y0))
        shoelace_area += (x0 * y1) - (y0 * x1)
        shoelace_area -= border_length

    return abs(shoelace_area) / 2 + 1


if __name__ == "__main__":
    instructions = read_instructions("input.txt")
    vertices = create_polygon(instructions)
    polygon_area = np.uint64(calculate_polygon_area(vertices))
    print(f"Part 1: {polygon_area}")
