#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBDynamics.PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TCellDestroysMacrophage(Destroy):
    def __init__(self, reaction_parameter, nodes):
        Destroy.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, [T_CELL_CYTOTOXIC_ACTIVATED])
