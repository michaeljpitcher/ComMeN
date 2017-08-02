#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *
from LungComMeN.LungEvents.RecruitmentByPerfusion import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

# TODO - perfusion based?
class MacrophageRecruitment(Create):
    def __init__(self, reaction_parameter, nodes):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)


class MacrophageRecruitmentPerfusionBased(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes):
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR)


class MacrophageRecruitmentByCytokine(Create):
    def __init__(self, reaction_parameter, nodes, cytokine_compartments):
        Create.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, cytokine_compartments)


class MacrophageRecruitmentByCytokinePerfusionBased(RecruitmentByPerfusion):
    def __init__(self, reaction_parameter, nodes, cytokine_compartments):
        RecruitmentByPerfusion.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, cytokine_compartments)
