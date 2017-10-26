#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.ChangeByOxygen import *
from LungComMeN.LungNetwork.PulmonaryPatch.LungPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

HALF_SAT = 'half_sat'
SIGMOID = 'sigmoid'
BACTERIA_CHANGE_STATE_OPTIONS = EXTRACELLULAR_BACTERIA + [HALF_SAT, SIGMOID]


def get_bacteria_change_events(lung_nodes, rates):
    for n in lung_nodes:
        # TODO - bacteria can't change in the lymph
        assert isinstance(n, LungPatch), "Node must be instance of LungPatch"
    events = []
    for compartment in EXTRACELLULAR_BACTERIA:
        rate = rates[compartment]
        if compartment == BACTERIUM_EXTRACELLULAR_FAST:
            events.append(BacteriaChangeByOxygen(rate, lung_nodes, BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW, -1 * rates[SIGMOID],
                                                 rates[HALF_SAT]))
        else:
            events.append(BacteriaChangeByOxygen(rate, lung_nodes, BACTERIUM_EXTRACELLULAR_SLOW, BACTERIUM_EXTRACELLULAR_FAST, rates[SIGMOID],
                                                 rates[HALF_SAT]))
    return events


class BacteriaChangeByOxygen(ChangeByOxygen):
    def __init__(self, reaction_parameter, nodes, original_compartment, new_compartment, sigmoid, half_sat):
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, original_compartment, new_compartment,
                                sigmoid, half_sat)
