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

EXTRACELLULAR_BACTERIA_REPLICATION_OPTIONS = EXTRACELLULAR_BACTERIA

REPLICATION_RATE_INTRACELLULAR = 'replication_rate_intracellular'
MACROPHAGE_CARRYING_CAPACITY = 'macrophage_internal_carrying_capcity'

INTRACELLULAR_BACTERIA_REPLICATION_OPTIONS = [REPLICATION_RATE_INTRACELLULAR, MACROPHAGE_CARRYING_CAPACITY]


def get_bacteria_replication_events(nodes, rates_extracellular, rate_intracellular, carrying_capacity, hill_exponent=2):
    events = []
    for compartment in EXTRACELLULAR_BACTERIA:
        rate = rates_extracellular[compartment]
        events.append(ExtracellularBacteriaReplication(rate, nodes, compartment))
    events.append(IntracellularBacteriaReplication(rate_intracellular, nodes, carrying_capacity, hill_exponent))
    return events


class ExtracellularBacteriaReplication(Create):
    def __init__(self, reaction_parameter, nodes, compartment_replicating):
        Create.__init__(self, reaction_parameter, nodes, compartment_replicating, [compartment_replicating])


class IntracellularBacteriaReplication(Create):
    def __init__(self, reaction_parameter, nodes, macrophage_carrying_capacity, hill_exponent):
        self._macrophage_carrying_capacity = macrophage_carrying_capacity
        self._hill_exponent = hill_exponent
        Create.__init__(self, reaction_parameter, nodes, BACTERIUM_INTRACELLULAR, [BACTERIUM_INTRACELLULAR])

    def _calculate_state_variable_at_node(self, node):
        # Need to cope for case when no intracellular bacteria to avoid division by 0 error
        if node[BACTERIUM_INTRACELLULAR] == 0:
            return 0
        else:
            return node[BACTERIUM_INTRACELLULAR] * (1 - (node[BACTERIUM_INTRACELLULAR]**self._hill_exponent * 1.0 /
                    (node[BACTERIUM_INTRACELLULAR]**self._hill_exponent +
                     (self._macrophage_carrying_capacity * node[MACROPHAGE_INFECTED])**self._hill_exponent)))
