def identify_calibration_value(line):
    """
    Identifies and returns the calibration value from a line of text.
    The calibration value is formed by combining the first and last digit (numeric or transformed spelled out).

    :param line: str - A line of text.
    :return: int - The calibration value from the line.

    >>> identify_calibration_value('two1nine')
    29
    >>> identify_calibration_value('eightwothree')
    83
    >>> identify_calibration_value('abcone2threexyz')
    13
    >>> identify_calibration_value('xtwone3four')
    24
    >>> identify_calibration_value('4nineeightseven2')
    42
    >>> identify_calibration_value('zoneight234')
    14
    >>> identify_calibration_value('7pqrstsixteen')
    76
    """
    digit_transform = {
        'zero': 'z0o', 'one': 'o1e', 'two': 't2o', 'three': 'th3ree',
        'four': 'fo4r', 'five': 'fi5ve', 'six': 'si6x', 'seven': 'se7ven',
        'eight': 'ei8ght', 'nine': 'ni9ne'
    }

    for word, replacement in digit_transform.items():
        line = line.replace(word, replacement)

    digits = [char for char in line if char.isdigit()]

    if len(digits) >= 2:
        return int(digits[0] + digits[-1])
    elif len(digits) == 1:
        return int(digits[0] * 2)  # If only one digit is found, use it twice
    return 0


def sum_calibration_values(filename):
    """
    Reads a file and calculates the sum of calibration values.
    Each line's calibration value is determined by the 'identify_calibration_value' function.

    :param filename: str - The name of the file to be read.
    :return: int - The sum of all calibration values.

    >>> with open('test.txt', 'w') as f:
    ...     _ = f.write('two1nine\\neightwothree\\nabcone2threexyz\\nxtwone3four\\n4nineeightseven2\\nzoneight234\\n7pqrstsixteen')
    >>> sum_calibration_values('test.txt')
    281
    """
    total_sum = 0
    with open(filename, 'r') as file:
        for line in file:
            total_sum += identify_calibration_value(line)
    return total_sum


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    result = sum_calibration_values('input.txt')
    print(f"Part 2: {result}")
