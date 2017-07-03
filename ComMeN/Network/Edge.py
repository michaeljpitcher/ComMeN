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
        self.node1 = node_1
        self.node2 = node_2
        self.directed = directed
