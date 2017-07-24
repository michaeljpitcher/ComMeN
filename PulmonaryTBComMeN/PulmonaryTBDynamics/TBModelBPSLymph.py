#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Dynamics.Dynamics import *
from ComMeN.Events import *
from LungComMeN.LungNetwork.BPS.BPSLymphMetapopulationNetwork import *
from PulmonaryTBCompartments import *
from ..PulmonaryTBEvents import *
from LungComMeN.LungEvents import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModel2(Dynamics):
    def __init__(self, ventilations, perfusions):

        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR,
                        MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED,
                        T_CELL_HELPER, T_CELL_CYTOTOXIC]
        chemokine_compartments = [MACROPHAGE_INFECTED]

        network = BronchopulmonarySegmentSingleLymphMetapopulationNetwork(compartments, ventilations, perfusions)

        events = []




        Dynamics.__init__(self, network, events)