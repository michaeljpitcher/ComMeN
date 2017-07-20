#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungDynamics.LungDynamics import *
from LungTBCompartments import *
from LungComMeN.LungEvents import *
from LungComMeN.LungNetwork import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModel1(LungDynamics):
    """
    First TB model.
    - One lung (right)
    - V and Q set to give O values of Superior:0.49, Middle:0.3, Inferior:0
    - Only extracellular bacteria
    - Events are replication, change, movement
    """

    def __init__(self, replication_fast, replication_slow, change_fast_to_slow, change_slow_to_fast, fast_translocate,
                 slow_translocate):

        ventilation = {SUPERIOR_RIGHT: 0.5, MIDDLE_RIGHT: 1, INFERIOR_RIGHT: 1.5}
        perfusion = {SUPERIOR_RIGHT: 0.01, MIDDLE_RIGHT: 0.7, INFERIOR_RIGHT: 1.5}

        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW]

        network = SingleLungLobeMetapopulationNetwork(compartments, ventilation, perfusion, True)

        events = []
        # Replication
        events.append(Create(replication_fast, network.nodes, BACTERIUM_FAST, [BACTERIUM_FAST]))
        events.append(Create(replication_slow, network.nodes, BACTERIUM_SLOW, [BACTERIUM_FAST]))
        # Change
        events.append(ChangeByOxygen(change_fast_to_slow, network.nodes, BACTERIUM_FAST, BACTERIUM_SLOW, True))
        events.append(ChangeByOxygen(change_slow_to_fast, network.nodes, BACTERIUM_FAST, BACTERIUM_SLOW, False))
        # Translocate
        events.append(Translocate(fast_translocate, network.nodes, BACTERIUM_FAST, LungEdge, False))
        events.append(Translocate(slow_translocate, network.nodes, BACTERIUM_FAST, LungEdge, False))

        LungDynamics.__init__(self, network, events)
