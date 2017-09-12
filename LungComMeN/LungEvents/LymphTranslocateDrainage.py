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
        Calculate the state variable contribution from node, based on edges and their drainage values
        :param node:
        :return: State variable contribution
        """
        # Get all acceptable edges
        viable_edges = self._viable_edges(node)
        # State variable depends on count of compartment
        state_variable = node[self._compartment_translocating]
        if state_variable == 0:
            return state_variable
        # Rate depends on the drainage values of lymph edges
        state_variable = state_variable * sum([n.drainage for n in viable_edges])

        return state_variable

    # TODO - only one lymph edge per lung patch, if changes, need a pick edge function
