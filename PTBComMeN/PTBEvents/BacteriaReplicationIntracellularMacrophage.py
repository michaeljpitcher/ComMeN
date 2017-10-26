#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_bacteria_replication_intracellular_macrophage_events(nodes, rate_intracellular, carrying_capacity,
                                                             hill_exponent):
    events = [IntracellularBacteriaMacrophageReplication(rate_intracellular, nodes, carrying_capacity, hill_exponent)]
    return events


class IntracellularBacteriaMacrophageReplication(Create):
    def __init__(self, reaction_parameter, nodes, macrophage_carrying_capacity, hill_exponent):
        self._macrophage_carrying_capacity = macrophage_carrying_capacity
        self._hill_exponent = hill_exponent
        Create.__init__(self, reaction_parameter, nodes, BACTERIUM_INTRACELLULAR_MACROPHAGE,
                        [BACTERIUM_INTRACELLULAR_MACROPHAGE])

    def _calculate_state_variable_at_node(self, node):
        # Need to cope for case when no intracellular bacteria to avoid division by 0 error
        if node[BACTERIUM_INTRACELLULAR_MACROPHAGE] == 0:
            return 0
        else:
            return node[BACTERIUM_INTRACELLULAR_MACROPHAGE] * (1 - (node[BACTERIUM_INTRACELLULAR_MACROPHAGE]**self._hill_exponent * 1.0 /
                    (node[BACTERIUM_INTRACELLULAR_MACROPHAGE]**self._hill_exponent +
                     (self._macrophage_carrying_capacity * node[MACROPHAGE_INFECTED])**self._hill_exponent)))
