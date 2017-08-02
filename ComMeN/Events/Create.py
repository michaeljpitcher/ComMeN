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


class Create(Event):
    """
    Create event - a member of the specified compartment is created. Either a spontaneous creation, or created by
    members of compartments
    """
    def __init__(self, reaction_parameter, nodes, compartment_created, influencing_compartments=None):
        """
        New create event. Must specify the compartment created, may specify members of which compartments have created
        the new member (else spontaneous creation)
        :param reaction_parameter: Reaction parameter of event
        :param nodes: Nodes where creation occurs
        :param compartment_created: The compartment to add new member into
        :param influencing_compartments: Compartments whose members cause creation (if not specified, spontaneous
                                         creation)
        """
        self._compartment_created = compartment_created
        self._influencing_compartments = influencing_compartments
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        """
        The amount this node provides to the state variable. 1 if no influencing compartments specified, else sum of
        counts of specified compartments
        :param node: Node to calculate
        :return: State variable contribution of node
        """
        if self._influencing_compartments:
            # Sum all influencing compartments
            return sum([node[c] for c in self._influencing_compartments])
        else:
            # Spontaneous creation
            return 1

    def _update_node(self, node):
        """
        Update the node by adding a new member into the compartment
        :param node: Node to update
        """
        node.update({self._compartment_created: 1})
