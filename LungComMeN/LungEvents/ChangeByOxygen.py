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

    def __init__(self, reaction_parameter, nodes, compartment_from, compartment_to, oxygen_low=True):
        self._oxygen_low = oxygen_low
        Change.__init__(self, reaction_parameter, nodes, compartment_from, compartment_to)

    def _calculate_state_variable_at_node(self, node):
        if self._oxygen_low:
            return Change._calculate_state_variable_at_node(self, node) * (1.0 / node.oxygen_tension)
        else:
            return Change._calculate_state_variable_at_node(self, node) * node.oxygen_tension