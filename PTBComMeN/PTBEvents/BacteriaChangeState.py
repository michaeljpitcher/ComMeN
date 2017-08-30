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


def get_bacteria_change_events(lung_nodes, rates):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Node must be instance of LungPatch"
    events = []
    for compartment in BACTERIA_CHANGE_STATE_OPTIONS:
        rate = rates[compartment]
        events.append(BacteriaChangeByOxygen(rate, lung_nodes, compartment))
    return events


class BacteriaChangeByOxygen(ChangeByOxygen):
    def __init__(self, reaction_parameter, nodes, original_compartment):
        if original_compartment == BACTERIUM_FAST:
            oxygen_low = True
            new_compartment = BACTERIUM_SLOW
        else:
            oxygen_low = False
            new_compartment = BACTERIUM_FAST
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, original_compartment, new_compartment, oxygen_low)
