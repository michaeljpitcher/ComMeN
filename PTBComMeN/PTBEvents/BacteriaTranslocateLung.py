#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungNetwork.PulmonaryPatch import *

from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_bacteria_translocation_lung_events(lung_nodes, lung_rates):
    events = []
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for b in lung_rates:
        events.append(BacteriaTranslocateLung(lung_rates[b], lung_nodes, b))
    return events


class BacteriaTranslocateLung(LungTranslocateWeight):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LungTranslocateWeight.__init__(self, reaction_parameter, nodes, compartment_translocating)
