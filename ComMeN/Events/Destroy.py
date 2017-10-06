#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import Event

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Destroy(Event):
    """
    Destroy event - a member of the specified compartment is destroyed. Either a spontaneous destruction, or destroyed
    by members of compartments
    """
    def __init__(self, reaction_parameter, nodes, compartment_destroyed, influencing_compartments=None):
        """
        New destroy event. Must specify the compartment from which member removed, may specify members of which
        compartments have destroyed the member (else spontaneous destruction)
        :param reaction_parameter: Reaction parameter of event
        :param nodes: Nodes where destruction occurs
        :param compartment_destroyed: The compartment to remove a member from
        :param influencing_compartments: Compartments whose members cause destruction (if not specified, spontaneous
                                         destruction)
        """
        self._compartment_destroyed = compartment_destroyed
        self._influencing_compartments = influencing_compartments
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        """
        The amount this node provides to the state variable. If no influencing compartments specified, value is count of
        the compartment to remove from, else count * sum of counts of influencing compartments
        :param node: Node to calculate
        :return: state variable contribution from this node
        """
        # Always depends on how many of compartment exist already
        state_variable = node[self._compartment_destroyed]
        # Multiply by influencing compartments, if specified
        if self._influencing_compartments:
            state_variable *= sum([node[c] for c in self._influencing_compartments])
        return state_variable

    def _update_node(self, node):
        """
        Update the node by removing a member from the compartment
        :param node: Node to update
        """
        node.update({self._compartment_destroyed: -1})
