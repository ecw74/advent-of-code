from typing import List

def read_sequence_from_file(file_path: str) -> list:
    """
    Reads the initialization sequence from a file and returns it as a list of strings.

    Args:
    file_path (str): The path to the file containing the sequence.

    Returns:
    list: A list of strings, each representing a step in the sequence.

    Example:
    >>> read_sequence_from_file("test.txt")
    ['rn=1', 'cm-', 'qp=3', 'cm=2', 'qp-', 'pc=4', 'ot=9', 'ab=5', 'pc-', 'pc=6', 'ot=7']
    """
    with open(file_path, 'r') as file:
        sequence = file.read().strip()
    return sequence.split(',')

def hash_algorithm(s: str) -> int:
    """
    Calculates the HASH of a given string according to the specified algorithm.

    Args:
    s (str): The input string.

    Returns:
    int: The HASH value of the string.

    Example:
    >>> hash_algorithm("rn=1")
    30
    >>> hash_algorithm("cm-")
    253
    """
    current_value = 0
    for char in s:
        ascii_code = ord(char)
        current_value = (current_value + ascii_code) * 17 % 256
    return current_value

def process_initialization_sequence(sequence: List[str]) -> int:
    """
    Processes the initialization sequence, applying the HASH algorithm to each step
    and summing the results.

    Args:
    sequence (str): The initialization sequence.

    Returns:
    int: The sum of HASH values for each step in the sequence.

    Example:
    >>> process_initialization_sequence(['rn=1', 'cm-', 'qp=3', 'cm=2', 'qp-', 'pc=4', 'ot=9', 'ab=5', 'pc-', 'pc=6', 'ot=7'])
    1320
    """
    return sum(hash_algorithm(step) for step in sequence)

if __name__ == "__main__":
    # Example initialization sequence
    sequence = read_sequence_from_file("input.txt")
    result = process_initialization_sequence(sequence)
    print(f"Part 2: {result}")
