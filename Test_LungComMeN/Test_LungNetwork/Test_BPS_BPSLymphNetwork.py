import unittest
from LungComMeN import *


class BronchopulmonarySegmentSingleLymphMetapopulationNetworkTestCase(unittest.TestCase):

    def setUp(self):

        compartments = ['a', 'b']

        rand.seed(101)

        self.vent = {}
        self.perf = {}
        for node_id in ALL_BPS:
            self.vent[node_id] = rand.randint(5, 10)
            self.perf[node_id] = rand.randint(0, 5)

        self.network = BronchopulmonarySegmentSingleLymphMetapopulationNetwork(compartments, self.vent, self.perf)

    def get_neighbour_ids(self, node_id, edge_type):
        return [edge[node_id].node_id for edge in self.network[node_id].adjacent_edges[edge_type]]

    def test_initialise(self):
        self.assertItemsEqual([n.node_id for n in self.network.nodes], ALL_BPS + [LYMPH])

        for n in ALL_BPS:
            node = self.network[n]
            self.assertEqual(node.ventilation, self.vent[n])
            self.assertEqual(node.perfusion, self.perf[n])

        for lobe in LOBES:
            for bps in lobe:
                expected_neighbours = list(lobe)
                expected_neighbours.remove(bps)
                actual_neighbours = self.get_neighbour_ids(bps, LungEdge)
                self.assertItemsEqual(expected_neighbours, actual_neighbours)
                actual_neighbours = self.get_neighbour_ids(bps, LymphEdge)
                self.assertItemsEqual([LYMPH], actual_neighbours)
