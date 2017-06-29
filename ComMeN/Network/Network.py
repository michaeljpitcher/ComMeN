#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..Network import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Network:

    def __init__(self):
        self.nodes = []
        self.edges = []
        self._neighbours = dict()

    def add_node(self, node):
        assert isinstance(node, Patch), "Node {0} is not instance of Patch class".format(node)
        self.nodes.append(node)

    def add_edge(self, edge):
        node1 = edge.node1
        assert node1 in self.nodes
        node2 = edge.node2
        assert node2 in self.nodes
        self.edges.append(edge)
        node1.neighbours[node2] = edge
        node2.neighbours[node1] = edge
