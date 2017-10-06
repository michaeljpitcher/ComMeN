#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import Change
from ComMeN.Events.Destroy import Destroy
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_becomes_infected_events(nodes, rates):
    events = []
    # TODO - no half-sat on this event
    for bacterium in EXTRACELLULAR_BACTERIA:
        events.append(MacrophageBecomesInfected(rates[bacterium], nodes, bacterium, MACROPHAGE_REGULAR))
    return events


class MacrophageBecomesInfected(Change):
    def __init__(self, reaction_parameter, nodes, bacterium, macrophage):
        Change.__init__(self, reaction_parameter, nodes, bacterium, BACTERIUM_INTRACELLULAR, [macrophage])

    def _update_node(self, node):
        changes = {self._compartment_from: -1, BACTERIUM_INTRACELLULAR: 1, MACROPHAGE_REGULAR: -1,
                   MACROPHAGE_INFECTED: 1}
        node.update(changes)
