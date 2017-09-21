#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *
from LungComMeN.LungNetwork.PulmonaryPatch.LymphPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

STANDARD = 'standard'
T_CELL_RECRUITMENT_OPTIONS = [STANDARD, MACROPHAGE_INFECTED]


def get_t_cell_recruitment_events(lymph_nodes, lymph_rates):
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Nodes must be instances of LymphPatch class"
    events = []
    for external, rate in lymph_rates.iteritems():
        if external == STANDARD:
            events.append(TCellRecruitmentLymph(rate, lymph_nodes))
        else:
            events.append(TCellRecruitmentLymph(rate, lymph_nodes, external))
    return events


class TCellRecruitmentLymph(Create):
    def __init__(self, reaction_parameter, nodes, external=None):
        if external:
            Create.__init__(self, reaction_parameter, nodes, T_CELL_NAIVE, [external])
        else:
            Create.__init__(self, reaction_parameter, nodes, T_CELL_NAIVE)
