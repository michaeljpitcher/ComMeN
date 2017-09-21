#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Translocate import *
from LungComMeN.LungNetwork.PulmonaryEdge.BloodEdge import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BloodTranslocatePerfusion(Translocate):

    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        Translocate.__init__(self, reaction_parameter, nodes, compartment_translocating, edge_class=BloodEdge,
                             rate_increases_with_edges=False)

    def _pick_edge(self, edges):
        """
        Pick an edge, probabilistically based on perfusion
        :param edges: Edges to choose from
        :return: Edge chosen
        """
        total_perfusion = sum([e.perfusion for e in edges])
        r = rand.random() * total_perfusion
        running_total = 0
        for e in edges:
            running_total += e.perfusion
            if running_total >= r:
                return e
