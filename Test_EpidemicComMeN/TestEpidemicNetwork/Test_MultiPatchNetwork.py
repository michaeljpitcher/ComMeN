import unittest

from EpidemicComMeN import *


class MultiPatchNetworkTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b','c']
        self.nodes = 10
        self.edges = [(0,1), (0,2), (2,3), (3,4), (4,5), (6,7), (7,8), (8,9), (0,9)]
        self.network = MultiPatchEpidemicNetwork(compartments, self.nodes, self.edges)

    def test_initialise(self):
        self.assertEqual(len(self.network.nodes), self.nodes)
        self.assertEqual(len(self.network.edges), len(self.edges))
        actual_edge_pairs = [(e.nodes[0].node_id, e.nodes[1].node_id) for e in self.network.edges]
        self.assertItemsEqual(self.edges, actual_edge_pairs)
