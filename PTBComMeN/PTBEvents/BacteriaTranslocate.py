#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..PulmonaryTBCompartments import *
from LungComMeN.LungEvents.LungTranslocateWeight import *
from LungComMeN.LungEvents.LymphTranslocateDrainage import *
from LungComMeN.LungEvents.BloodTranslocatePerfusion import *
from LungComMeN.LungNetwork.LungPatch import *
from LungComMeN.LungNetwork.LymphPatch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def get_bacteria_translocation_events(lung_nodes, lymph_nodes, lung_rates, lymph_rates, blood_rates):
    events = []
    for n in lung_nodes:
        assert isinstance(n, LungPatch), "Patches must be instances of LungPatch"
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    for b in EXTRACELLULAR_BACTERIA:
        events.append(BacteriaTranslocateLung(lung_rates[b], lung_nodes, b))
        events.append(BacteriaTranslocateLymph(lymph_rates[b], lung_nodes, b))
        events.append(BacteriaTranslocateBlood(blood_rates[b], lymph_nodes, b))
    return events

class BacteriaTranslocateLung(LungTranslocateWeight):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LungTranslocateWeight.__init__(self, reaction_parameter, nodes, compartment_translocating)


class BacteriaTranslocateLymph(LymphTranslocateDrainage):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        LymphTranslocateDrainage.__init__(self, reaction_parameter, nodes, compartment_translocating)


class BacteriaTranslocateBlood(BloodTranslocatePerfusion):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        BloodTranslocatePerfusion.__init__(self, reaction_parameter, nodes, compartment_translocating)
