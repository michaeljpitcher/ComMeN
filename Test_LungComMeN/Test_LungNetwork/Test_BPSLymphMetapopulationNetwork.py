import unittest
from LungComMeN import *


def get_neighbour_ids(network, node_id, edge_type):
    return [edge[node_id].node_id for edge in network[node_id].adjacent_edges[edge_type]]


class BronchopulmonarySegmentSingleLymphMetapopulationNetworkTestCase(unittest.TestCase):

    def setUp(self):

        compartments = ['a', 'b']

        rand.seed(101)

        self.vent = {}
        self.perf = {}
        for node_id in LUNG_BPS:
            self.vent[node_id] = rand.randint(5, 10)
            self.perf[node_id] = rand.randint(1, 5)

        self.network_all = PulmonaryNetwork(compartments, self.vent, self.perf, JOINING_ALL)
        self.network_adjacent = PulmonaryNetwork(compartments, self.vent, self.perf, JOINING_ADJACENT_LOBE)
        self.network_lobe = PulmonaryNetwork(compartments, self.vent, self.perf, JOINING_LOBE)
        self.network_none = PulmonaryNetwork(compartments, self.vent, self.perf, JOINING_NONE)

    def test_initialise(self):
        self.assertItemsEqual([n.node_id for n in self.network_all.nodes], LUNG_BPS + [LYMPH])
        for node_id in LUNG_BPS:
            self.assertEqual(self.network_all[node_id].ventilation, self.vent[node_id])
            self.assertEqual(self.network_all[node_id].perfusion, self.perf[node_id])
        for p in self.network_all.lung_patches:
            self.assertTrue(isinstance(p, LungPatch))
        for p in self.network_all.lymph_patches:
            self.assertTrue(isinstance(p, LymphPatch))

        # Adjacent
        adjacency = [RIGHT_INFERIOR_LOBE, RIGHT_MIDDLE_LOBE, RIGHT_SUPERIOR_LOBE, LEFT_SUPERIOR_LOBE, LEFT_INFERIOR_LOBE]
        for p in RIGHT_INFERIOR_LOBE:
            expected = list(RIGHT_INFERIOR_LOBE) + list(RIGHT_MIDDLE_LOBE)
            expected.remove(p)
            self.assertItemsEqual(get_neighbour_ids(self.network_adjacent, p, LungEdge), expected)
        for i in range(1,4):
            for p in adjacency[i]:
                expected = list(adjacency[i]) + list(adjacency[i-1]) + list(adjacency[i+1])
                expected.remove(p)
                self.assertItemsEqual(get_neighbour_ids(self.network_adjacent, p, LungEdge), expected)
        for p in LEFT_INFERIOR_LOBE:
            expected = list(LEFT_INFERIOR_LOBE) + list(LEFT_SUPERIOR_LOBE)
            expected.remove(p)
            self.assertItemsEqual(get_neighbour_ids(self.network_adjacent, p, LungEdge), expected)

        # Lymph and blood edges
        for p in LUNG_BPS:
            self.assertTrue(LymphEdge in self.network_all[p].adjacent_edges.keys())
            self.assertEqual(len(self.network_all[p].adjacent_edges[LymphEdge]), 1)
            edge = self.network_all[p].adjacent_edges[LymphEdge][0]
            self.assertEqual(edge[p], self.network_all.lymph_patches[0])
            self.assertTrue(LymphEdge in self.network_all[p].adjacent_edges.keys())
            self.assertEqual(len(self.network_all[p].adjacent_edges[BloodEdge]), 1)
            edge = self.network_all[p].adjacent_edges[BloodEdge][0]
            self.assertEqual(edge[p], self.network_all.lymph_patches[0])

        self.assertItemsEqual(get_neighbour_ids(self.network_all, LYMPH, LymphEdge), LUNG_BPS)
        self.assertItemsEqual(get_neighbour_ids(self.network_all, LYMPH, BloodEdge), LUNG_BPS)