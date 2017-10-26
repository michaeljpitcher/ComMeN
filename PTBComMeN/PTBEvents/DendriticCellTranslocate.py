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


def get_dendritic_cell_translocation_events(lung_nodes, lymph_rate):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    events = [DendriticCellTranslocation(lymph_rate, lung_nodes)]
    return events



class DendriticCellTranslocation(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, DENDRITIC_CELL_MATURE)

    def _move(self, node, neighbour):
        bac_to_move = int(round(float(node[BACTERIUM_INTRACELLULAR_DENDRITIC]) / node[DENDRITIC_CELL_MATURE]))
        node.update({DENDRITIC_CELL_MATURE: -1, BACTERIUM_INTRACELLULAR_DENDRITIC: -1 * bac_to_move})
        # Add member to the neighbour
        neighbour.update({DENDRITIC_CELL_MATURE: 1, BACTERIUM_INTRACELLULAR_DENDRITIC: bac_to_move})
