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


def get_macrophage_death_by_t_cell_events(nodes, t_cell_death_rate, half_sat):
    return [InfectedMacrophageDeathByTCell(t_cell_death_rate, nodes, half_sat)]


class InfectedMacrophageDeathByTCell(Event):
    def __init__(self, reaction_parameter, nodes, half_sat):
        self._half_sat = half_sat
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        # Check for zero division
        if node[MACROPHAGE_INFECTED] == 0:
            return 0
        else:
            t_cell_mac_ratio = float(node[T_CELL_ACTIVATED]) / node[MACROPHAGE_INFECTED]
            return node[MACROPHAGE_INFECTED] * (t_cell_mac_ratio / (t_cell_mac_ratio + self._half_sat))

    def _update_node(self, node):
        bacs_killed = int(round(float(node[BACTERIUM_INTRACELLULAR_MACROPHAGE]) / node[MACROPHAGE_INFECTED]))
        node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR_MACROPHAGE: -1 * bacs_killed})
