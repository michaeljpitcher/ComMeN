#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_activation_events(nodes, influencers_rates):
    events = []
    for influencer, rate in influencers_rates.iteritems():
        events.append(MacrophageActivation(rate, nodes, influencer))
    return events


class MacrophageActivation(Change):
    def __init__(self, reaction_parameter, nodes, external=None):
        Change.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [external])
