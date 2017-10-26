#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import *
from LungComMeN.LungNetwork.PulmonaryPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_dendritic_cell_maturation_antigen_events(nodes, antigen_producer_rates):
    events = []
    for producer, rate in antigen_producer_rates.iteritems():
        events.append(DendriticCellMaturationAntigen(rate, nodes, producer))
    return events


class DendriticCellMaturationAntigen(Change):
    def __init__(self, reaction_parameter, nodes, bacterium):
        self._bacterium = bacterium
        Change.__init__(self, reaction_parameter, nodes, DENDRITIC_CELL_IMMATURE, DENDRITIC_CELL_MATURE, [bacterium])
