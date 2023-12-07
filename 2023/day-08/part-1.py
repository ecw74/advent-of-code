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
        lines = file.readlines()

    instructions = lines[0].strip()
    network = {}
    for line in lines[1:]:
        line = line.strip()
        if line:
            node, connections = line.split(' = ')
            connections = connections.strip('()').split(', ')
            network[node] = tuple(connections)

    return instructions, network


def calculate_steps(node, nodes, instructions):
    """
    Calculates the number of steps required to reach the node 'ZZZ' from a given starting node.

    Args:
        node (str): The starting node.
        nodes (dict): A dictionary of nodes and their connections.
        instructions (str): Navigation instructions.

    Returns:
        int: Number of steps to reach 'ZZZ', or -1 if not reachable.
    """
    step_count = 0
    current_node = node

    while current_node != "ZZZ":
        if current_node not in nodes:
            return -1  # Node not in the graph

        instruction = instructions[step_count % len(instructions)]
        current_node = nodes[current_node][0 if instruction == 'L' else 1]
        step_count += 1

    return step_count


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    instructions, network = read_and_preprocess('input.txt')
    result = calculate_steps("AAA", network, instructions)
    print(f"Part 1: {result}")
