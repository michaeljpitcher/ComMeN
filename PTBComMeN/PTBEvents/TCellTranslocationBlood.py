#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungNetwork.PulmonaryPatch.LymphPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


T_CELL_TRANSLOCATION_OPTIONS = [T_CELL_ACTIVATED]


def get_t_cell_translocation_events(lymph_nodes, rate):
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Nodes must be instances of LymphPatch class"
    events = []
    events.append(TCellTranslocationBlood(rate, lymph_nodes))
    return events


class TCellTranslocationBlood(BloodTranslocatePerfusion):
    def __init__(self, reaction_parameter, nodes):
        BloodTranslocatePerfusion.__init__(self, reaction_parameter, nodes, T_CELL_ACTIVATED)

    def _pick_edge(self, edges):
        nodes = [edge.nodes[1] for edge in edges]
        total_m_i = sum(n[MACROPHAGE_INFECTED] for n in nodes)
        if total_m_i == 0:
            return BloodTranslocatePerfusion._pick_edge(self, edges)
        else:
            total = sum(n[MACROPHAGE_INFECTED] * n.perfusion for n in nodes)
            counter = 0
            r = rand.random() * total
            for c in range(len(edges)):
                counter += nodes[c][MACROPHAGE_INFECTED] * nodes[c].perfusion
                if counter >= r:
                    return edges[c]
