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

    def __init__(self, nodes, edges=None):
        """
        Create a new metapopulation network
        :param nodes: Nodes of network
        :param edges: Optional edges of network
        """
        # If nodes or edges provided, add them
        self.nodes = []
        for n in nodes:
            self._add_node(n)
        self.edges = []
        if edges:
            for e in edges:
                self._add_edge(e)

    def seed(self, seeding):
        """
        Seed the network with sub-populations
        :param seeding: Dict of seeding. Key=node_id, value=dict, key=compartment, value=subpopulation value
        :return:
        """
        for node_id in seeding:
            node = self.get_node_by_id(node_id)
            node.update(seeding[node_id])

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

    def get_node_by_id(self, node_id):
        """
        Given an ID, return a node
        :param node_id: The ID to find
        :return: The node to return
        """
        node = [n for n in self.nodes if n.node_id == node_id]
        # Check only one node found
        assert len(node) != 0, "Node ID {0} not found".format(node_id)
        assert len(node) < 2, "Too many nodes found for ID {0}: {1}".format(node_id, len(node))
        return node[0]
