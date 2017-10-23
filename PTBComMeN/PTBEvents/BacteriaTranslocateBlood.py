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


def get_bacteria_translocation_blood_events(lymph_nodes, blood_rates):
    events = []
    for n in lymph_nodes:
        assert isinstance(n, LymphPatch), "Patches must be instances of LymphPatch"
    for b in blood_rates:
        events.append(BacteriaTranslocateBlood(blood_rates[b], lymph_nodes, b))
    return events


class BacteriaTranslocateBlood(BloodTranslocatePerfusion):
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        BloodTranslocatePerfusion.__init__(self, reaction_parameter, nodes, compartment_translocating)
