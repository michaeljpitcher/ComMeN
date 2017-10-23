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


def get_macrophage_recruitment_lung_enhanced_events(lung_nodes, enhanced_lung_rates):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    events = []
    for external, rate in enhanced_lung_rates.iteritems():
        events.append(MacrophageRecruitmentLungEnhanced(rate, lung_nodes, external))
    return events


class MacrophageRecruitmentLungEnhanced(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes, external):
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])
