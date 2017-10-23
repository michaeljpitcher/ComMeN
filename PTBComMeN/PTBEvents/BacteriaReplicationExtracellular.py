#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_bacteria_replication_extracellular_events(nodes, rates_extracellular):
    events = []
    for compartment in EXTRACELLULAR_BACTERIA:
        rate = rates_extracellular[compartment]
        events.append(ExtracellularBacteriaReplication(rate, nodes, compartment))
    return events


class ExtracellularBacteriaReplication(Create):
    def __init__(self, reaction_parameter, nodes, compartment_replicating):
        Create.__init__(self, reaction_parameter, nodes, compartment_replicating, [compartment_replicating])
