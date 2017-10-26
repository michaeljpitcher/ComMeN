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


def get_dendritic_cell_maturation_bacterial_uptake_events(nodes, bacterium_rates):
    events = []
    for bacterium, rate in bacterium_rates.iteritems():
        events.append(DendriticCellMaturationBacteriaUptake(rate, nodes, bacterium))
    return events


class DendriticCellMaturationBacteriaUptake(Change):
    def __init__(self, reaction_parameter, nodes, bacterium):
        self._extracellular_bacterium = bacterium
        Change.__init__(self, reaction_parameter, nodes, DENDRITIC_CELL_IMMATURE, DENDRITIC_CELL_MATURE, [bacterium])

    def _update_node(self, node):
        node.update({DENDRITIC_CELL_IMMATURE: -1, DENDRITIC_CELL_MATURE: 1,
                     self._extracellular_bacterium: -1, BACTERIUM_INTRACELLULAR_DENDRITIC:1})