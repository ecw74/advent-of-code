def parse_almanac(almanac_text):
    """
    Parses the almanac text and extracts the seed number ranges and the mappings for each category.

    Args:
    almanac_text (str): The text of the almanac.

    Returns:
    tuple: A tuple containing a list of seed number ranges (as start and end values) and a dictionary of mappings for each category.
    """
    lines = almanac_text.strip().split('\n')
    seed_pairs = [int(x) for x in lines[0].split(':')[1].split()]
    seed_ranges = [(seed_pairs[i], seed_pairs[i] + seed_pairs[i + 1] - 1) for i in range(0, len(seed_pairs), 2)]

    mappings = {}
    current_map = None

    for line in lines[1:]:
        if 'map' in line:
            current_map = line.split(':')[0]
            mappings[current_map] = []
        else:
            if line.strip():
                destination_start, source_start, range_length = map(int, line.split())
                mappings[current_map].append((destination_start, source_start, range_length))

    return seed_ranges, mappings


def merge_ranges(ranges):
    """
    Merge overlapping or contiguous ranges.

    Args:
    ranges (list): List of tuples representing ranges (start, end).

    Returns:
    list: Merged list of ranges.
    """
    if not ranges:
        return []

    # Sort ranges by their start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last = merged[-1]
        if current[0] <= last[1] + 1:  # Check if ranges overlap or are contiguous
            merged[-1] = (last[0], max(last[1], current[1]))  # Merge the ranges
        else:
            merged.append(current)

    return merged


def map_range(range, mapping):
    """
    Apply a mapping to a range.

    Args:
    range (tuple): A tuple representing the range (start, end).
    mapping (list): List of tuples representing the mapping rules (destination_start, source_start, range_length).

    Returns:
    list: List of ranges after applying the mapping.
    """
    start, end = range
    result = []

    for destination_start, source_start, range_length in mapping:
        source_end = source_start + range_length - 1
        if source_start <= end and start <= source_end:  # Check if ranges overlap
            mapped_start = max(start, source_start)
            mapped_end = min(end, source_end)
            offset = mapped_start - source_start
            result.append((destination_start + offset, destination_start + offset + mapped_end - mapped_start))

    # Handle the case where the number maps to itself if not in any mapping
    if not result:
        result.append((start, end))

    return result


def optimize_conversion(seed_ranges, mappings):
    """
    Optimizes the conversion of seed ranges through each mapping to find the lowest possible location.

    Efficiently handles large ranges without iterating over individual numbers.

    Args:
    seed_ranges (list): A list of tuples representing the seed ranges.
    mappings (dict): A dictionary of mappings for each category.

    Returns:
    int: The lowest possible location number after conversion through all mappings.

    Example:
    >>> seed_ranges = [(79, 92), (55, 67)]
    >>> mappings = {
    ...     'seed-to-soil map': [(50, 98, 2), (52, 50, 48)],
    ...     'soil-to-fertilizer map': [(0, 15, 37), (37, 52, 2), (39, 0, 15)],
    ...     'fertilizer-to-water map': [(49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4)],
    ...     'water-to-light map': [(88, 18, 7), (18, 25, 70)],
    ...     'light-to-temperature map': [(45, 77, 23), (81, 45, 19), (68, 64, 13)],
    ...     'temperature-to-humidity map': [(0, 69, 1), (1, 0, 69)],
    ...     'humidity-to-location map': [(60, 56, 37), (56, 93, 4)]
    ... }
    >>> optimize_conversion(seed_ranges, mappings)
    46
    """
    current_ranges = [(start, end - 1) for start, end in seed_ranges]  # Convert end to exclusive

    for category in mappings:
        next_ranges = []
        for range in current_ranges:
            mapped_ranges = map_range(range, mappings[category])
            next_ranges.extend(mapped_ranges)
        current_ranges = merge_ranges(next_ranges)

    return min(current_ranges)[0]


def read_almanac_from_file(file_path):
    """
    Reads the almanac text from a file.

    Args:
    file_path (str): The path to the file containing the almanac.

    Returns:
    str: The content of the almanac.
    """
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    almanac_text = read_almanac_from_file("input.txt")

    # Process the almanac text using the previously defined functions
    seeds, mappings = parse_almanac(almanac_text)
    result = optimize_conversion(seeds, mappings)
    print(f"Part 2: {result}")
