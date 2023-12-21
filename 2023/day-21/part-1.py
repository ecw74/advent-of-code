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


if __name__ == '__main__':
    grid = read_grid_from_file("input.txt")
    start_position = find_start_position(grid)
    visited = bfs_elf_map(grid, start_position, 64)
    print(f"Part 1: {visited}")
