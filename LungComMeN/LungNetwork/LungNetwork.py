#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network.MetapopulationNetwork import *
from LungPatch import *
import numpy.random as rand

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LungNetwork(MetapopulationNetwork):

    def __init__(self, nodes, edges):
        MetapopulationNetwork.__init__(self, nodes, edges)

    def ventilation_seeding(self, bacteria_counts):
        """
        Creating a seeding dictionary based on ventilation. Can be supplied to run method of dynamics to seed
        the network with preference given to nodes with greater ventilation value
        :param bacteria_counts: Dictionary of bacteria - key: bacteria compartment, value: amount to deposit
        :return: Dictionary: key: node, value: dict - key: bacteria compartment, value: count
        """
        seeding = dict()
        nodes = [n for n in self.nodes if isinstance(n, LungPatch)]
        total_ventilation = sum([n.ventilation for n in nodes])
        for bacterium_compartment, amount_to_deposit in bacteria_counts.itertools():
            for i in range(amount_to_deposit):
                r = rand.random() * total_ventilation
                count = 0
                for n in nodes:
                    count += n.ventilation
                    if count > r:
                        if n not in seeding:
                            seeding[n] = dict()
                        if bacterium_compartment not in seeding[n]:
                            seeding[n][bacterium_compartment] = 1
                        else:
                            seeding[n][bacterium_compartment] += 1
                        break
        return seeding
