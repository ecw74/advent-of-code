def parse_game_data(game_data):
    """
    Parses a list of game data strings into a structured format.

    Each string in the list represents a card with winning numbers and the numbers you have,
    separated by a vertical bar (|). The string may start with non-numeric text like 'Card 1:'.

    Args:
    game_data (list): List of strings with each string representing a card's data.

    Returns:
    list of tuples: Each tuple contains two lists, the first with winning numbers and the second with the numbers you have.

    >>> parse_game_data([
    ...     "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    ...     "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    ...     "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    ...     "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    ...     "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    ...     "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    ... ]) == [
    ...     ([41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53]),
    ...     ([13, 32, 20, 16, 61], [61, 30, 68, 82, 17, 32, 24, 19]),
    ...     ([1, 21, 53, 59, 44], [69, 82, 63, 72, 16, 21, 14, 1]),
    ...     ([41, 92, 73, 84, 69], [59, 84, 76, 51, 58, 5, 54, 83]),
    ...     ([87, 83, 26, 28, 32], [88, 30, 70, 12, 93, 22, 82, 36]),
    ...     ([31, 18, 13, 56, 72], [74, 77, 10, 23, 35, 67, 36, 11])
    ... ]
    True
    """
    cards = []
    for line in game_data:
        # Extract only the part after the colon
        line = line.split(':', 1)[-1]
        winning_numbers, your_numbers = line.split('|')
        winning_numbers = [int(num) for num in winning_numbers.split()]
        your_numbers = [int(num) for num in your_numbers.split()]
        cards.append((winning_numbers, your_numbers))
    return cards


def calculate_points(winning_numbers, your_numbers):
    """
    Calculates the points of a card based on the matching numbers.

    The first match makes the card worth one point and each match after the first doubles the point value.

    Args:
    winning_numbers (list): List of winning numbers for the card.
    your_numbers (list): List of numbers you have for the card.

    Returns:
    int: The point value of the card.

    Example:
    >>> calculate_points([41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53])
    8
    >>> calculate_points([13, 32, 20, 16, 61], [61, 30, 68, 82, 17, 32, 24, 19])
    2
    >>> calculate_points([1, 21, 53, 59, 44], [69, 82, 63, 72, 16, 21, 14, 1])
    2
    >>> calculate_points([41, 92, 73, 84, 69], [59, 84, 76, 51, 58, 5, 54, 83])
    1
    >>> calculate_points([87, 83, 26, 28, 32], [88, 30, 70, 12, 93, 22, 82, 36])
    0
    >>> calculate_points([31, 18, 13, 56, 72], [74, 77, 10, 23, 35, 67, 36, 11])
    0
    """
    matches = set(winning_numbers) & set(your_numbers)
    if not matches:
        return 0
    return 2 ** (len(matches) - 1)


def read_game_data_from_file(file_path):
    """
    Reads game data from a specified text file and parses it into a structured format.

    Args:
    file_path (str): Path to the text file containing the game data.

    Returns:
    list of tuples: Each tuple contains two lists, the first with winning numbers and the second with the numbers you have.

    The function assumes that each line in the file corresponds to a card's data.
    """
    with open(file_path, 'r') as file:
        game_data = file.readlines()
    return game_data


# To run the doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    card_data = read_game_data_from_file("input.txt")
    cards = parse_game_data(card_data)
    total_points = sum(calculate_points(winning, your) for winning, your in cards)
    print(f"Part 1: {total_points}")
