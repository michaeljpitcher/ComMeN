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


class SingleLungLobeMetapopulationNetwork(MetapopulationNetwork):
    """
    Network representing a single human lung (right/left side). Contains 3/2 lobes and adjacent lobes
    (Superior-Middle-Inferior / Superior-Inferior) have an edge connecting them.
    """

    def __init__(self, compartments, seeding, ventilation, perfusion, right=True):
        """
        Create a single human lung model
        :param compartments: Compartments in lobe patches
        :param seeding: Initial seeding of network compartments
        :param ventilation: Dictionary of ventilation attributes for nodes, key=node_id (lobe name)
        :param perfusion: Dictionary of perfusion attributes for nodes, key=node_id (lobe name)
        :param right: Is this model for the right lung? (False = left lung)
        """
        nodes = []

        if right:
            id_list = [SUPERIOR_RIGHT, MIDDLE_RIGHT, INFERIOR_RIGHT]
        else:
            id_list = [SUPERIOR_LEFT, INFERIOR_LEFT]

        for node_id in id_list:
            nodes.append(LungPatch(node_id, compartments, ventilation[node_id], perfusion[node_id]))

        # Edges
        edges = []

        if right:
            edges.append(Edge(nodes[0], nodes[1]))
            edges.append(Edge(nodes[1], nodes[2]))
        else:
            edges.append(Edge(nodes[0], nodes[1]))

        MetapopulationNetwork.__init__(self, nodes, edges, seeding)
