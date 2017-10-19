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

STANDARD = 'standard'

MACROPHAGE_RECRUITMENT_LUNG_ENHANCED_OPTIONS = MACROPHAGE_RECRUITMENT_LYMPH_ENHANCED_OPTIONS = \
    [MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED]


def get_macrophage_recruitment_events(lung_nodes, lymph_nodes, standard_lung_rate, enhanced_lung_rates,
                                      standard_lymph_rate, enhanced_lymph_rates):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = []
    events.append(MacrophageRecruitmentLungStandard(standard_lung_rate, lung_nodes))
    for external, rate in enhanced_lung_rates.iteritems():
        events.append(MacrophageRecruitmentLungEnhanced(rate, lung_nodes, external))
    events.append(MacrophageRecruitmentLymphStandard(standard_lymph_rate, lymph_nodes))
    for external, rate in enhanced_lymph_rates.iteritems():
        events.append(MacrophageRecruitmentLymphEnhanced(rate, lymph_nodes, external))
    return events


class MacrophageRecruitmentLungStandard(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes):
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)


class MacrophageRecruitmentLungEnhanced(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes, external):
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])


class MacrophageRecruitmentLymphStandard(Create):
    def __init__(self, reaction_parameter, nodes):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)


class MacrophageRecruitmentLymphEnhanced(Create):
    def __init__(self, reaction_parameter, nodes, external):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])
