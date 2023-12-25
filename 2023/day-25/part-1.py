import sys

import numpy as np


def parse_input(file_path):
    """
    Reads and parses the input data from a file to create a graph representation.

    :param file_path: The path to the file containing the wiring diagram.
    :return: A dictionary representing the graph.

    Example:
    # Assuming 'example.txt' contains:
    # a: b
    # b: a
    >>> parse_input("example.txt")
    {'a': {'b'}, 'b': {'a'}}
    """
    graph = {}
    with open(file_path) as file:
        for line in file:
            s, e = line.split(':')
            for y in e.split():
                if s not in graph:
                    graph[s] = set()
                if y not in graph:
                    graph[y] = set()
                graph[s].add(y)
                graph[y].add(s)
    return graph


def initialize_graph(graph_dict):
    """
    Initializes the graph from a dictionary of sets and converts it to an adjacency matrix.

    Args:
        graph_dict (Dict[str, Set[str]]): A dictionary of sets representing the graph.

    Returns:
        An adjacency matrix representing the graph.
    """

    # Initialize the graph with edge weights
    graph = {u: {v: 1 for v in neighbors} for u, neighbors in graph_dict.items()}

    # Convert to adjacency matrix
    nodes = list(graph.keys())
    node_index = {node: i for i, node in enumerate(nodes)}
    size = len(nodes)
    matrix = [[0] * size for _ in range(size)]

    for node, edges in graph.items():
        for adjacent, weight in edges.items():
            i, j = node_index[node], node_index[adjacent]
            matrix[i][j] = weight

    return matrix


def stoer_wagner_algorithm(adjacency_matrix):
    """
    Implement the Stoer-Wagner algorithm to find the minimum cut of a graph.
    (see https://en.wikipedia.org/wiki/Stoer%E2%80%93Wagner_algorithm)

    It's based of the C++ implementation in the kactl library
    (see https://github.com/kth-competitive-programming/kactl/blob/main/content/graph/GlobalMinCut.h)

    Parameters:
    adjacency_matrix: A square matrix representing the adjacency matrix of the graph.

    Returns:
    A tuple containing the weight of the minimum cut and the vertices involved in this cut.
    """

    # Set a high value to represent infinity.
    infinity = sys.maxsize

    # Determine the number of vertices in the graph.
    num_vertices = len(adjacency_matrix)

    # Convert the matrix to a numpy array for efficient computation.
    converted_matrix = np.array(adjacency_matrix, dtype='int64')

    # Initialize the best cut as infinity and an empty list.
    minimum_cut = (infinity, [])

    # Initialize a list to keep track of combined vertices.
    combined_vertices = [[vertex] for vertex in range(num_vertices)]

    # Main loop to contract the graph one edge at a time.
    for phase in range(1, num_vertices):
        # Create a copy of the weights of the edges connected to the first vertex.
        edge_weights = converted_matrix[0].copy()
        source_vertex, target_vertex = 0, 0

        # Find the most tightly connected vertices.
        for _ in range(num_vertices - phase):
            # Ignore the last used vertex by setting its weight to negative infinity.
            edge_weights[target_vertex] = -infinity

            # Select vertices based on maximum edge weight.
            source_vertex, target_vertex = target_vertex, np.argmax(edge_weights)

            # Update the weights to reflect the addition of target_vertex.
            edge_weights += converted_matrix[target_vertex]

        # Update the minimum cut if a smaller one is found.
        cut_weight = edge_weights[target_vertex] - converted_matrix[target_vertex, target_vertex]
        minimum_cut = min(minimum_cut, (cut_weight, combined_vertices[target_vertex].copy()))

        # Combine the source and target vertices.
        combined_vertices[source_vertex].extend(combined_vertices[target_vertex])

        # Update the adjacency matrix to reflect the contraction.
        converted_matrix[source_vertex] += converted_matrix[target_vertex]
        converted_matrix[:, source_vertex] = converted_matrix[source_vertex]  # Symmetric update.

        # Mark the target vertex as used.
        converted_matrix[0, target_vertex] = -infinity

    # Return the minimum cut weight and the involved vertices.
    return minimum_cut


def main():
    graph_dict = parse_input('input.txt')
    adj_matrix = initialize_graph(graph_dict)
    ans = stoer_wagner_algorithm(adj_matrix)
    result = len(ans[1]) * (len(adj_matrix) - len(ans[1]))
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
