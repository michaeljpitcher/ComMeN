#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network import *
from LungComMeN.LungNetwork.BronchopulmonarySegments import *
from LungComMeN.LungNetwork.BloodEdge import *
from LungComMeN.LungNetwork.LungEdge import *
from LungComMeN.LungNetwork.LungPatch import *
from LungComMeN.LungNetwork.LymphEdge import *
from LungComMeN.LungNetwork.LymphPatch import *

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


def get_inter_lobe_edges(nodes, weight=1):
    """
    Create edges between all bronchopulmonary segments in a lobe
    :param nodes:
    :param weight:
    :return:
    """
    edges = []
    # Loop through all lobes (lobes is list of lists, each of which contains ID of BPS in a lobe)
    for lobe in LOBES:
        # In each lobe, add an edge between every BPS in lobe
        for index in range(len(lobe) - 1):
            bps_patch = nodes[lobe[index]]
            for index2 in range(index + 1, len(lobe)):
                bps_patch2 = nodes[lobe[index2]]
                edges.append(LungEdge(bps_patch, bps_patch2, weight))
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
            edges.append(LungEdge(node1, node2, edge_weight))
    return edges


class BronchopulmonarySegmentSingleLymphMetapopulationNetwork(MetapopulationNetwork):
    """
    Network representing the human lungs. Each bronchopulmonary segment (BPS) of the lung is a patch. Lymphatic system
    is represented by a single lymph patch, which is connected to all BPS patches by a lymph edge. BPS are connected
    together based on the method chosen.
    """

    def __init__(self, compartments, ventilation, perfusion, edge_joining=JOINING_NONE):
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

        # Node for every BPS
        nodes = {}
        for segment_id in ALL_BPS:
            try:
                nodes[segment_id] = LungPatch(segment_id, compartments, ventilation[segment_id], perfusion[segment_id])
            except KeyError as e:
                raise KeyError("Patch {0} is missing value for ventilation/perfusion".format(e.message))
            self.lung_patches.append(nodes[segment_id])
        # Single node for the lymph system
        nodes[LYMPH] = LymphPatch(LYMPH, compartments)
        self.lymph_patches = [nodes[LYMPH]]

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

        for segment_id in ALL_BPS:
            # Add a lymph edge from lymph to every BPS
            edges.append(LymphEdge(nodes[segment_id], nodes[LYMPH], 1))
            # Add a blood edge from lymph to all BPS
            edges.append(BloodEdge(nodes[LYMPH], nodes[segment_id]))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)
