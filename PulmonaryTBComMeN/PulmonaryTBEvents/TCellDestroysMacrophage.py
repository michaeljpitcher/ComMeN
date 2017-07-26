#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBDynamics.PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellDestroysMacrophageDestroyInternals(Destroy):
    def __init__(self, reaction_parameter, nodes):
        Destroy.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, [T_CELL_CYTOTOXIC_ACTIVATED])

    def _update_node(self, node):
        internal_bacteria = int(round(node[BACTERIUM_INTRACELLULAR] / float(node[MACROPHAGE_INFECTED])))
        node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * internal_bacteria})


class TCellDestroysMacrophageReleaseInternals(Destroy):
    def __init__(self, reaction_parameter, nodes):
        Destroy.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, [T_CELL_CYTOTOXIC_ACTIVATED])

    def _update_node(self, node):
        internal_bacteria = int(round(node[BACTERIUM_INTRACELLULAR] / float(node[MACROPHAGE_INFECTED])))
        node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * internal_bacteria,
                     BACTERIUM_SLOW: internal_bacteria})
