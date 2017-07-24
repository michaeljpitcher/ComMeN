#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.ChangeByOxygen import *
from ..PulmonaryTBDynamics.PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class OxygenChangeFastToSlow(ChangeByOxygen):
    def __init__(self, reaction_parameter, nodes):
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, BACTERIUM_FAST, BACTERIUM_SLOW, True)


class OxygenChangeSlowToFast(ChangeByOxygen):
    def __init__(self, reaction_parameter, nodes):
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, BACTERIUM_SLOW, BACTERIUM_FAST, False)
