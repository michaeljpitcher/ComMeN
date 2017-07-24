#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Change import *
from ..PulmonaryTBDynamics.PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageSpontaneousActivation(Change):
    def __init__(self, reaction_parameter, nodes):
        Change.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED)


class MacrophageActivationByChemokine(Change):
    def __init__(self, reaction_parameter, nodes, chemokine_compartments):
        Change.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED,
                        influencing_compartments=chemokine_compartments)


class MacrophageActivationByTCell(Change):
    def __init__(self, reaction_parameter, nodes):
        Change.__init__(self, reaction_parameter, nodes, MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED,
                        influencing_compartments=[T_CELL_HELPER_ACTIVATED])

# TODO: macrophage deactivation?