#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..PulmonaryTBCompartments import *
from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *
from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungNetwork.LungPatch import *
from LungComMeN.LungNetwork.LymphPatch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

MACROPHAGE_TRANSLOCATION_OPTIONS = ALL_MACROPHAGES


def _move_with_internals(compartment_translocating, node, neighbour):
    """
    Function to move the compartment along with any internals
    :param compartment_translocating:
    :param internal_compartment:
    :param node:
    :param neighbour:
    :return:
    """
    internals_to_move = int(round(node[BACTERIUM_INTRACELLULAR] * 1.0 / node[compartment_translocating]))
    node_changes = {compartment_translocating: -1, BACTERIUM_INTRACELLULAR: -1 * internals_to_move}
    neighbour_changes = {compartment_translocating: 1, BACTERIUM_INTRACELLULAR: internals_to_move}
    node.update(node_changes)
    neighbour.update(neighbour_changes)


def get_macrophage_translocation_events(lung_nodes, lymph_nodes, lung_rates, lymph_rates, blood_rates):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = []
    for m in ALL_MACROPHAGES:
        events.append(MacrophageTranslocateLung(lung_rates[m], lung_nodes, m))
        events.append(MacrophageTranslocateLymph(lymph_rates[m], lung_nodes, m))
        events.append(MacrophageTranslocateBlood(blood_rates[m], lymph_nodes, m))
    return events


class MacrophageTranslocateLung(LungTranslocateWeight):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LungTranslocateWeight.__init__(self, reaction_parameter, nodes, compartment_translocating)

    def _move(self, node, neighbour):
        if self._compartment_translocating == MACROPHAGE_INFECTED:
            _move_with_internals(self._compartment_translocating, node, neighbour)
        else:
            Translocate._move(self, node, neighbour)


class MacrophageTranslocateLymph(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, compartment_translocating)

    def _move(self, node, neighbour):
        if self._compartment_translocating == MACROPHAGE_INFECTED:
            _move_with_internals(self._compartment_translocating, node, neighbour)
        else:
            Translocate._move(self, node, neighbour)


class MacrophageTranslocateBlood(BloodTranslocatePerfusion):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        BloodTranslocatePerfusion.__init__(self, reaction_parameter, nodes, compartment_translocating)

    def _move(self, node, neighbour):
        if self._compartment_translocating == MACROPHAGE_INFECTED:
            _move_with_internals(self._compartment_translocating, node, neighbour)
        else:
            Translocate._move(self, node, neighbour)
