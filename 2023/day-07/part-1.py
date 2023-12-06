from collections import Counter

from typing import List

card_strength = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}


def preprocess_data(file_path):
    """
    Reads Camel Cards data from a file and preprocesses it for ranking and calculation.

    :param file_path: Path to the file containing the hands and bids.
    :return: List of tuples, each containing a hand and its corresponding bid.

    >>> data_dict = preprocess_data('test.txt')
    >>> data_dict
    {'32T3K': 765, 'T55J5': 684, 'KK677': 28, 'KTJJT': 220, 'QQQJA': 483}

    """
    result_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            result_dict[key] = int(value)
            # result_dict[sort_by_frequency_and_strength(key)] = int(value)

    return result_dict


def sort_by_frequency_and_strength(s):
    """
    Sorts the characters in a string based on their frequency and a predefined strength order.
    Characters with higher frequency come first. If frequencies are equal, characters are sorted
    by the strength order 'AKQJT98765432'.

    Args:
    s (str): The string to be sorted.

    Returns:
    str: The sorted string.

    Examples:
    >>> sort_by_frequency_and_strength("32T3K")
    '33KT2'
    >>> sort_by_frequency_and_strength("T55J5")
    '555JT'
    >>> sort_by_frequency_and_strength("KK677")
    'KK776'
    >>> sort_by_frequency_and_strength("KTJJT")
    'JJTTK'
    >>> sort_by_frequency_and_strength("QQQJA")
    'QQQAJ'
    """

    # Define the strength order
    strength_order = "AKQJT98765432"

    # Count the frequency of each character
    char_frequency = {}
    for char in s:
        if char in char_frequency:
            char_frequency[char] += 1
        else:
            char_frequency[char] = 1

    # Sort the characters first by frequency (descending) and then by strength
    sorted_chars = sorted(char_frequency.keys(), key=lambda x: (-char_frequency[x], strength_order.index(x)))

    # Build the final sorted string
    sorted_string = ''.join([char * char_frequency[char] for char in sorted_chars])

    return sorted_string


def categorize_hands(card_hands):
    """
    Categorize a list of card hands into different types.

    Args:
    card_hands (list): A list of strings where each string represents a hand of cards.

    Returns:
    dict: A dictionary categorizing each hand into one of the seven types.

    Example:
    >>> categorize_hands(["33KT2", "555JT", "KK776", "JJTTK", "QQQAJ"])
    {'Five of a Kind': [], 'Four of a Kind': [], 'Full House': [], 'Three of a Kind': ['555JT', 'QQQAJ'], 'Two Pair': ['KK776', 'JJTTK'], 'One Pair': ['33KT2'], 'High Card': []}
    """
    categories = {
        "Five of a Kind": [],
        "Four of a Kind": [],
        "Full House": [],
        "Three of a Kind": [],
        "Two Pair": [],
        "One Pair": [],
        "High Card": []
    }

    for hand in card_hands:
        counts = Counter(hand)
        count_values = list(counts.values())

        if 5 in count_values:
            categories["Five of a Kind"].append(hand)
        elif 4 in count_values:
            categories["Four of a Kind"].append(hand)
        elif sorted(count_values) == [2, 3]:
            categories["Full House"].append(hand)
        elif 3 in count_values:
            categories["Three of a Kind"].append(hand)
        elif count_values.count(2) == 2:
            categories["Two Pair"].append(hand)
        elif 2 in count_values:
            categories["One Pair"].append(hand)
        else:
            categories["High Card"].append(hand)

    return categories


def compare_hands(hand1: str, hand2: str) -> int:
    """
    Same compare_hands function as before, now using the global card_strength variable.
    """
    for card1, card2 in zip(hand1, hand2):
        if card_strength[card1] > card_strength[card2]:
            return -1
        elif card_strength[card1] < card_strength[card2]:
            return 1
    return 0


def sort_hands(hands: List[str]) -> List[str]:
    """
    Sorts a list of poker hands in descending order of their strength.
    """
    # Using the compare_hands function for custom sorting
    return sorted(hands, key=lambda x: [card_strength[c] for c in x])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    categories = [
        "Five of a Kind",
        "Four of a Kind",
        "Full House",
        "Three of a Kind",
        "Two Pair",
        "One Pair",
        "High Card"
    ]

    # Read and process the data
    input_data = preprocess_data('input.txt')

    # Categorize hands
    categorized_hands = categorize_hands(input_data.keys())

    # Sort and rank hands
    sorted_hands = []
    for category in reversed(categories):
        sorted_hands.extend(sort_hands(categorized_hands[category]))

    # Calculate total winnings
    total_winnings = sum((idx + 1) * input_data[hand] for idx, hand in enumerate(sorted_hands))

    print(f"Part 1: {total_winnings}")
