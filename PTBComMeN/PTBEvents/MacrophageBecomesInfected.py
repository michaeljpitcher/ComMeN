#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Event import Event
from ..PulmonaryTBCompartments import *
import numpy.random as rand

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_becomes_infected_events(nodes, rate, half_sat):
    events = []
    events.append(MacrophageBecomesInfected(rate, nodes, half_sat))
    return events


class MacrophageBecomesInfected(Event):
    def __init__(self, reaction_parameter, nodes, half_sat):
        self._half_sat = half_sat
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        total_bacteria = node[BACTERIUM_EXTRACELLULAR_FAST] + node[BACTERIUM_EXTRACELLULAR_SLOW]
        if total_bacteria == 0:
            return 0
        return node[MACROPHAGE_REGULAR] * (float(total_bacteria) / (total_bacteria + self._half_sat))

    def _update_node(self, node):
        # TODO -Doesn't match Kirschner dynamics
        changes = {MACROPHAGE_REGULAR: -1, MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR_MACROPHAGE: 1}
        # To account for uncertain cause of infection, choose a bacterium at random from extracellular
        r = rand.random() * (node[BACTERIUM_EXTRACELLULAR_FAST] + node[BACTERIUM_EXTRACELLULAR_SLOW])
        if r <= node[BACTERIUM_EXTRACELLULAR_FAST]:
            changes[BACTERIUM_EXTRACELLULAR_FAST] = -1
        else:
            changes[BACTERIUM_EXTRACELLULAR_SLOW] = -1
        node.update(changes)
