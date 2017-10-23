#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.RecruitmentByPerfusion import *
from ..Dynamics.PTBComMeNCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


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
