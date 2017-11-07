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

    def __init__(self, compartments, ventilation, perfusion, edge_weight_within_lobe=1,
                 edge_weight_adjacent_lobe=1, lymphatic_drainage=None):
        """
        Create a new network
        :param compartments: Compartments within patches
        :param ventilation: Dictionary of ventilation values (key:zone number, value:ventilation value)
        :param perfusion: Dictionary of perfusion values (key:zone number, value:perfusion value)
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
        for segment_id in LUNG_BPS:
            # Get the West Zone for this patch
            zone = ZONE_FOR_SEGMENT[segment_id]

            # If patch has been specified for ventilation/perfusion, use the specified value
            try:
                if segment_id in ventilation:
                    vent = ventilation[segment_id]
                # Otherwise use the West Zone value specified
                else:
                    vent = ventilation[zone]
            except KeyError as e:
                raise KeyError(
                    "Please specify a value for ventilation of either patch {0} or West Zone {1}".format(segment_id,
                                                                                                         zone))
            try:
                if segment_id in perfusion:
                    perf = perfusion[segment_id]
                else:
                    perf = perfusion[zone]
            except KeyError as e:
                raise KeyError(
                    "Please specify a value for perfusion of either patch {0} or West Zone {1}".format(segment_id,
                                                                                                         zone))

            nodes[segment_id] = LungPatch(segment_id, compartments, vent, perf)
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
            adjacency = [RIGHT_INFERIOR_LOBE, RIGHT_MIDDLE_LOBE, RIGHT_SUPERIOR_LOBE, LEFT_SUPERIOR_LOBE, LEFT_INFERIOR_LOBE]
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
            for segment_id in LUNG_BPS:
                # Add a lymph edge from lymph to every BPS
                edges.append(LymphEdge(nodes[segment_id], nodes[LYMPH], lymphatic_drainage[segment_id]))
                # Add a blood edge from lymph to all BPS
                edges.append(BloodEdge(nodes[LYMPH], nodes[segment_id]))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)

    def get_standard_seeding(self, cell_recruitment_lung_rates, cell_recruitment_lymph_rates, death_rates):
        seeding = {}
        for node_id in LUNG_BPS + [LYMPH]:
            seeding[node_id] = {}
        # Lung seedings
        for cell, rate in cell_recruitment_lung_rates.iteritems():
            for n in LUNG_BPS:
                seeding[n][cell] = int(float(self[n].perfusion * rate / death_rates[cell]))
        # Lymph seedings
        for cell, rate in cell_recruitment_lymph_rates.iteritems():
            seeding[LYMPH][cell] = int(float(rate / death_rates[cell]))
        return seeding
