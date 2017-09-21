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
MACROPHAGE_RECRUITMENT_OPTIONS = [STANDARD]
MACROPHAGE_RECRUITMENT_OPTIONS += [m for m in [MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED]]


def get_macrophage_recruitment_events(lung_nodes, lymph_nodes, lung_rates, lymph_rates):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = []
    for external, rate in lung_rates.iteritems():
        if external == STANDARD:
            events.append(MacrophageRecruitmentLung(rate, lung_nodes))
        else:
            events.append(MacrophageRecruitmentLung(rate, lung_nodes, external))
    for external, rate in lymph_rates.iteritems():
        if external == STANDARD:
            events.append(MacrophageRecruitmentLymph(rate, lymph_nodes))
        else:
            events.append(MacrophageRecruitmentLymph(rate, lymph_nodes, external))
    return events


class MacrophageRecruitmentLung(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes, external=None):
        if external:
            RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])
        else:
            RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)


class MacrophageRecruitmentLymph(Create):
    def __init__(self, reaction_parameter, nodes, external=None):
        if external:
            Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, [external])
        else:
            Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)
