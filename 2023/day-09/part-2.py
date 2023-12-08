import doctest


def read_and_preprocess_data(file_path):
    """
    Reads data from a file and preprocesses it into a list of lists of integers.

    :param file_path: Path to the data file.
    :return: List of lists of integers.

    >>> read_and_preprocess_data('test.txt') # Assuming test.txt contains the provided example data
    [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append([int(x) for x in line.split()])
    return data


def extrapolate_previous_value(history):
    """
    Extrapolates the previous value of a given history sequence.

    :param history: List of integers representing the history.
    :return: The extrapolated previous value.

    >>> extrapolate_previous_value([0, 3, 6, 9, 12, 15])
    -3
    >>> extrapolate_previous_value([1, 3, 6, 10, 15, 21])
    0
    >>> extrapolate_previous_value([10, 13, 16, 21, 30, 45])
    5
    """
    sequences = [history]
    while True:
        diffs = [sequences[-1][i + 1] - sequences[-1][i] for i in range(len(sequences[-1]) - 1)]
        sequences.append(diffs)
        if all(d == 0 for d in diffs):
            break

    for i in range(len(sequences) - 2, -1, -1):
        sequences[i].insert(0, sequences[i][0] - sequences[i + 1][0])

    return sequences[0][0]


if __name__ == "__main__":
    doctest.testmod()

    histories = read_and_preprocess_data('input.txt')  # Replace 'data.txt' with your actual data file
    total = sum(extrapolate_previous_value(history) for history in histories)
    print(f"Part 2: {total}")
