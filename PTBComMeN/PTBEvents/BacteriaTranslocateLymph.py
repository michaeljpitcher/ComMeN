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

BACTERIA_TRANSLOCATION_OPTIONS = EXTRACELLULAR_BACTERIA


def get_bacteria_translocation_lymph_events(lung_nodes, lymph_rates):
    events = []
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for b in lymph_rates:
        events.append(BacteriaTranslocateLymph(lymph_rates[b], lung_nodes, b))
    return events


class BacteriaTranslocateLymph(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, compartment_translocating)

