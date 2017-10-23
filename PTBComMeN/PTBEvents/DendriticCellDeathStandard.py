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


def get_dendritic_cell_standard_death_events(nodes, standard_rates):
    events = []
    # Standard
    for dendritic_cell_state, rate in standard_rates.iteritems():
        events.append(DendriticCellDeathStandard(rate, nodes, dendritic_cell_state))
    return events


class DendriticCellDeathStandard(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed):
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)
