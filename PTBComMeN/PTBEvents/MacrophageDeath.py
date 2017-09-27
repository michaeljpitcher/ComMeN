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

MACROPHAGE_DEATH_OPTIONS = ALL_MACROPHAGES

def get_macrophage_death_events(nodes, standard_rates, t_cell_death_rate, bursting_rate, carrying_capacity, hill_exponent):
    events = []
    # Standard
    for m in ALL_MACROPHAGES:
        # TODO - assumes natural death of infected macrophage kills all internal bacteria
        events.append(MacrophageDeath(standard_rates[m], nodes, m))
    # By T-cell
    events.append(InfectedMacrophageDeathByTCell(t_cell_death_rate, nodes))
    # By bursting
    events.append(InfectedMacrophageBursts(bursting_rate, nodes, carrying_capacity, hill_exponent))
    return events


class MacrophageDeath(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed):
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)


class InfectedMacrophageDeathByTCell(Destroy):
    def __init__(self, reaction_parameter, nodes):
        Destroy.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, [T_CELL_ACTIVATED])


class InfectedMacrophageBursts(Event):
    def __init__(self, reaction_parameter, nodes, carrying_capacity, hill_exponent):
        self._carrying_capacity = carrying_capacity
        self._hill_exponent = hill_exponent
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        # Account for possible division by zero
        if node[MACROPHAGE_INFECTED] == 0:
            return 0
        else:
            return node[MACROPHAGE_INFECTED] * (node[BACTERIUM_INTRACELLULAR] ** self._hill_exponent * 1.0 / (
                    node[BACTERIUM_INTRACELLULAR] ** self._hill_exponent + (
                    self._carrying_capacity * node[MACROPHAGE_INFECTED]) ** self._hill_exponent))

    def _update_node(self, node):
        node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * self._carrying_capacity,
                     BACTERIUM_SLOW: self._carrying_capacity})
