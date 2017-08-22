#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import Change
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PhagocytosisInfect(Change):

    def __init__(self, reaction_parameter, nodes, macrophage, bacterium):
        self._macrophage = macrophage
        self._bacterium = bacterium
        Change.__init__(self, reaction_parameter, nodes, bacterium, BACTERIUM_INTRACELLULAR, [macrophage])

    def _update_node(self, node):
        changes = {self._bacterium: -1, BACTERIUM_INTRACELLULAR: 1}
        if self._macrophage == MACROPHAGE_REGULAR:
            changes[self._macrophage] = -1
            changes[MACROPHAGE_INFECTED] = 1
        node.update(changes)
