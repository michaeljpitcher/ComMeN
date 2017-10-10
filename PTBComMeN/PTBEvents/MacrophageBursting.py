#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_bursting_events(nodes, bursting_rate, carrying_capacity, hill_exponent):
    return [InfectedMacrophageBursts(bursting_rate, nodes, carrying_capacity, hill_exponent)]


class InfectedMacrophageBursts(Event):
    def __init__(self, reaction_parameter, nodes, carrying_capacity, hill_exponent):
        self._carrying_capacity = carrying_capacity
        self._hill_exponent = hill_exponent
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        # Account for possible division by zero
        if node[BACTERIUM_INTRACELLULAR] ** self._hill_exponent + \
           (self._carrying_capacity * node[MACROPHAGE_INFECTED]) ** self._hill_exponent == 0:
            return 0
        else:
            return node[MACROPHAGE_INFECTED] * (node[BACTERIUM_INTRACELLULAR] ** self._hill_exponent * 1.0 / (
                    node[BACTERIUM_INTRACELLULAR] ** self._hill_exponent + (
                    self._carrying_capacity * node[MACROPHAGE_INFECTED]) ** self._hill_exponent))

    def _update_node(self, node):
        bacteria_to_release = int(round(float(node[BACTERIUM_INTRACELLULAR]) / node[MACROPHAGE_INFECTED]))
        node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * bacteria_to_release,
                     BACTERIUM_SLOW: bacteria_to_release})
