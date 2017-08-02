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
            self.add_node(n)
        self.edges = []
        if edges:
            for e in edges:
                self.add_edge(e)

    def __getitem__(self, item):
        """
        Get the node in the network with the given ID
        :param item: Node ID to return
        :return: Node with ID
        """
        try:
            # Find the next node in node list with the given ID (should only be one by the add_node function)
            return next(n for n in self.nodes if n.node_id == item)
        except StopIteration:
            raise Exception, "Node with id '{0}' not found in network".format(item)

    def seed(self, seeding):
        """
        Seed the network with values for sub-populations of nodes
        :param seeding: Dict of seeding. Key=node_id, value=dict, key=compartment, value=subpopulation value
        """
        for node_id, node_seeding in seeding.iteritems():
            self[node_id].update(node_seeding)

    def add_node(self, node):
        """
        Add a node (instance of patch class) to the network (must have unique node ID)
        :param node: Patch instance to add
        """
        assert node.node_id not in [n.node_id for n in self.nodes], \
            "Node ID {0} already exists in network".format(node.node_id)
        self.nodes.append(node)

    def add_edge(self, edge):
        """
        Add an edge instance to the network
        :param edge: Edge to be added
        """
        # Pull nodes from edge instance, check they exist on this network object
        for n in edge.nodes:
            assert n in self.nodes, "Node {0} is not in the network".format(n)
        self.edges.append(edge)
        for n in edge.nodes:
            n.add_adjacent_edge(edge)
