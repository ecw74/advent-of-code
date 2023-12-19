from math import prod


def read_input(filename):
    """
    Reads workflow and part data from a file.

    :param filename: Path to the file containing workflow and part data.
    :return: Tuple containing two lists: workflow definitions and part data.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the blank line separating workflows and parts
    blank_line_index = lines.index('\n')
    workflow_data = lines[:blank_line_index]
    part_data = lines[blank_line_index + 1:]

    return workflow_data, part_data


def parse_workflows(workflow_data):
    """
    Parses the workflow definitions into a dictionary.

    :param workflow_data: List of workflow strings.
    :return: Dictionary of workflows and their rules.

    >>> parse_workflows(['ex{x>10:one,m<20:two,a>30:R,A}', 'ab{x<5:A,m>15:R}'])
    {'ex': [('x>10', 'one'), ('m<20', 'two'), ('a>30', 'R'), (None, 'A')], 'ab': [('x<5', 'A'), ('m>15', 'R')]}
    """
    workflows = {}
    for line in workflow_data:
        name, rules = line.split('{', 1)
        name = name.strip()  # Removing any trailing whitespace
        rules = rules.strip('}\n').split(',')  # Removing the closing brace and splitting the rules
        parsed_rules = []
        for rule in rules:
            condition, action = rule.split(':') if ':' in rule else (None, rule)
            parsed_rules.append((condition, action))
        workflows[name] = parsed_rules
    return workflows


def read_input(filename):
    """
    Reads workflow and part data from a file.

    :param filename: Path to the file containing workflow and part data.
    :return: Tuple containing two lists: workflow definitions and part data.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Find the blank line separating workflows and parts
    blank_line_index = lines.index('\n')
    workflow_data = lines[:blank_line_index]
    part_data = lines[blank_line_index + 1:]

    return workflow_data, part_data


def parse_workflows(workflow_data):
    """
    Parses the workflow definitions into a dictionary.

    :param workflow_data: List of workflow strings.
    :return: Dictionary of workflows and their rules.

    >>> parse_workflows(['ex{x>10:one,m<20:two,a>30:R,A}', 'ab{x<5:A,m>15:R}'])
    {'ex': [('x>10', 'one'), ('m<20', 'two'), ('a>30', 'R'), (None, 'A')], 'ab': [('x<5', 'A'), ('m>15', 'R')]}
    """
    workflows = {}
    for line in workflow_data:
        name, rules = line.split('{', 1)
        name = name.strip()  # Removing any trailing whitespace
        rules = rules.strip('}\n').split(',')  # Removing the closing brace and splitting the rules
        parsed_rules = []
        for rule in rules:
            condition, action = rule.split(':') if ':' in rule else (None, rule)
            parsed_rules.append((condition, action))
        workflows[name] = parsed_rules
    return workflows


def split_ranges(ranges, condition):
    """
    Splits the ranges based on the given condition.

    :param ranges: List of possible values for each rating.
    :param condition: A string representing the condition (e.g., 'x>2005').
    :return: A tuple of two lists: ranges that meet the condition and ranges that do not.
    """
    rating_index = "xmas".index(condition[0])
    threshold = int(condition[2:])
    if condition[1] == '>':
        matching = [x for x in ranges[rating_index] if x > threshold]
        non_matching = [x for x in ranges[rating_index] if x <= threshold]
    else:
        matching = [x for x in ranges[rating_index] if x < threshold]
        non_matching = [x for x in ranges[rating_index] if x >= threshold]

    new_ranges = [list(r) for r in ranges]
    new_ranges[rating_index] = matching
    remaining_ranges = [list(r) for r in ranges]
    remaining_ranges[rating_index] = non_matching

    return new_ranges, remaining_ranges


def calculate_combinations(workflows, current_workflow, ranges):
    """
    Recursively calculates the total number of accepted combinations based on the workflows.

    :param workflows: Dictionary of workflow rules.
    :param current_workflow: The current workflow identifier.
    :param ranges: List of lists, each representing the range of possible values for a rating.
    :return: Total number of accepted combinations.
    """
    if current_workflow == "R":
        return 0
    if current_workflow == "A":
        return prod(len(r) for r in ranges)

    total = 0
    for condition, next_workflow in workflows[current_workflow]:
        if condition is None:
            total += calculate_combinations(workflows, next_workflow, ranges)
            continue

        new_ranges, ranges = split_ranges(ranges, condition)

        total += calculate_combinations(workflows, next_workflow, new_ranges)

    return total


def total_accepted_combinations(workflows, start_workflow):
    """
    Calculates the total number of accepted combinations for the given workflows.

    :param workflows: Dictionary of workflow rules.
    :param start_workflow: The starting workflow identifier.
    :return: Total number of accepted combinations.
    """
    ranges = [[i for i in range(1, 4001)] for _ in range(4)]
    return calculate_combinations(workflows, start_workflow, ranges)


if __name__ == "__main__":
    workflow_data, part_data = read_input("input.txt")
    workflows = parse_workflows(workflow_data)
    total_combinations = total_accepted_combinations(workflows, 'in')
    print(f"Part 2: {total_combinations}")
