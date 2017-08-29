#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *
from LungComMeN.LungEvents.RecruitmentByPerfusion import *
from LungComMeN.LungNetwork.LungPatch import *
from LungComMeN.LungNetwork.LymphPatch import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_macrophage_recruitment_events(lung_nodes, lymph_nodes, standard_lung_rate, standard_lymph_rate,
                                      external_lung_rates=None, external_lymph_rates=None):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    events = [MacrophageRecruitmentLung(standard_lung_rate, lung_nodes),
              MacrophageRecruitmentLymph(standard_lymph_rate, lymph_nodes)]
    if external_lung_rates:
        for external, rate in external_lung_rates.iteritems():
            events.append(MacrophageRecruitmentLung(rate, lung_nodes, external))
    if external_lymph_rates:
        for external, rate in external_lymph_rates.iteritems():
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
