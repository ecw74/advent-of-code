def read_and_preprocess(file_path):
    """
    Reads race data from a given file and preprocesses it into a usable format.

    The function reads two lines: the first line for times and the second line for distances.

    :param file_path: Path to the file containing race data.
    :return: A list of tuples, each containing time and distance for a race.

    This doctest assumes 'test.txt' contains the following lines:
    'Time:      7  15   30'
    'Distance:  9  40  200'
    >>> read_and_preprocess('test.txt')  # Adjust the path as needed
    [(7, 9), (15, 40), (30, 200)]
    """
    with open(file_path, 'r') as file:
        file_lines = file.readlines()
        times = list(map(int, file_lines[0].split()[1:]))  # Skip the first word 'Time:'
        distances = list(map(int, file_lines[1].split()[1:]))  # Skip the first word 'Distance:'

    return list(zip(times, distances))


def calculate_winning_ways(races):
    """
    Calculates the number of ways to beat the record in each race.

    :param races: A list of tuples, each containing time and distance for a race.
    :return: The product of the number of ways to beat the record in each race.

    >>> calculate_winning_ways([(7, 9), (15, 40), (30, 200)])
    288
    """

    def max_distance(hold_time, total_time):
        return (total_time - hold_time) * hold_time

    total_ways = 1
    for race in races:
        time, record = race
        ways_to_win = sum(1 for hold_time in range(1, time) if max_distance(hold_time, time) > record)
        total_ways *= ways_to_win

    return total_ways


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    races_data = read_and_preprocess('test.txt')

    result = calculate_winning_ways(races_data)
    print(f"Part 1: {result}")
