#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# imports

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Edge:
    """
    An edge connecting two nodes on the network in some way. Can be bi-directional or directed.
    """

    def __init__(self, node_1, node_2, directed=False):
        """
        Create a new edge. If directed == True, then assumed direction is from node 1 to node 2.
        :param node_1: Node on network
        :param node_2: Node on network
        :param directed: Does edge have a direction
        """
        self.nodes = [node_1, node_2]
        self.directed = directed
        node_1.add_adjacent_edge(self)
        node_2.add_adjacent_edge(self)

    def __getitem__(self, item):
        """
        Given a node or node_id, return the neighbour. I.e. instance[self.nodes[0]] returns self.nodes[1]
        :param item: Node
        :return:
        """
        if item == self.nodes[0] or item == self.nodes[0].node_id:
            return self.nodes[1]
        elif item == self.nodes[1] or item == self.nodes[1].node_id:
            return self.nodes[0]
        else:
            raise Exception("Node {0} is not on this edge".format(item))

    def __str__(self):
        """
        String version of edge is (node1.node_id, node2.node_id)
        :return:
        """
        return "(" + str(self.nodes[0].node_id) + ", " + str(self.nodes[1].node_id) + ")"
