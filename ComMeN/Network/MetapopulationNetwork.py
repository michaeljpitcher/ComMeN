#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Patch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MetapopulationNetwork:
    """
    A collection of nodes (patch instances) joined by edges, which forms the basis of the metapopulation model
    """

    def __init__(self, nodes=None, edges=None):
        """
        Create a new network
        """
        # If nodes or edges provided, add them
        self.nodes = []
        if nodes:
            for n in nodes:
                self._add_node(n)
        self.edges = []
        if edges:
            for e in edges:
                self._add_edge(e)

    def _add_node(self, node):
        """
        Add a node (instance of patch class) to the network (must have unique node ID)
        :param node: Patch instance to add
        """
        assert node.node_id not in [n.node_id for n in self.nodes], \
            "Node ID {0} already exists in network".format(node.node_id)
        self.nodes.append(node)

    def _add_edge(self, edge):
        """
        Add an edge instance to the network
        :param edge: Edge to be added
        """
        # Pull nodes from edge instance, check they exist on this network object
        for n in edge.nodes:
            assert n in self.nodes, "Node {0} is not in the network".format(n)
        self.edges.append(edge)
