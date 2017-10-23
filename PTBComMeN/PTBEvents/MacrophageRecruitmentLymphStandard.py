#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.RecruitmentByPerfusion import *
from LungComMeN.LungNetwork.PulmonaryPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_recruitment_lymph_standard_events(lymph_nodes, standard_lymph_rate):
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = [MacrophageRecruitmentLymphStandard(standard_lymph_rate, lymph_nodes)]
    return events


class MacrophageRecruitmentLymphStandard(Create):
    def __init__(self, reaction_parameter, nodes):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)
