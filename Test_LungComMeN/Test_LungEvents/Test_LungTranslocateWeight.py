import unittest
from LungComMeN import *
import numpy as np


class LungTranslocateWeightTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a']

        self.nodes = [LungPatch(1, self.compartments, 1.0, 1.0),
                      LungPatch(2, self.compartments, 1.0, 1.0),
                      LungPatch(3, self.compartments, 1.0, 1.0)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.2), LungEdge(self.nodes[0], self.nodes[2], 0.3)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = LungTranslocateWeight(0.1, self.nodes, self.compartments[0])
        uh = UpdateHandler([self.event])

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Translocate))
        self.assertEqual(self.event._compartment_translocating, self.compartments[0])
        self.assertEqual(self.event._edge_class, LungEdge)
        self.assertTrue(self.event._rate_increases_with_edges)

    def test_pick_edge(self):
        np.random.seed(101)
        self.nodes[0].update({self.compartments[0]: 1})
        self.assertEqual(self.event.rate, 0.2)

        edge = self.event._pick_edge(self.edges)
        self.assertEqual(edge.nodes[0], self.nodes[0])
        self.assertEqual(edge.nodes[1], self.nodes[2])

        np.random.seed(5)
        edge = self.event._pick_edge(self.edges)
        self.assertEqual(edge.nodes[0], self.nodes[0])
        self.assertEqual(edge.nodes[1], self.nodes[1])


if __name__ == '__main__':
    unittest.main()
