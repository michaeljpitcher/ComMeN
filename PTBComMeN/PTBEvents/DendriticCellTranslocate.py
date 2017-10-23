#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungNetwork.PulmonaryPatch import *

from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_dendritic_cell_translocation_maturation_events(lung_nodes, lymph_rate, half_sat):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    events = [DendriticCellTranslocationMaturation(lymph_rate, lung_nodes, half_sat)]
    return events

# TODO - no bacteria are uptaken

class DendriticCellTranslocationMaturation(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes, half_sat):
        self._half_sat = half_sat
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, DENDRITIC_CELL_IMMATURE)

    def _calculate_state_variable_at_node(self, node):
        total_extracellular_bac = node[BACTERIUM_FAST] + node[BACTERIUM_SLOW]
        if total_extracellular_bac + self._half_sat == 0:
            return 0
        else:
            return node[DENDRITIC_CELL_IMMATURE] * (float(total_extracellular_bac) /
                                                (total_extracellular_bac + self._half_sat))

    def _move(self, node, neighbour):
        node.update({DENDRITIC_CELL_IMMATURE: -1})
        # Add member to the neighbour
        neighbour.update({DENDRITIC_CELL_MATURE: 1})
