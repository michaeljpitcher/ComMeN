#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from PulmonaryPatch import *
from PulmonaryEdge import *
from BronchopulmonarySegments import *

from ComMeN.Network import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PulmonaryNetwork(MetapopulationNetwork):
    """
    Network representing the human lungs. Each patch represents a bronchopulmonary segment (BPS) of the lung. Lymphatic
    system is represented by a single lymph patch, which is connected to all BPS patches by a lymph edge. BPS are
    connected together based on the method chosen.
    """

    def __init__(self, compartments, ventilation, perfusion, edge_weight_within_lobe=1, edge_weight_adjacent_lobe=1,
                 lymphatic_drainage=None):
        """
        Create a new network
        :param compartments: Compartments within patches
        :param ventilation: Dictionary of ventilation values (key:patch ID, value:ventilation value)
        :param perfusion: Dictionary of perfusion values (key:patch ID, value:perfusion value)
        :param edge_joining: How to join BPS
        """
        # Keep lists of node types for convenience
        self.lung_patches = []
        self.lymph_patches = []

        nodes = {}
        edges = []

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # BPS network

        # Node for every BPS
        for segment_id in ALL_BPS:
            try:
                nodes[segment_id] = LungPatch(segment_id, compartments, ventilation[segment_id], perfusion[segment_id])
            except KeyError as e:
                raise KeyError("Patch {0} is missing value for ventilation/perfusion".format(e.message))
            self.lung_patches.append(nodes[segment_id])

        # Edges
        # Loop through all lobes (lobes is list of lists, each of which contains ID of BPS in a lobe)
        for lobe in LOBES:
            # In each lobe, add an edge between every BPS in lobe
            for index in range(len(lobe) - 1):
                bps_patch = nodes[lobe[index]]
                for index2 in range(index + 1, len(lobe)):
                    bps_patch2 = nodes[lobe[index2]]
                    edges.append(LungEdge(bps_patch, bps_patch2, edge_weight_within_lobe))
        if edge_weight_adjacent_lobe > 0.0:
            # Adjacent lobes list. Lobes next to each other are considered adjacent and may have an edge
            adjacency = [RIGHT_INFERIOR, RIGHT_MIDDLE, RIGHT_SUPERIOR, LEFT_SUPERIOR, LEFT_INFERIOR]
            for lobe_index in range(len(adjacency)-1):
                for BPS in adjacency[lobe_index]:
                    node1 = nodes[BPS]
                    for BPS2 in adjacency[lobe_index+1]:
                        node2 = nodes[BPS2]
                        edges.append(LungEdge(node1, node2, edge_weight_adjacent_lobe))

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
        # Lymph Network

        # Single node for the lymph system
        nodes[LYMPH] = LymphPatch(LYMPH, compartments)
        self.lymph_patches = [nodes[LYMPH]]

        if lymphatic_drainage:
            for segment_id in ALL_BPS:
                # Add a lymph edge from lymph to every BPS
                edges.append(LymphEdge(nodes[segment_id], nodes[LYMPH], lymphatic_drainage[segment_id]))
                # Add a blood edge from lymph to all BPS
                edges.append(BloodEdge(nodes[LYMPH], nodes[segment_id]))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)
