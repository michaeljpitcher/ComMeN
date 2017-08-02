#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from MetapopulationNetwork import MetapopulationNetwork
from Patch import Patch
from Edge import Edge

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MultiPatchMetapopulationNetwork(MetapopulationNetwork):
    """
    A network of identical patches (no spatial attributes) with defined connections
    """
    def __init__(self, compartments, number_patches, connections):
        """
        Create a new multi-patch network
        :param compartments: Compartments of subpopulations of nodes
        :param number_patches: Number of nodes in network
        :param connections: Edge definitions - consists of (n1, n2) pairs integers, where 0 <= n1, n2 < number_patches
        """
        # Create the nodes
        nodes = [Patch(n, compartments) for n in range(number_patches)]
        edges = []
        # Create the edges
        for (n1, n2) in connections:
            edges.append(Edge(nodes[n1], nodes[n2]))
        MetapopulationNetwork.__init__(self, nodes, edges)
