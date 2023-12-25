def sum_calibration_values(filename):
    """
    Reads a file and calculates the sum of calibration values.
    Each calibration value is determined by combining the first and last digit of each line in the file.

    :param filename: str - The name of the file to be read.
    :return: int - The sum of all calibration values.

    >>> with open('test.txt', 'w') as f:
    ...     _ = f.write('1abc2\\npqr3stu8vwx\\na1b2c3d4e5f\\ntreb7uchet')
    >>> sum_calibration_values('test.txt')
    142
    """
    total_sum = 0
    with open(filename, 'r') as file:
        for line in file:
            digits = [char for char in line if char.isdigit()]
            if digits:
                calibration_value = int(digits[0] + digits[-1])
                total_sum += calibration_value
    return total_sum

if __name__ == "__main__":
    import doctest

    doctest.testmod()
    result = sum_calibration_values('input.txt')
    print(f"Part 1: {result}")