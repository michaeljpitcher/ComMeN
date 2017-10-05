#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_standard_death_events(nodes, standard_rates):
    events = []
    # Standard
    for m in ALL_MACROPHAGES:
        events.append(MacrophageDeathStandard(standard_rates[m], nodes, m))
    return events


class MacrophageDeathStandard(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed):
        # TODO - where's the bac death?
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)

    def _update_node(self, node):
        if self._compartment_destroyed == MACROPHAGE_INFECTED:
            bacs_killed = int(round(float(node[BACTERIUM_INTRACELLULAR]) / node[MACROPHAGE_INFECTED]))
            node.update({MACROPHAGE_INFECTED: -1, BACTERIUM_INTRACELLULAR: -1 * bacs_killed})
        else:
            Destroy._update_node(self, node)