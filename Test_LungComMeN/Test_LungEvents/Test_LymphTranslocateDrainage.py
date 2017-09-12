import unittest
from LungComMeN import *
import numpy as np


class LymphTranslocateDrainageTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a']

        self.nodes = [LungPatch(1, self.compartments, 1.0, 1.0),
                      LungPatch(2, self.compartments, 1.0, 1.0),
                      LungPatch(3, self.compartments, 1.0, 1.0),
                      LymphPatch(4, self.compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[3], 0.4), LymphEdge(self.nodes[1], self.nodes[3], 1.7)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = LymphTranslocateDrainage(0.1, self.nodes, self.compartments[0])
        uh = UpdateHandler([self.event])

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Translocate))
        self.assertEqual(self.event._compartment_translocating, self.compartments[0])
        self.assertEqual(self.event._edge_class, LymphEdge)
        self.assertTrue(self.event._rate_increases_with_edges)

    def test_calculate_state_variable_from_node(self):
        for n in self.nodes:
            self.assertEqual(self.event._calculate_state_variable_at_node(n), 0)
            n.update({self.compartments[0]: 1})

        self.assertEqual(self.event._calculate_state_variable_at_node(self.nodes[0]), 1 * 0.4)
        self.assertEqual(self.event._calculate_state_variable_at_node(self.nodes[1]), 1 * 1.7)
        self.assertEqual(self.event._calculate_state_variable_at_node(self.nodes[2]), 0)


if __name__ == '__main__':
    unittest.main()
