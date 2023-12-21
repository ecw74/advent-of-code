from collections import deque
from typing import List, Optional, Tuple


def read_grid_from_file(file_path: str) -> List[List[str]]:
    """
    Read a grid from a text file and return it as a list of lists.

    :param file_path: str - The path to the text file containing the grid.
    :return: List[List[str]] - 2D grid representing the map.
    """
    grid = []
    with open(file_path, 'r') as file:
        for line in file:
            # Strip newline characters and convert line to list
            grid.append(list(line.strip()))
    return grid


def print_grid(grid: List[List[str]]) -> None:
    """
    Print the grid in a readable format.

    :param grid: List[List[str]] - 2D grid to be printed.
    """
    for row in grid:
        print("".join(row))


def find_start_position(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """
    Find the starting position of the Elf in the grid.

    :param grid: List[List[str]] - 2D grid representing the map.
    :return: Tuple[int, int] - The coordinates of the starting position, or None if not found.
    """
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                return i, j
    return None


def bfs_elf_map(grid: List[List[str]], start: Tuple[int, int], max_steps: int) -> int:
    """
    Perform a BFS to find all unique garden plots the elf can reach in a specified number of steps
    from the start position, avoiding rocks marked as '#'. The elf can step on garden plots ('.')
    and the starting position ('S').

    This function returns the count of unique garden plots reachable in exactly the specified
    number of steps.

    :param grid: List[List[str]] - 2D grid representing the map.
    :param start: Tuple[int, int] - The starting position of the Elf.
    :param max_steps: int - The maximum number of steps the Elf can take.
    :return: int - The count of unique garden plots reachable in exactly max_steps.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # North, South, East, West
    visited = set()

    queue = deque()
    queue.append(start)
    for step in range(1, max_steps + 1):
        visited.clear()
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if grid[nx % rows][ny % cols] != '#':
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
        queue = deque(visited)
    return len(visited)


def estimate_reachable_plots(grid: List[List[str]], start_position: Tuple[int, int], total_steps: int) -> int:
    """
    Estimate the number of unique garden plots reachable in a given number of steps
    in an infinitely repeating grid. The estimation is based on a quadratic equation
    derived from smaller, more manageable step sizes.

    :param grid: List[List[str]] - 2D grid representing the map.
    :param start_position: Tuple[int, int] - The starting position of the Elf.
    :param total_steps: int - The total number of steps to estimate for.
    :return: int - Estimated number of unique garden plots reachable.
    """
    rows, cols = len(grid), len(grid[0])
    # Calculate reachable plots for modulated step sizes
    v1 = bfs_elf_map(grid, start_position, total_steps % cols)
    v2 = bfs_elf_map(grid, start_position, total_steps % cols + cols)
    v3 = bfs_elf_map(grid, start_position, total_steps % cols + 2 * cols)

    # Derive coefficients for the quadratic equation
    a = (v1 - 2 * v2 + v3) / 2
    b = (-3 * v1 + 4 * v2 - v3) / 2
    c = v1

    # Calculate the estimated number of plots for the large step count
    n = total_steps // cols

    return int(a * n * n + b * n + c)


if __name__ == '__main__':
    grid = read_grid_from_file("input.txt")
    start_position = find_start_position(grid)
    result = estimate_reachable_plots(grid, start_position, 26501365)
    print(f"Part 1: {result}")
