#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Translocate import *
from ..LungNetwork.LungEdge import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LungTranslocateWeight(Translocate):
    """
    Member moves along a lung edge, state variable is based on weight values of edges
    """
    def __init__(self, reaction_parameter, nodes, compartment_translocating):
        Translocate.__init__(self, reaction_parameter, nodes, compartment_translocating, edge_class=LungEdge)

    # TODO: state variable doesn't affect node choice. Check accuracy of this.

    def _pick_edge(self, edges):
        """
        Pick an edge, probabilistically based on weight
        :param edges: Edges to choose from
        :return: Edge chosen
        """
        total_weight = sum([e.weight for e in edges])
        r = rand.random() * total_weight
        running_total = 0
        for e in edges:
            running_total += e.weight
            if running_total >= r:
                return e
