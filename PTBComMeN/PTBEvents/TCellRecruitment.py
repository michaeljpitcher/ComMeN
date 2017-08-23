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


def get_t_cell_recruitment_events(lymph_nodes, standard_lymph_rate, external_rates=None):
    events = [TCellRecruitmentLymph(standard_lymph_rate, lymph_nodes)]
    if external_rates:
        for external, rate in external_rates.iteritems():
            events.append(TCellRecruitmentLymph(rate, lymph_nodes, external))
    return events


class TCellRecruitmentLymph(Create):
    def __init__(self, reaction_parameter, nodes, external=None):
        Create.__init__(self, reaction_parameter, nodes, T_CELL_NAIVE, [external])