#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Event import Event
import numpy.random as rand
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Phagocytosis(Event):

    def __init__(self, reaction_parameter, nodes, macrophage, bacterium, probability_of_bacterial_survival):
        self._macrophage = macrophage
        self._bacterium = bacterium
        self._prob_survival = probability_of_bacterial_survival
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        return node[self._bacterium] * node[self._macrophage]

    def _update_node(self, node):
        changes = {self._bacterium: -1}
        r = rand.random()
        if r < self._prob_survival:
            changes[BACTERIUM_INTRACELLULAR] = 1
            if self._macrophage != MACROPHAGE_INFECTED:
                changes[self._macrophage] = -1
                changes[MACROPHAGE_INFECTED] = 1
        node.update(changes)
