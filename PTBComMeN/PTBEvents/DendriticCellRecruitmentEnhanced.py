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


def get_dendritic_cell_recruitment_enhanced_events(lung_nodes, rate, half_sat):
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    events = [DendriticCellRecruitmentLungEnhancedByBacteria(rate, lung_nodes, half_sat)]
    return events


class DendriticCellRecruitmentLungEnhancedByBacteria(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes, half_sat):
        self._half_sat = half_sat
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, DENDRITIC_CELL_IMMATURE)

    def _calculate_state_variable_at_node(self, node):
        total_extracellular_bac = node[BACTERIUM_FAST] + node[BACTERIUM_SLOW]
        if total_extracellular_bac + self._half_sat == 0:
            return 0
        else:
            return float(total_extracellular_bac) / (total_extracellular_bac + self._half_sat)
