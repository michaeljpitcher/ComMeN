#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Dynamics.Dynamics import *
from ComMeN.Events import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LungDynamics(Dynamics):

    def __init__(self, network, events):
        Dynamics.__init__(self, network, events)

    def ventilation_seeding(self, bacteria_counts):
        total_ventilation = sum([n.ventilation for n in self._network.nodes])
        for bacterium_compartment in bacteria_counts:
            bacteria_to_deposit = bacteria_counts[bacterium_compartment]
            for i in range(bacteria_to_deposit):
                r = rand.random() * total_ventilation
                count = 0
                for n in self._network.nodes:
                    count += n.ventilation
                    if count > r:
                        n.update({bacterium_compartment: 1})
                        break
