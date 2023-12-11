from functools import cache


def read_input(filename):
    """
    Reads the input file and returns a list of tuples containing the spring conditions
    and the group sizes for each row.

    Each line in the file should be in the format: 'condition_string group_sizes'
    where 'condition_string' consists of '.', '#', and '?' characters and
    'group_sizes' is a comma-separated list of integers.

    >>> read_input('test_input.txt')
    [('???.###', [1, 1, 3]), ('.??..??...?##.', [1, 1, 3]), ('?#?#?#?#?#?#?#?', [1, 3, 1, 6]), ('????.#...#...', [4, 1, 1]), ('????.######..#####.', [1, 6, 5]), ('?###????????', [3, 2, 1])]
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            parts = line.strip().split()
            conditions = parts[0]
            groups = list(map(int, parts[1].split(',')))
            data.append((conditions, groups))
        return data

@cache
def count_combinations(springs: str, groups: tuple[int, ...]):
    """
    Counts the number of arrangements of groups of '#' within a bitmask of '?', '#', and '.'.

    Doctests:
    >>> count_combinations("???.###", tuple([1, 1, 3]))
    1
    >>> count_combinations(".??..??...?##.", tuple([1, 1, 3]))
    4
    >>> count_combinations("?#?#?#?#?#?#?#?", tuple([1, 3, 1, 6]))
    1
    >>> count_combinations("????.#...#...", tuple([4, 1, 1]))
    1
    >>> count_combinations("????.######..#####.", tuple([1, 6, 5]))
    4
    >>> count_combinations("?###????????", tuple([3, 2, 1]))
    10

    :param bitmask: A string consisting of '?', '#', and '.' representing the bitmask.
    :param groups: A list of integers representing the sizes of groups of '#' to be arranged.
    :return: The number of possible arrangements.
    """
    springs = springs.lstrip(".")
    if len(groups) == 0:
        return int("#" not in springs)
    if len(springs) == 0:
        return int(len(groups) == 0)

    if springs[0] == "?":
        return count_combinations("." + springs[1:], groups) + count_combinations("#" + springs[1:], groups)
    elif springs[0] == "#":
        remaining = groups[0]
        if "." not in springs[:remaining]:
            if remaining < len(springs) and springs[remaining] != "#":
                return count_combinations(springs[remaining + 1:], groups[1:])
            elif len(springs) == remaining:
                return int(len(groups) == 1)
    return 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    input = read_input("input.txt")
    total_combinations = 0
    for spring, group in input:
        total_combinations += count_combinations(spring, tuple(group))
    print(total_combinations)

