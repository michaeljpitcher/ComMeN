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


def get_dendritic_cell_standard_death_events(nodes, standard_rates):
    events = []
    # Standard
    for d in ALL_DENDRITIC_CELLS:
        rate = standard_rates[d]
        events.append(DendriticCellDeathStandard(rate, nodes, d))
    return events


class DendriticCellDeathStandard(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed):
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)

    def _update_node(self, node):
        if self._compartment_destroyed == DENDRITIC_CELL_MATURE:
            # TODO - assume bacteria inside are released
            bacs_inside = int(round(float(node[BACTERIUM_INTRACELLULAR_DENDRITIC]) / node[DENDRITIC_CELL_MATURE]))
            node.update({DENDRITIC_CELL_MATURE: -1, BACTERIUM_INTRACELLULAR_DENDRITIC: -1 * bacs_inside,
                         BACTERIUM_EXTRACELLULAR_SLOW: bacs_inside})
        else:
            Destroy._update_node(self, node)
