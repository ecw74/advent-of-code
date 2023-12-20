from collections import deque, defaultdict

import numpy as np


class FlipFlopModule:
    """
    Represents a flip-flop module which toggles its state between True and False
    with each 'low' pulse received.

    Attributes:
        name (str): The name of the module.
        state (bool): The current state of the module (True or False).
        destinations (list): List of destination modules to send the pulse to.
    """

    def __init__(self, name):
        self.name = name
        self.state = False  # Initially off
        self.destinations = []

    def receive_pulse(self, pulse_type):
        """
        Toggles the state if a 'low' pulse is received and returns the new pulse type.

        Args:
            pulse_type (str): The type of pulse received ('low' or other).

        Returns:
            str: 'high' if the state is True after toggling, 'low' if False, None otherwise.

        Examples:
            >>> f = FlipFlopModule('flipflop')
            >>> f.receive_pulse('low')
            'high'
            >>> f.receive_pulse('low')
            'low'
        """
        if pulse_type == 'low':
            self.state = not self.state
            return 'high' if self.state else 'low'
        return None


class ConjunctionModule:
    """
    Represents a conjunction module that outputs 'low' only if all its inputs are 'high'.

    Attributes:
        name (str): The name of the module.
        input_states (dict): A dictionary tracking the states ('low' or 'high') of inputs.
        destinations (list): List of destination modules to send the pulse to.
    """

    def __init__(self, name):
        """
        Initializes the ConjunctionModule with a given name.

        Args:
            name (str): The name of the module.
        """
        self.name = name
        self.input_states = {}
        self.destinations = []

    def receive_pulse(self, pulse_type, source):
        """
        Receives a pulse from a source module and updates the module's output.

        If all inputs are 'high', it outputs 'low', otherwise 'high'.

        Args:
            pulse_type (str): The type of pulse ('low' or 'high').
            source (object): The source module sending the pulse.

        Returns:
            str: 'low' if all inputs are 'high', otherwise 'high'.
        """

        self.input_states[source] = pulse_type
        if all(state == 'high' for state in self.input_states.values()):
            return 'low'
        return 'high'


class BroadcasterModule:
    """
    Represents a broadcaster module that forwards the received pulse type unchanged.

    Attributes:
        name (str): The name of the module, defaulted to "broadcaster".
        destinations (list): List of destination modules to send the pulse to.
    """

    def __init__(self):
        self.name = "broadcaster"
        self.destinations = []

    def receive_pulse(self, pulse_type):
        """
        Forwards the received pulse type without any modification.

        Args:
            pulse_type (str): The type of pulse received (e.g., 'low', 'high').

        Returns:
            str: The same pulse type as received.
        """
        return pulse_type


class ButtonModule:
    """
    Represents a button module that always generates a 'low' pulse.

    Attributes:
        name (str): The name of the module, set to 'button'.
        destinations (list): List of destination modules to send the pulse to.
    """

    def __init__(self):
        self.name = 'button'
        self.destinations = []

    def receive_pulse(self):
        """
        Simulates the action of pressing the button, which always generates a 'low' pulse.

        Returns:
            str: Always returns 'low'.
        """
        return 'low'


class OutputModule:
    """
    Represents an output module which receives pulses but does not act on them.

    This module is designed to be a terminal point in the network of modules.
    It does not modify the state of the pulse or propagate it further.

    Attributes:
        name (str): The name of the module.
    """

    def __init__(self, name):
        """
        Initializes the OutputModule with a given name.

        Args:
            name (str): The name of the output module.
        """
        self.name = name
        self.destinations = []

    def receive_pulse(self, pulse_type):
        """
        Receives a pulse but does not perform any action.

        This method is intended to be a placeholder to maintain a consistent interface
        across different module types. It does not change the state of the pulse or
        have any side effects.

        Args:
            pulse_type (str): The type of pulse received ('low' or 'high').
        """
        pass


def read_config(filename):
    """
    Reads a configuration file and sets up the modules and their connections.

    Args:
        filename (str): Path to the configuration file.

    Returns:
        dict: A dictionary of module names to module objects.
    """
    modules = {
        'button': ButtonModule()
    }
    connections = defaultdict(list)

    with open(filename, 'r') as file:
        lines = file.readlines()

        # init all nodes per default as output nodes
        for line in lines:
            parts = line.strip().split(' -> ')
            _, dst = parts[0], parts[1].split(', ')
            for d in dst:
                modules[d] = OutputModule(d)

        # now assign the correct node type
        for line in lines:
            # Create list of modules
            parts = line.strip().split(' -> ')
            src, dst = parts[0], parts[1].split(', ')
            if src not in modules:
                module_name = ""
                if src.startswith('%'):
                    modules[src.strip('%')] = FlipFlopModule(src.strip('%'))
                elif src.startswith('&'):
                    modules[src.strip('&')] = ConjunctionModule(src.strip('&'))
                elif src == 'broadcaster':
                    modules[src] = BroadcasterModule()
                    modules['button'].destinations.append(modules[src])
                else:
                    print(f"Unkown module type {src}")

        for line in lines:
            # Create connections
            parts = line.strip().split(' -> ')
            src, dst = parts[0], parts[1].split(', ')

            for d in dst:
                src = src.strip('%').strip('&')
                connections[d].append(modules[src])
                if d in modules:
                    modules[src].destinations.append(modules[d])

    for mod_name, mod in modules.items():
        if isinstance(mod, ConjunctionModule):
            for input_mod in connections[mod_name]:
                mod.input_states[input_mod] = 'low'

    return modules


def simulate_pulses(modules, num_button_pushes):
    """
    Simulates the propagation of pulses through the modules.

    Args:
        modules (dict): A dictionary of module names to module objects.
        num_button_pushes (int): The number of times the button is pushed.

    Returns:
        tuple: Counts of 'low' and 'high' pulses.
    """
    pulse = {
        'low': np.uint64(0),
        'high': np.uint64(0)
    }

    for _ in range(num_button_pushes):
        pulse_queue = deque([('low', None, modules['button'])])

        while pulse_queue:
            pulse_type, src, module = pulse_queue.popleft()

            new_pulse = None
            if isinstance(module, ButtonModule):
                new_pulse = module.receive_pulse()
            if isinstance(module, BroadcasterModule):
                new_pulse = module.receive_pulse(pulse_type)
            elif isinstance(module, FlipFlopModule):
                new_pulse = module.receive_pulse(pulse_type)
            elif isinstance(module, ConjunctionModule):
                new_pulse = module.receive_pulse(pulse_type, src)

            if new_pulse:
                for dest in module.destinations:
                    pulse[new_pulse] += 1
                    pulse_queue.append((new_pulse, module, dest))

    return pulse['low'], pulse['high']


if __name__ == "__main__":
    modules = read_config("input.txt")
    low_pulse_count, high_pulse_count = simulate_pulses(modules, 10000)
    result = low_pulse_count * high_pulse_count
    print(f"Part -1: {result}")
