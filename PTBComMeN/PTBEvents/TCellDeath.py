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

T_CELL_DEATH_OPTIONS = ALL_T_CELLS


def get_t_cell_death_events(nodes, standard_death_rates):
    events = []
    # Standard
    for t in ALL_T_CELLS:
        events.append(TCellDeath(standard_death_rates[t], nodes, t))
    return events


class TCellDeath(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed):
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)
