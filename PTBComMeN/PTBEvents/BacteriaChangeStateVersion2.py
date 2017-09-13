#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.ChangeByOxygen import *
from LungComMeN.LungNetwork.LungPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

BACTERIA_CHANGE_STATE_OPTIONS = EXTRACELLULAR_BACTERIA


def get_bacteria_change_v2_events(lung_nodes, rates, sigmoid, half_sat):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Node must be instance of LungPatch"
    events = []
    for compartment in BACTERIA_CHANGE_STATE_OPTIONS:
        rate = rates[compartment]
        if compartment == BACTERIUM_FAST:
            events.append(BacteriaChangeByOxygenVersion2(rate, lung_nodes, BACTERIUM_FAST, BACTERIUM_SLOW, -1 * sigmoid,
                                                 half_sat))
        else:
            events.append(BacteriaChangeByOxygenVersion2(rate, lung_nodes, BACTERIUM_SLOW, BACTERIUM_FAST, sigmoid,
                                                         half_sat))
    return events


class BacteriaChangeByOxygenVersion2(ChangeByOxygenVersion2):
    def __init__(self, reaction_parameter, nodes, original_compartment, new_compartment, sigmoid, half_sat):
        ChangeByOxygenVersion2.__init__(self, reaction_parameter, nodes, original_compartment, new_compartment,
                                        sigmoid, half_sat)
