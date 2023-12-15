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

def hash_algorithm(label: str) -> int:
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
    for char in label:
        ascii_code = ord(char)
        current_value = (current_value + ascii_code) * 17 % 256
    return current_value

def process_step(boxes, step: str):
    """
    Processes a single step and updates the boxes accordingly.

    Args:
    boxes (list): The current state of the boxes.
    step (str): The step to process.

    The step format is 'label=operation' or 'label-', where 'label' is the lens label
    and 'operation' is either a focal length (number) or '-' for removal.

    Examples:
    >>> boxes = [[] for _ in range(256)]
    >>> process_step(boxes, "rn=1")
    >>> boxes[0]
    [('rn', 1)]

    >>> process_step(boxes, "cm-")
    >>> boxes[0]
    [('rn', 1)]

    >>> process_step(boxes, "qp=3")
    >>> boxes[1]
    [('qp', 3)]

    >>> process_step(boxes, "cm=2")
    >>> boxes[0]
    [('rn', 1), ('cm', 2)]

    >>> process_step(boxes, "qp-")
    >>> boxes[1]
    []
    """
    label, operation = step.split('=' if '=' in step else '-')
    box_index = hash_algorithm(label)
    if operation == '':
        # Remove the lens if present
        boxes[box_index] = [lens for lens in boxes[box_index] if lens[0] != label]
    else:
        # Insert or replace the lens
        focal_length = int(operation)
        for i, (lens_label, _) in enumerate(boxes[box_index]):
            if lens_label == label:
                boxes[box_index][i] = (label, focal_length)
                break
        else:
            boxes[box_index].append((label, focal_length))

def process_initialization_sequence(sequence: list) -> list:
    """
    Processes the entire initialization sequence, updating the boxes accordingly.

    Args:
    sequence (list): A list of strings, each representing a step in the sequence.

    Returns:
    list: The state of all 256 boxes after processing the sequence.

    Example:
    >>> sequence = ["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]
    >>> boxes = process_initialization_sequence(sequence)
    >>> [box for box in boxes if box]  # Only display non-empty boxes for brevity
    [[('rn', 1), ('cm', 2)], [('ot', 7), ('ab', 5), ('pc', 6)]]
    """
    boxes = [[] for _ in range(256)]
    for step in sequence:
        process_step(boxes, step)
    return boxes

def calculate_focusing_power(boxes: list) -> int:
    """
    Calculates the total focusing power of all lenses in the boxes.

    Args:
    boxes (list): The state of all 256 boxes.

    Returns:
    int: The total focusing power.

    Example:
    >>> boxes = [[('rn', 1), ('cm', 2)], [], [], [('ot', 7), ('ab', 5), ('pc', 6)]]
    >>> calculate_focusing_power(boxes)
    145
    """
    total_power = 0
    for box_index, box in enumerate(boxes):
        for slot_index, (_, focal_length) in enumerate(box, start=1):
            total_power += (1 + box_index) * slot_index * focal_length
    return total_power

if __name__ == "__main__":
    file_path = "input.txt"  # Replace with your file path
    sequence = read_sequence_from_file(file_path)
    boxes = process_initialization_sequence(sequence)
    power = calculate_focusing_power(boxes)
    print(f"Part 2: {power}")
