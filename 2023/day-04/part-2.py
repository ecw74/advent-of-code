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


# Redefine the process_scratchcards function
def process_scratchcards(cards_data):
    """
    Processes the original and copied scratchcards until no more scratchcards are won.

    Args:
    cards_data (list): List of tuples containing the winning numbers and the numbers you have for each card.

    Returns:
    int: Total number of scratchcards including the original set and all copies.

    The function processes the cards and their copies iteratively until no new copies are won.

    Example:
    >>> game_data = [
    ...     "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    ...     "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    ...     "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    ...     "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    ...     "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    ...     "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
    ... ]
    >>> cards = parse_game_data(game_data)
    >>> process_scratchcards(cards)
    30
    """
    copies = [1] * len(cards_data)
    i = 0
    while i < len(copies):
        if copies[i] > 0:
            winning, your = cards_data[i]
            matches = len(set(winning) & set(your))
            for j in range(i + 1, min(i + 1 + matches, len(copies))):
                copies[j] += copies[i]
        i += 1
    return sum(copies)


# To run the doctests
if __name__ == "__main__":
    import doctest

    doctest.testmod()

    card_data = read_game_data_from_file("input.txt")
    cards = parse_game_data(card_data)
    total_scratchcards = process_scratchcards(cards)
    print(f"Part 2: {total_scratchcards}")
