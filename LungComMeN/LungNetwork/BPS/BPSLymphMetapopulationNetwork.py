#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network import *
from ..LungPatch import *
from ..LymphPatch import *
from ..LungEdge import *
from ..LymphEdge import *
from BronchopulmonarySegments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BronchopulmonarySegmentSingleLymphMetapopulationNetwork(MetapopulationNetwork):
    """
    Network representing the human lungs. Each bronchopulmonary segment (BPS) of the lung is a patch. All BPSs in a lobe
    are connected by a lung edge. Lymphatic system is represented by a single lymph patch, which is connected to all
    BPS patches by a lymph edge. Thus all BPS are connected, but travel from a BPS in one lobe to a BPS in a different
    lobe requires passage through the lymphatics.
    """

    def __init__(self, compartments, ventilation, perfusion):
        # Keep lists of node types for convenience
        self.BPS_nodes = []
        self.lymph_nodes = []

        # Node for every BPS
        nodes = {}
        for segment in ALL_BPS:
            nodes[segment] = LungPatch(segment, compartments, ventilation[segment], perfusion[segment])
            self.BPS_nodes.append(nodes[segment])
        # Single node for the lymph system
        nodes[LYMPH] = LymphPatch(LYMPH, compartments)
        self.lymph_nodes = [nodes[LYMPH]]

        # Edges
        edges = []
        # Loop through all lobes (lobes is list of lists, each of which contains ID of BPS in a lobe)
        for lobe in LOBES:
            # In each lobe, add an edge between every BPS in lobe
            for index in range(len(lobe)-1):
                BPS_patch = nodes[lobe[index]]
                for index2 in range(index+1, len(lobe)):
                    BPS_patch2 = nodes[lobe[index2]]
                    edges.append(LungEdge(BPS_patch, BPS_patch2, False, 1))

        for segment in ALL_BPS:
            edges.append(LymphEdge(nodes[LYMPH], nodes[segment], False, 1))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)