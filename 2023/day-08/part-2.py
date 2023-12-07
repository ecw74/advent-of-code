from functools import reduce
from math import lcm


def read_and_preprocess(file_path):
    """
    Reads data from a file and prepares it for processing.

    The file should have the following format:
    - The first line contains left-right instructions.
    - The following lines define the nodes of the network.

    Example:
    RL

    AAA = (BBB, CCC)
    BBB = (DDD, EEE)
    CCC = (ZZZ, GGG)
    DDD = (DDD, DDD)
    EEE = (EEE, EEE)
    GGG = (GGG, GGG)
    ZZZ = (ZZZ, ZZZ)

    Args:
    file_path (str): Path to the input file.

    Returns:
    tuple: A tuple containing the instructions and the network as a dictionary.

    Doctest:
    >>> read_and_preprocess('test.txt')
    ('RL', {'AAA': ('BBB', 'CCC'), 'BBB': ('DDD', 'EEE'), 'CCC': ('ZZZ', 'GGG'), 'DDD': ('DDD', 'DDD'), 'EEE': ('EEE', 'EEE'), 'GGG': ('GGG', 'GGG'), 'ZZZ': ('ZZZ', 'ZZZ')})
    """
    with open(file_path, 'r') as file:
        instructions = file.readline().strip()
        network = dict(line.strip().split(' = ') for line in file if line.strip())

    # Convert string representations of tuples to actual tuples
    for node in network:
        network[node] = tuple(network[node].strip('()').split(', '))

    return instructions, network


def calculate_steps(node, nodes, instructions):
    """
    Calculates the number of steps required for a single path to reach a node ending with 'Z'.
    Does not check for cycles.

    Args:
        node (str): The starting node.
        nodes (dict): A dictionary of nodes and their connections.
        instructions (str): Navigation instructions.

    Returns:
        int: Number of steps to reach a node ending with 'Z', or -1 if not reachable.
    """
    step_count = 0
    current_node = node

    while not current_node[-1] == 'Z':
        if current_node not in nodes:
            return -1  # Node not in the graph

        instruction = instructions[step_count % len(instructions)]
        current_node = nodes[current_node][0 if instruction == 'L' else 1]
        step_count += 1

    return step_count


def navigate_with_lcm(instructions, nodes):
    """
    Navigate through nodes to find the least common multiple of steps required for each path to reach a node ending with 'Z'.

    Args:
        instructions (str): A string of 'L' and 'R' characters representing navigation instructions.
        nodes (dict): A dictionary of nodes where keys are node labels and values are tuples (left, right) nodes.

    Returns:
        int: The least common multiple of steps for all paths to end at nodes ending with 'Z'.

    Example:
    >>> navigate_with_lcm('LR', {'11A': ('11B', 'XXX'), '11B': ('XXX', '11Z'), '11Z': ('11B', 'XXX'), '22A': ('22B', 'XXX'), '22B': ('22C', '22C'), '22C': ('22Z', '22Z'), '22Z': ('22B', '22B'), 'XXX': ('XXX', 'XXX')})
    6
    """
    start_nodes = [node for node in nodes if node.endswith('A')]
    steps = [calculate_steps(node, nodes, instructions) for node in start_nodes]

    if any(step == -1 for step in steps):
        return -1  # If any path does not reach a 'Z' node

    return lcm(*steps)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    instructions, network = read_and_preprocess('input.txt')
    steps_to_all_z = navigate_with_lcm(instructions, network)
    print(f"Part 2: {steps_to_all_z}")
