#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Change(Event):
    """
    Change event - a member of one compartment changes to another
    """
    def __init__(self, reaction_parameter, nodes, compartment_from, compartment_to, influencing_compartments=None):
        """
        New change event. Must specify the compartment changing from and to, may specify members of which compartments
        have caused change (else spontaneous change)
        :param reaction_parameter: Reaction parameter of event
        :param nodes: Nodes where change occurs
        :param compartment_from: The compartment to remove member from
        :param compartment_to: Compartment to add new member into
        :param influencing_compartments: Compartments whose members cause change (if not specified, spontaneous
        change)
        """
        self._compartment_from = compartment_from
        self._compartment_to = compartment_to
        self._influencing_compartments = influencing_compartments
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        """
        The amount this node provides to the state variable. If no influencing compartments specified, value is count of
        compartment changing from, else value is count * sum of counts of influencing compartments
        counts of specified compartments
        :param node: Node to calculate
        :return:
        """
        state_variable = node[self._compartment_from]
        if self._influencing_compartments:
            state_variable = state_variable * sum([node[c] for c in self._influencing_compartments])
        return state_variable

    def _update_node(self, node):
        """
        Update the node by removing a member from one compartment and adding a member into another compartment
        :param node: Node to update
        :return:
        """
        node.update({self._compartment_from: -1, self._compartment_to: 1})
