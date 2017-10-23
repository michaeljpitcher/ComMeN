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


def get_macrophage_recruitment_lymph_enhanced_events(lymph_nodes, enhanced_lymph_rates):
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = []
    for external, rate in enhanced_lymph_rates.iteritems():
        events.append(MacrophageRecruitmentLymphEnhanced(rate, lymph_nodes, external))
    return events


class MacrophageRecruitmentLymphEnhanced(Create):
    def __init__(self, reaction_parameter, nodes, external):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])
