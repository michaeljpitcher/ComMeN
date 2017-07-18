#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network import *
from LungComMeN.LungNetwork.LungPatch import *
from LungLobes import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TwoLungLobeMetapopulationNetwork(MetapopulationNetwork):
    """
    Network representing two human lungs (both right and left side). Contains all lung lobes and adjacent lobes
    have an edge connecting them (assume superior lobes on each lung are adjacent, i.e.
    INFERIOR_RIGHT - MIDDLE_RIGHT - SUPERIOR_RIGHT - SUPERIOR_LEFT - INFERIOR_LEFT).
    """

    def __init__(self, compartments, ventilation, perfusion):
        """
        Create a human dual lung model
        :param compartments: Compartments in lobe patches
        :param ventilation: Dictionary of ventilation attributes for nodes, key=node_id (lobe name)
        :param perfusion: Dictionary of perfusion attributes for nodes, key=node_id (lobe name)
        """
        nodes = []
        # Right lobes
        nodes.append(LungPatch(INFERIOR_RIGHT, compartments, ventilation[INFERIOR_RIGHT], perfusion[INFERIOR_RIGHT]))
        nodes.append(LungPatch(MIDDLE_RIGHT, compartments, ventilation[MIDDLE_RIGHT], perfusion[MIDDLE_RIGHT]))
        nodes.append(LungPatch(SUPERIOR_RIGHT, compartments, ventilation[SUPERIOR_RIGHT], perfusion[SUPERIOR_RIGHT]))
        #  Left lobes
        nodes.append(LungPatch(SUPERIOR_LEFT, compartments, ventilation[SUPERIOR_LEFT], perfusion[SUPERIOR_LEFT]))
        nodes.append(LungPatch(INFERIOR_LEFT, compartments, ventilation[INFERIOR_LEFT], perfusion[INFERIOR_LEFT]))

        # Edges
        edges = []
        for n in range(4):
            edges.append(Edge(nodes[n], nodes[n+1]))

        MetapopulationNetwork.__init__(self, nodes, edges)
