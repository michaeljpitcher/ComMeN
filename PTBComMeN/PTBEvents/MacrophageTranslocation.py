#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *
from LungComMeN.LungNetwork.PulmonaryPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_translocation_events(lung_nodes, lymph_rate):
    events = [InfectedMacrophageTranslocateLymph(lymph_rate, lung_nodes)]
    return events


class InfectedMacrophageTranslocateLymph(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED)

    def _move(self, node, neighbour):
        internals_to_move = int(round(node[BACTERIUM_INTRACELLULAR] * 1.0 / node[MACROPHAGE_INFECTED]))
        node_changes = {MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * internals_to_move}
        neighbour_changes = {MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR: internals_to_move}
        node.update(node_changes)
        neighbour.update(neighbour_changes)
