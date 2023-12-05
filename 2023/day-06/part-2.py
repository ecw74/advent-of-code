import math


def read_and_preprocess(file_path):
    """
    Reads race data from a given file and preprocesses it into a single race's time and distance.

    The function concatenates the numbers on each line to form a single large number.

    :param file_path: Path to the file containing race data.
    :return: A tuple containing the time and distance for the single race.

    This doctest assumes 'test.txt' contains the following lines:
    'Time:      7  15   30'
    'Distance:  9  40  200'
    >>> read_and_preprocess('test.txt')  # Adjust the path as needed
    (71530, 940200)
    """
    with open(file_path, 'r') as file:
        time_line, distance_line = file.readlines()
        time = int(''.join(time_line.split()[1:]))
        distance = int(''.join(distance_line.split()[1:]))

    return time, distance


def calculate_winning_ways(race):
    """
    Calculates the number of ways to beat the record in a single race.

    :param race: A tuple containing the time and distance for the race.
    :return: The number of ways to beat the record in the race.

    >>> calculate_winning_ways((71530, 940200))
    71503
    """
    time, record = race
    max_hold_time = time - 1

    # The equation of motion is d = v * t, where v = hold_time and t = (time - hold_time)
    # This simplifies to d = hold_time * (time - hold_time), which is a parabolic equation
    # We solve for hold_time using the quadratic formula where a = -1, b = time, c = -record
    a, b, c = -1, time, -record
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return 0  # No solution, cannot beat the record

    # Two solutions from the quadratic formula
    sol1 = (-b + math.sqrt(discriminant)) / (2 * a)
    sol2 = (-b - math.sqrt(discriminant)) / (2 * a)

    # Valid hold times are within [1, max_hold_time] range and should be whole numbers
    lower_bound = math.ceil(min(sol1, sol2))
    upper_bound = math.floor(max(sol1, sol2))

    # Clamp the values within the valid range
    lower_bound = max(lower_bound, 1)
    upper_bound = min(upper_bound, max_hold_time)

    return max(0, upper_bound - lower_bound + 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    races_data = read_and_preprocess('input.txt')

    result = calculate_winning_ways(races_data)
    print(f"Part 2: {result}")
