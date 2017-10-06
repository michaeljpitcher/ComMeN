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


def get_macrophage_destroy_bacteria_events(nodes, regular_rates, activated_rates):
    events = []
    for bacterium in EXTRACELLULAR_BACTERIA:
        # Regular
        events.append(MacrophageDestroysBacteria(regular_rates[bacterium], nodes, bacterium, MACROPHAGE_REGULAR))
        # Activated
        events.append(MacrophageDestroysBacteria(activated_rates[bacterium], nodes, bacterium, MACROPHAGE_ACTIVATED))

    return events


class MacrophageDestroysBacteria(Destroy):
    def __init__(self, reaction_parameter, nodes, bacterium, macrophage):
        Destroy.__init__(self, reaction_parameter, nodes, bacterium, [macrophage])
