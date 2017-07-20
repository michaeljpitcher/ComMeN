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
        try:
            return [n for n in self.nodes if n.node_id == item][0]
        except IndexError:
            raise Exception, "Node with id '{0}' not found in network".format(item)

    def seed(self, seeding):
        """
        Seed the network with sub-populations
        :param seeding: Dict of seeding. Key=node_id, value=dict, key=compartment, value=subpopulation value
        :return:
        """
        for node_id in seeding:
            self[node_id].update(seeding[node_id])

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
