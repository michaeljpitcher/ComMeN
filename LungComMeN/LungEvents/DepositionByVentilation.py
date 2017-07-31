#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class DepositByVentilation(Create):
    """
    Create a new member of the compartment, inhaled into the lungs. Rate is dependent on the ventilation at the
    patch.
    """

    def __init__(self, reaction_parameter, nodes, compartment_created):
        """
        Create deposition event.
        :param reaction_parameter:
        :param nodes:
        :param compartment_created:
        """
        # No influencing compartments, as deposition comes from outside the patch and does not depend on what's inside,
        Create.__init__(self, reaction_parameter, nodes, compartment_created)

    def _calculate_state_variable_at_node(self, node):
        """
        State variable = standard create state variable * ventilation
        :param node:
        :return:
        """
        return Create._calculate_state_variable_at_node(self, node) * node.ventilation
