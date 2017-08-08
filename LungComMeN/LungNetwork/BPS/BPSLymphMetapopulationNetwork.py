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


JOINING_LOBE = 'joining_lobe'
JOINING_ADJACENT_LOBE = 'joining_adjacent_lobe'
JOINING_ALL = 'joining_all'
JOINING_NONE = 'joining_none'


def get_inter_lobe_edges(nodes):
    """
    Create edges between all bronchopulmonary segments in a lobe
    :param nodes:
    :return:
    """
    edges = []
    # Loop through all lobes (lobes is list of lists, each of which contains ID of BPS in a lobe)
    for lobe in LOBES:
        # In each lobe, add an edge between every BPS in lobe
        for index in range(len(lobe) - 1):
            BPS_patch = nodes[lobe[index]]
            for index2 in range(index + 1, len(lobe)):
                BPS_patch2 = nodes[lobe[index2]]
                edges.append(LungEdge(BPS_patch, BPS_patch2, False, 1))
    return edges


def get_between_lobe_edges(nodes, lobe1, lobe2, edge_weight=1):
    """
    Create edges between nodes in two different lobes
    :param nodes:
    :param lobe1:
    :param lobe2:
    :param edge_weight:
    :return:
    """
    edges = []
    for BPS in lobe1:
        node1 = nodes[BPS]
        for BPS2 in lobe2:
            node2 = nodes[BPS2]
            edges.append(LungEdge(node1, node2, False, edge_weight))
    return edges


class BronchopulmonarySegmentSingleLymphMetapopulationNetwork(MetapopulationNetwork):
    """
    Network representing the human lungs. Each bronchopulmonary segment (BPS) of the lung is a patch. Lymphatic system
    is represented by a single lymph patch, which is connected to all BPS patches by a lymph edge. BPS are connected
    together based on the method chosen.
    """

    def __init__(self, compartments, ventilation, perfusion, edge_joining=None):
        """
        Create a new network
        :param compartments: Compartments within patches
        :param ventilation: Dictionary of ventilation values (key:patch ID, value:ventilation value)
        :param perfusion: Dictionary of perfusion values (key:patch ID, value:perfusion value)
        :param edge_joining: How to join BPS
        """
        # Keep lists of node types for convenience
        self.BPS_nodes = []
        self.lymph_nodes = []

        # Node for every BPS
        nodes = {}
        for segment_id in ALL_BPS:
            nodes[segment_id] = LungPatch(segment_id, compartments, ventilation[segment_id], perfusion[segment_id])
            self.BPS_nodes.append(nodes[segment_id])
        # Single node for the lymph system
        nodes[LYMPH] = LymphPatch(LYMPH, compartments)
        self.lymph_nodes = [nodes[LYMPH]]

        # Edges
        edges = []

        # TODO - edge weights
        if edge_joining == JOINING_LOBE:
            edges = get_inter_lobe_edges(nodes)
        elif edge_joining == JOINING_ADJACENT_LOBE:
            edges = get_inter_lobe_edges(nodes)
            # Adjacent lobes list. Lobes next to each other are considered adjacent and may have an edge
            adjacency = [RIGHT_INFERIOR, RIGHT_MIDDLE, RIGHT_SUPERIOR, LEFT_SUPERIOR, LEFT_INFERIOR]
            for lobe_index in range(len(adjacency)-1):
                edges += get_between_lobe_edges(nodes, adjacency[lobe_index], adjacency[lobe_index+1])
        elif edge_joining == JOINING_ALL:
            edges = get_inter_lobe_edges(nodes)
            for i in range(len(LOBES) - 1):
                for j in range(i+1, len(LOBES)):
                    edges += get_between_lobe_edges(nodes, LOBES[i], LOBES[j])
        elif edge_joining == JOINING_NONE:
            # No edges between any BPS
            pass
        else:
            raise Exception("Incorrect edge joining method: {0}".format(edge_joining))

        # Add a lymph edge from lymph to every BPS
        for segment_id in ALL_BPS:
            edges.append(LymphEdge(nodes[LYMPH], nodes[segment_id], False, 1))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)
