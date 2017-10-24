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


def get_macrophage_recruitment_lung_standard_events(lung_nodes, standard_lymph_rate):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    events = [MacrophageRecruitmentLungStandard(standard_lymph_rate, lung_nodes)]
    return events


class MacrophageRecruitmentLungStandard(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)
