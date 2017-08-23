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


def get_phagocytosis_events(nodes, regular_infect_rates, regular_destroy_rates, infected_retain_rates,
                            activated_destroy_rates):
    events = []
    for bacterium in EXTRACELLULAR_BACTERIA:
        # Regular - infect
        events.append(PhagocytosisRetain(regular_infect_rates[bacterium], nodes, bacterium, MACROPHAGE_REGULAR))
        # Regular - destroy
        events.append(PhagocytosisDestroy(regular_destroy_rates[bacterium], nodes, bacterium, MACROPHAGE_REGULAR))
        # Activated - destroy only
        events.append(PhagocytosisDestroy(activated_destroy_rates[bacterium], nodes, bacterium, MACROPHAGE_ACTIVATED))
        # Infected - retain only
        events.append(PhagocytosisRetain(infected_retain_rates[bacterium], nodes, bacterium, MACROPHAGE_INFECTED))
    return events


class PhagocytosisDestroy(Destroy):
    def __init__(self, reaction_parameter, nodes, bacterium, macrophage):
        Destroy.__init__(self, reaction_parameter, nodes, bacterium, [macrophage])


class PhagocytosisRetain(Change):
    def __init__(self, reaction_parameter, nodes, bacterium, macrophage):
        self._macrophage = macrophage
        Change.__init__(self, reaction_parameter, nodes, bacterium, BACTERIUM_INTRACELLULAR, [macrophage])

    def _update_node(self, node):
        changes = {self._compartment_from: -1, BACTERIUM_INTRACELLULAR: 1}
        if self._macrophage == MACROPHAGE_REGULAR:
            changes[MACROPHAGE_REGULAR] = -1
            changes[MACROPHAGE_INFECTED] = 1
        node.update(changes)
