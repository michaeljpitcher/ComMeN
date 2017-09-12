#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class ChangeByOxygen(Change):
    """
    A member changes its compartment with probability based on the oxygen of the patch. Can be either change due to high
    or low oxygen.
    """

    def __init__(self, reaction_parameter, nodes, compartment_from, compartment_to, oxygen_low=True):
        """
        Create oxygen change event
        :param reaction_parameter:
        :param nodes:
        :param compartment_from:
        :param compartment_to:
        :param oxygen_low: If true, higher probability with lower oxygen, else higher probability with higher oxygen
        """
        self._oxygen_low = oxygen_low
        Change.__init__(self, reaction_parameter, nodes, compartment_from, compartment_to)

    def _calculate_state_variable_at_node(self, node):
        """
        State variable from node - change state variable * oxygen (if not oxygen low), else change state variable * (1 /
        oxygen)
        :param node:
        :return:
        """
        # TODO - review this RE case when oxygen == 0.
        if self._oxygen_low:
            # Avoid division by zero error by dividing by v. small value
            if node.oxygen_tension == 0:
                return Change._calculate_state_variable_at_node(self, node) * (1.0 / 0.00000000001)
            else:
                return Change._calculate_state_variable_at_node(self, node) * (1.0 / node.oxygen_tension)
        else:
            return Change._calculate_state_variable_at_node(self, node) * node.oxygen_tension


class ChangeByOxygenVersion2(Change):
    """
    A member changes its compartment with probability based on the oxygen of the patch.
    """

    def __init__(self, reaction_parameter, nodes, compartment_from, compartment_to, sigmoid, half_sat):
        """
        Create oxygen change event
        :param reaction_parameter:
        :param nodes:
        :param compartment_from:
        :param compartment_to:
        :param sigmoid:
        :param half_sat:
        """
        self._sigmoid = sigmoid
        self._half_sat = half_sat
        Change.__init__(self, reaction_parameter, nodes, compartment_from, compartment_to)

    def _calculate_state_variable_at_node(self, node):
        """
        State variable from node
        :param node:
        :return:
        """
        return (node[self._compartment_from] * (node.oxygen_tension ** self._sigmoid)) / \
               (self._half_sat ** self._sigmoid + node.oxygen_tension ** self._sigmoid)
