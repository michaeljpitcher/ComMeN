#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Translocate import *
from LungComMeN.LungNetwork.LymphEdge import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class DendriticTranslocation(Translocate):

    def __init__(self, reaction_parameter, nodes, bacterium):
        self._bacterium = bacterium
        Translocate.__init__(self, reaction_parameter, nodes, DENDRITIC_IMMATURE, LymphEdge, False,
                             EXTRACELLULAR_BACTERIA)

    def _update_node(self, node):
        """
        When immature dendritic translocates to lymph, it matures and becomes DENDRITIC MATURE
        :param node:
        :return:
        """
        # Choose an edge - should only be one
        chosen_edge = node.adjacent_edges[LymphEdge][0]
        # Remove immature DC and bacteria from the lung node
        node.update({DENDRITIC_IMMATURE: -1, self._bacterium: -1})
        # Get neighbour from edge
        neighbour = chosen_edge[node]
        # Add mature DC to the lymph neighbour
        neighbour.update({DENDRITIC_MATURE: 1})
