import re
from typing import Dict, List


def parse_game_data(input_str: str) -> Dict[str, List[Dict[str, int]]]:
    """
    Parses a string containing game data and returns a dictionary with game IDs as keys
    and a list of dictionaries representing the count of colors in each segment.

    Args:
    input_str (str): A string containing game data in a specific format.

    Returns:
    Dict[str, List[Dict[str, int]]]: A dictionary where each key is a game ID and the value
                                     is a list of dictionaries with color counts.

    Examples:
    >>> parse_game_data("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    {'1': [{'red': 4, 'green': 0, 'blue': 3}, {'red': 1, 'green': 2, 'blue': 6}, {'red': 0, 'green': 2, 'blue': 0}]}

    >>> parse_game_data("Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue")
    {'2': [{'red': 0, 'green': 2, 'blue': 1}, {'red': 1, 'green': 3, 'blue': 4}, {'red': 0, 'green': 1, 'blue': 1}]}

    >>> parse_game_data("Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red")
    {'3': [{'red': 20, 'green': 8, 'blue': 6}, {'red': 4, 'green': 13, 'blue': 5}, {'red': 1, 'green': 5, 'blue': 0}]}

    >>> parse_game_data("Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red")
    {'4': [{'red': 3, 'green': 1, 'blue': 6}, {'red': 6, 'green': 3, 'blue': 0}, {'red': 14, 'green': 3, 'blue': 15}]}

    >>> parse_game_data("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
    {'5': [{'red': 6, 'green': 3, 'blue': 1}, {'red': 1, 'green': 2, 'blue': 2}]}
    """
    # Regular expression to find game ID and color counts
    game_pattern = r"Game (\d+): (.+)"
    color_pattern = r"(\d+) (red|green|blue)"

    # Find all games
    games = re.findall(game_pattern, input_str)

    # Initialize result dictionary
    result = {}

    # Process each game
    for game_id, game_data in games:
        # Split the game data into segments
        segments = game_data.split(';')
        segment_list = []

        # Process each segment
        for segment in segments:
            # Find all color counts in the segment
            colors = re.findall(color_pattern, segment)
            color_dict = {'red': 0, 'green': 0, 'blue': 0}

            # Update color dictionary with counts
            for count, color in colors:
                color_dict[color] += int(count)

            segment_list.append(color_dict)

        # Add the processed segments to the result
        result[game_id] = segment_list

    return result


def find_minimum_elements(games: List[Dict[str, List[Dict[str, int]]]]) -> Dict[str, Dict[str, int]]:
    """
    Iterates over a list of games and finds the minimum number of red, green, and blue elements required for each game.
    The minimum number is defined as the maximum number of each color required at any stage of the game.

    :param games: List of dictionaries containing game IDs and lists of color counts.
    :return: Dictionary with game IDs and the minimum number of red, green, and blue elements required.

    >>> games_example = [
    ...  {'1': [{'red': 4, 'green': 0, 'blue': 4}, {'red': 1, 'green': 2, 'blue': 6}, {'red': 0, 'green': 2, 'blue': 0}]},
    ...  {'2': [{'red': 0, 'green': 2, 'blue': 1}, {'red': 1, 'green': 3, 'blue': 4}, {'red': 0, 'green': 1, 'blue': 1}]},
    ...  {'3': [{'red': 20, 'green': 8, 'blue': 6}, {'red': 4, 'green': 13, 'blue': 5}, {'red': 1, 'green': 5, 'blue': 0}]},
    ...  {'4': [{'red': 3, 'green': 1, 'blue': 6}, {'red': 6, 'green': 3, 'blue': 0}, {'red': 14, 'green': 3, 'blue': 15}]},
    ...  {'5': [{'red': 6, 'green': 3, 'blue': 1}, {'red': 1, 'green': 2, 'blue': 2}]}
    ... ]
    >>> find_minimum_elements(games_example)
    {'1': {'red': 4, 'green': 2, 'blue': 6}, '2': {'red': 1, 'green': 3, 'blue': 4}, '3': {'red': 20, 'green': 13, 'blue': 6}, '4': {'red': 14, 'green': 3, 'blue': 15}, '5': {'red': 6, 'green': 3, 'blue': 2}}
    """
    min_elements = {}

    for game in games:
        for game_id, color_counts in game.items():
            # Initialize minimum values for each color
            min_red = min_green = min_blue = 0

            # Find the maximum required for each color in all stages
            for stage in color_counts:
                min_red = max(min_red, stage['red'])
                min_green = max(min_green, stage['green'])
                min_blue = max(min_blue, stage['blue'])

            # Update the dictionary with the minimum required for each color
            min_elements[game_id] = {'red': min_red, 'green': min_green, 'blue': min_blue}

    return min_elements


def extract_games_from_file(file_path: str) -> List[List[int]]:
    """
    Reads a text file line by line and extracts all numbers from each line.

    :param file_path: Path to the text file.
    :return: A list of lists, where each inner list contains the numbers found in a corresponding line of the file.
    """
    game_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            game_lines.append(parse_game_data(line))
    return game_lines


def multiply_color_values(games: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Iterates over a dictionary of games and multiplies the values of red, green, and blue for each game.
    Returns a new dictionary with the game ID and the product of these values.

    :param games: Dictionary with game IDs and color values.
    :return: Dictionary with game IDs and the product of the color values.

    >>> games_example = {
    ...     '1': {'red': 4, 'green': 2, 'blue': 6},
    ...     '2': {'red': 1, 'green': 3, 'blue': 4},
    ...     '3': {'red': 20, 'green': 13, 'blue': 6},
    ...     '4': {'red': 14, 'green': 3, 'blue': 15},
    ...     '5': {'red': 6, 'green': 3, 'blue': 2}
    ... }
    >>> multiply_color_values(games_example)
    {'1': 48, '2': 12, '3': 1560, '4': 630, '5': 36}
    """
    result = {}

    for game_id, colors in games.items():
        product = colors['red'] * colors['green'] * colors['blue']
        result[game_id] = product

    return result


# To run the doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    games = extract_games_from_file("input.txt")
    minimum_elements = find_minimum_elements(games)
    multiplied_color_values = multiply_color_values(minimum_elements)
    sum_value = sum(values for values in multiplied_color_values.values())
    print(f"Part 2 {sum_value}")
