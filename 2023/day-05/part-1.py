def parse_almanac(almanac_text):
    """
    Parses the almanac text and extracts the seed numbers and the mappings for each category.

    The almanac text format is expected to have a list of seeds followed by mappings in the format:
    category-to-category map:
    destination_start source_start range_length

    Args:
    almanac_text (str): The text of the almanac.

    Returns:
    tuple: A tuple containing a list of seed numbers and a dictionary of mappings for each category.

    Example:
    >>> almanac_text = '''seeds: 79 14 55 13\\n\\nseed-to-soil map:\\n50 98 2\\n52 50 48\\n'''
    >>> seeds, mappings = parse_almanac(almanac_text)
    >>> seeds
    [79, 14, 55, 13]
    >>> mappings['seed-to-soil map']
    [(50, 98, 2), (52, 50, 48)]
    """
    lines = almanac_text.strip().split('\n')
    seeds = [int(x) for x in lines[0].split(':')[1].split()]
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

    return seeds, mappings


def convert_number(source_number, mapping):
    """
    Converts a number from one category to another using the provided mapping.

    Args:
    source_number (int): The number to be converted.
    mapping (list): A list of tuples, each containing destination start, source start, and range length.

    Returns:
    int: The converted number in the destination category.

    Example:
    >>> convert_number(79, [(50, 98, 2), (52, 50, 48)])
    81
    >>> convert_number(14, [(50, 98, 2), (52, 50, 48)])
    14
    """
    for destination_start, source_start, range_length in mapping:
        if source_start <= source_number < source_start + range_length:
            # Calculate the offset from the start of the source range
            offset = source_number - source_start
            # Apply the same offset to the destination start
            return destination_start + offset
    # If the number is not in any range, it maps to itself
    return source_number


def find_lowest_location(seeds, mappings):
    """
    Finds the lowest location number that corresponds to any of the initial seed numbers.

    Args:
    seeds (list): A list of seed numbers.
    mappings (dict): A dictionary of mappings for each category.

    Returns:
    int: The lowest location number corresponding to the initial seeds.

    Example:
    >>> seeds = [79, 14, 55, 13]
    >>> mappings = {
    ...     'seed-to-soil map': [(50, 98, 2), (52, 50, 48)],
    ...     'soil-to-fertilizer map': [(0, 15, 37), (37, 52, 2), (39, 0, 15)],
    ...     'fertilizer-to-water map': [(49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4)],
    ...     'water-to-light map': [(88, 18, 7), (18, 25, 70)],
    ...     'light-to-temperature map': [(45, 77, 23), (81, 45, 19), (68, 64, 13)],
    ...     'temperature-to-humidity map': [(0, 69, 1), (1, 0, 69)],
    ...     'humidity-to-location map': [(60, 56, 37), (56, 93, 4)]
    ... }
    >>> find_lowest_location(seeds, mappings)
    35
    """
    lowest_location = float('inf')
    for seed in seeds:
        soil = convert_number(seed, mappings['seed-to-soil map'])
        fertilizer = convert_number(soil, mappings['soil-to-fertilizer map'])
        water = convert_number(fertilizer, mappings['fertilizer-to-water map'])
        light = convert_number(water, mappings['water-to-light map'])
        temperature = convert_number(light, mappings['light-to-temperature map'])
        humidity = convert_number(temperature, mappings['temperature-to-humidity map'])
        location = convert_number(humidity, mappings['humidity-to-location map'])
        lowest_location = min(lowest_location, location)

    return lowest_location


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
    result = find_lowest_location(seeds, mappings)
    print(f"Part 1: {result}")
