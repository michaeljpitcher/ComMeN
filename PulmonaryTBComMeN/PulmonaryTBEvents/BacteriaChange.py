#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.ChangeByOxygen import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class OxygenChangeFastToSlow(ChangeByOxygen):
    """
    Fast bacterium reverts to dormant state due to lack of oxygen
    """
    def __init__(self, reaction_parameter, nodes):
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, BACTERIUM_FAST, BACTERIUM_SLOW, True)


class OxygenChangeSlowToFast(ChangeByOxygen):
    """
    Slow bacterium re-activates to fast due to availability of oxygen
    """
    def __init__(self, reaction_parameter, nodes):
        ChangeByOxygen.__init__(self, reaction_parameter, nodes, BACTERIUM_SLOW, BACTERIUM_FAST, False)
