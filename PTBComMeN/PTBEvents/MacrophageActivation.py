#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_activation_events(nodes, rate, half_sat):
    return [MacrophageActivation(rate, nodes, half_sat)]

# TODO - assumes only T-cell activated causes macrophage activation


class MacrophageActivation(Change):
    def __init__(self, reaction_parameter, nodes, half_sat):
        self._half_sat = half_sat
        Change.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED)

    def _calculate_state_variable_at_node(self, node):
        if node[T_CELL_ACTIVATED] + self._half_sat == 0.0:
            return 0
        else:
            return node[MACROPHAGE_REGULAR] * (float(node[T_CELL_ACTIVATED]) / (node[T_CELL_ACTIVATED] + self._half_sat))
