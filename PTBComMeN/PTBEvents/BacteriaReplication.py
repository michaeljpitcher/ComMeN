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

BACTERIA_REPLICATION_OPTIONS = ALL_BACTERIA


def get_bacteria_replication_events(nodes, rates):
    events = []
    for compartment in BACTERIA_REPLICATION_OPTIONS:
        rate = rates[compartment]
        events.append(BacteriaReplication(rate, nodes, compartment))
    return events


class BacteriaReplication(Create):
    def __init__(self, reaction_parameter, nodes, compartment_replicating):
        Create.__init__(self, reaction_parameter, nodes, compartment_replicating, [compartment_replicating])
