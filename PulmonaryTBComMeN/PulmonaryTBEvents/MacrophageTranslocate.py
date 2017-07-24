#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageTranslocateLung(LungTranslocateWeight):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LungTranslocateWeight.__init__(self, reaction_parameter, nodes, compartment_translocating)


class MacrophageTranslocateLungToLymph(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, compartment_translocating)


class MacrophageTranslocateLymphToLung(Translocate):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        Translocate.__init__(self, reaction_parameter, nodes, compartment_translocating, LymphEdge)
