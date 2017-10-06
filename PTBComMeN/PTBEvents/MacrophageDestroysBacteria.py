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
        events.append(RegularMacrophageDestroysBacteria(regular_rates[bacterium], nodes, bacterium,))
        # Activated
        events.append(ActivatedMacrophageDestroysBacteria(activated_rates[bacterium], nodes, bacterium))

    return events


class RegularMacrophageDestroysBacteria(Destroy):
    def __init__(self, reaction_parameter, nodes, bacterium):
        Destroy.__init__(self, reaction_parameter, nodes, bacterium, [MACROPHAGE_REGULAR])


class ActivatedMacrophageDestroysBacteria(Destroy):
    def __init__(self, reaction_parameter, nodes, bacterium):
        Destroy.__init__(self, reaction_parameter, nodes, bacterium, [MACROPHAGE_ACTIVATED])
