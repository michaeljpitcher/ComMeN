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


def get_t_cell_differentiation_events(nodes, antigen_presenter_rates):
    events = []
    for apc, rate in antigen_presenter_rates.iteritems():
        events.append(TCellDifferentiationByAPC(rate, nodes, apc))
    return events


class TCellDifferentiationByAPC(Change):
    def __init__(self, reaction_parameter, nodes, antigen_presenting_cell):
        Change.__init__(self, reaction_parameter, nodes, T_CELL_NAIVE, T_CELL_ACTIVATED, [antigen_presenting_cell])
