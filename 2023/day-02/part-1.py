def parse_game_data_line(line):
    """
    Parses a single line of game data.

    The line format is expected to be a game ID followed by a semicolon-separated list of cube counts.

    Args:
    line (str): A line from the file containing the game data.

    Returns:
    tuple: A tuple where the first element is the game ID and the second is a list of dictionaries with cube counts.

    Example:
    >>> parse_game_data_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    (1, [{'blue': 3, 'red': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'green': 2}])
    """
    parts = line.strip().split(': ')
    game_id = int(parts[0].split()[1])
    subsets = parts[1].split('; ')
    cube_counts = []
    for subset in subsets:
        counts = {}
        cubes = subset.split(', ')
        for cube in cubes:
            count, color = cube.split()
            counts[color] = int(count)
        cube_counts.append(counts)
    return game_id, cube_counts


def parse_game_data(file_path):
    games = {}
    with open(file_path, 'r') as file:
        for line in file:
            game_id, cube_counts = parse_game_data_line(line)
            games[game_id] = cube_counts
    return games


def is_game_possible(game_data, red_cubes, green_cubes, blue_cubes):
    """
    Determines if a game is possible given the constraints of cube counts.

    Args:
    game_data (list): A list of dictionaries with cube counts for each subset in a game.
    red_cubes (int): The maximum number of red cubes available.
    green_cubes (int): The maximum number of green cubes available.
    blue_cubes (int): The maximum number of blue cubes available.

    Returns:
    bool: True if the game is possible, False otherwise.
    """
    for subset in game_data:
        if subset.get('red', 0) > red_cubes or subset.get('green', 0) > green_cubes or subset.get('blue',
                                                                                                  0) > blue_cubes:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    file_path = "input.txt"  # Replace with the path to your input file
    games = parse_game_data(file_path)
    possible_games = [game_id for game_id, data in games.items() if is_game_possible(data, 12, 13, 14)]
    print(f"Part 1: {sum(possible_games)}")
