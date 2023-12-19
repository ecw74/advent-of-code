import re


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


def evaluate_condition(condition, part_ratings):
    """
    Evaluates a condition against part ratings.

    :param condition: The condition string (e.g., 'x>10').
    :param part_ratings: Dictionary of part ratings.
    :return: Boolean result of the condition evaluation.
    """
    if condition is None:
        return True

    lhs, operator, rhs = re.match(r"(\w)([<>]=?)(\d+)", condition).groups()
    rhs = int(rhs)

    if operator == '>':
        return part_ratings[lhs] > rhs
    elif operator == '<':
        return part_ratings[lhs] < rhs
    elif operator == '>=':
        return part_ratings[lhs] >= rhs
    elif operator == '<=':
        return part_ratings[lhs] <= rhs
    else:
        raise ValueError(f"Unknown operator in condition: {condition}")


def process_part(workflows, part, start_workflow):
    """
    Processes a part through the workflows.

    :param workflows: Dictionary of parsed workflows.
    :param part: Dictionary of part ratings.
    :param start_workflow: The starting workflow name.
    :return: Boolean indicating if the part was accepted.
    """
    workflow = start_workflow
    while True:
        for condition, action in workflows[workflow]:
            if evaluate_condition(condition, part):
                if action == 'A':
                    return True
                elif action == 'R':
                    return False
                else:
                    workflow = action
                    break


def calc_total_rating(workflows, part_data):
    total_rating = 0
    for part in part_data:
        part_ratings = {k: int(v) for k, v in re.findall(r'(\w)=(\d+)', part)}
        if process_part(workflows, part_ratings, 'in'):
            total_rating += sum(part_ratings.values())
    return total_rating


if __name__ == "__main__":
    workflow_data, part_data = read_input("input.txt")
    workflows = parse_workflows(workflow_data)
    total_rating = calc_total_rating(workflows, part_data)
    print(f"Part 1: {total_rating}")
