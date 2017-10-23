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


def get_t_cell_recruitment_standard_events(lymph_nodes, standard_rate):
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Nodes must be instances of LymphPatch class"
    events = [TCellRecruitmentStandard(standard_rate, lymph_nodes)]
    return events


class TCellRecruitmentStandard(Create):
    def __init__(self, reaction_parameter, nodes):
        Create.__init__(self, reaction_parameter, nodes, T_CELL_NAIVE)
