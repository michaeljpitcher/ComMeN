#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Translocate import *
from ..LungNetwork.LymphEdge import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LymphTranslocateDrainage(Translocate):
    """
    Member moves along a lymphatic edge, state variable is based on drainage values of edges
    """
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        Translocate.__init__(self, reaction_parameter, nodes, compartment_translocating, edge_class=LymphEdge)

    def _calculate_state_variable_at_node(self, node):
        """
        Calulcate the state variable contribution from node, based on edges and thier drainage values
        :param node:
        :return: State variable contribution
        """
        # Pass to translocate to calculate state variable based on edges, then multiply by drainage value of all edges
        return Translocate._calculate_state_variable_at_node(self, node) * \
            sum([e.drainage for e in self._viable_edges(node)])

    def _pick_edge(self, edges):
        """
        Pick an edge, probabilistically based on drainage
        :param edges: Edges to choose from
        :return: Edge chosen
        """
        total_drainage = sum([e.drainage for e in edges])
        r = rand.random() * total_drainage
        running_total = 0
        for e in edges:
            running_total += e.drainage
            if running_total >= r:
                return e
