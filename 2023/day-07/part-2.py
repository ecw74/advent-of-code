from typing import List

card_strength = {'A': 14, 'K': 13, 'Q': 12, 'T': 11, '9': 10, '8': 9, '7': 8, '6': 7, '5': 6, '4': 5, '3': 4, '2': 3, 'J': 1}


def preprocess_data(file_path):
    """
    Reads Camel Cards data from a file and preprocesses it for ranking and calculation.

    :param file_path: Path to the file containing the hands and bids.
    :return: Dictionary with hands as keys and bids as values.

    >>> preprocess_data('test.txt')
    {'32T3K': 765, 'T55J5': 684, 'KK677': 28, 'KTJJT': 220, 'QQQJA': 483}
    """
    result_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            result_dict[key] = int(value)
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


def determine_hand_type(hand):
    """
    Determines the type of a given hand of cards, considering Jokers.

    :param hand: String representing a hand of cards.
    :return: The type of the hand.

    >>> determine_hand_type("JJJJJ")
    'Five of a kind'
    >>> determine_hand_type("2J299")
    'Full house'
    """

    def count_hand(hand_counts):
        unique_counts = set(hand_counts.values())

        if 5 in unique_counts:
            return "Five of a kind"
        elif 4 in unique_counts:
            return "Four of a kind"
        elif 3 in unique_counts and 2 in unique_counts:
            return "Full house"
        elif 3 in unique_counts:
            return "Three of a kind"
        elif list(hand_counts.values()).count(2) == 2:
            return "Two pair"
        elif 2 in unique_counts:
            return "One pair"
        else:
            return "High card"

    # Special case: All Jokers
    if hand == "JJJJJ":
        return "Five of a kind"

    # Count the occurrences of each card excluding J
    counts = {}
    j_count = 0
    for card in hand:
        if card == 'J':
            j_count += 1
        else:
            counts[card] = counts.get(card, 0) + 1

    # If there are no J's, simply count the hand
    if j_count == 0:
        return count_hand(counts)

    # Try replacing J's with each card to find the best hand
    best_hand = "High card"
    for card in counts:
        temp_counts = counts.copy()
        temp_counts[card] += j_count
        hand_type = count_hand(temp_counts)
        if hand_type == "Five of a kind":
            return hand_type  # Can't do better than this
        if hand_type == "Four of a kind" and best_hand != "Five of a kind":
            best_hand = hand_type
        elif hand_type == "Full house" and best_hand not in ["Five of a kind", "Four of a kind"]:
            best_hand = hand_type
        elif hand_type == "Three of a kind" and best_hand not in ["Five of a kind", "Four of a kind", "Full house"]:
            best_hand = hand_type
        elif hand_type == "Two pair" and best_hand not in ["Five of a kind", "Four of a kind", "Full house", "Three of a kind"]:
            best_hand = hand_type
        elif hand_type == "One pair" and best_hand not in ["Five of a kind", "Four of a kind", "Full house", "Three of a kind", "Two pair"]:
            best_hand = hand_type

    # If no J's can improve the hand, count it as it is
    if best_hand == "High card":
        return count_hand(counts)
    else:
        return best_hand


def categorize_hands(card_hands):
    """
    Categorizes a list of card hands into different types.

    :param card_hands: List of strings where each string represents a hand of cards.
    :return: Dictionary categorizing each hand into one of the seven types.

    >>> categorize_hands(["JJJJJ", "2J299", "89JKK", "55J77", "QQQ2J", "8A383", "9A383", "23456"])
    {'Five of a kind': ['JJJJJ'], 'Four of a kind': ['QQQ2J'], 'Full house': ['2J299', '55J77'], 'Three of a kind': ['89JKK'], 'Two pair': ['8A383'], 'One pair': ['9A383'], 'High card': ['23456']}
    """
    categories = {
        "Five of a kind": [],
        "Four of a kind": [],
        "Full house": [],
        "Three of a kind": [],
        "Two pair": [],
        "One pair": [],
        "High card": []
    }

    for hand in card_hands:
        cat = determine_hand_type(hand)
        categories[cat].append(hand)
    return categories


def compare_hands(hand1: str, hand2: str) -> int:
    """
    Compares two hands of the same type, treating J as J for the purpose of breaking ties.

    :param hand1: First hand to compare.
    :param hand2: Second hand to compare.
    :return: -1 if hand1 is stronger, 1 if hand2 is stronger, 0 if equal.
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

    :param hands: List of hands to sort.
    :return: Sorted list of hands.
    """
    # Using the compare_hands function for custom sorting
    return sorted(hands, key=lambda x: [card_strength[c] for c in x])


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    categories = [
        "Five of a kind",
        "Four of a kind",
        "Full house",
        "Three of a kind",
        "Two pair",
        "One pair",
        "High card"
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

    print(f"Part 2: {total_winnings}")
