#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.ChangeByOxygen import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_bacteria_change_events(nodes, rates):
    events = []
    for compartment in EXTRACELLULAR_BACTERIA:
        rate = rates[compartment]
        events.append(BacteriaChangeByOxygen(rate, nodes, compartment))
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
