import unittest
from LungComMeN import *


class SingleLungLobeMetapopulationNetworkTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a', 'b']

        self.ventilation_right = {SUPERIOR_RIGHT: 0.2, MIDDLE_RIGHT: 1.0, INFERIOR_RIGHT: 1.5}
        self.perfusion_right = {SUPERIOR_RIGHT: 0.1, MIDDLE_RIGHT: 0.9, INFERIOR_RIGHT: 2.0}

        self.ventilation_left = {SUPERIOR_LEFT: 0.4, INFERIOR_LEFT: 1.0}
        self.perfusion_left = {SUPERIOR_LEFT: 0.1, INFERIOR_LEFT: 1.0}

        self.network_right = SingleLungLobeMetapopulationNetwork(compartments, self.ventilation_right,
                                                                 self.perfusion_right, True)
        self.network_left = SingleLungLobeMetapopulationNetwork(compartments, self.ventilation_left,
                                                                self.perfusion_left, False)

    def test_initialise(self):
        self.assertItemsEqual([n.node_id for n in self.network_right.nodes],
                              [SUPERIOR_RIGHT, MIDDLE_RIGHT, INFERIOR_RIGHT])
        self.assertItemsEqual([n.node_id for n in self.network_left.nodes],
                              [SUPERIOR_LEFT, INFERIOR_LEFT])
        for node_id in [SUPERIOR_RIGHT, MIDDLE_RIGHT, INFERIOR_RIGHT]:
            self.assertEqual(self.network_right[node_id].ventilation, self.ventilation_right[node_id])
            self.assertEqual(self.network_right[node_id].perfusion, self.perfusion_right[node_id])
        self.assertEqual(self.network_right[SUPERIOR_RIGHT].oxygen_tension, 0.2 - 0.1)
        self.assertEqual(self.network_right[MIDDLE_RIGHT].oxygen_tension, 1.0 - 0.9)
        self.assertEqual(self.network_right[INFERIOR_RIGHT].oxygen_tension, 0)

        self.assertEqual(len(self.network_right.edges), 2)

        self.assertItemsEqual(self.network_right[SUPERIOR_RIGHT].adjacent_edges.keys(), [LungEdge])
        self.assertEqual(len(self.network_right[SUPERIOR_RIGHT].adjacent_edges[LungEdge]), 1)
        edge_superior_middle = self.network_right[SUPERIOR_RIGHT].adjacent_edges[LungEdge][0]
        self.assertTrue(isinstance(edge_superior_middle, LungEdge))
        self.assertItemsEqual(edge_superior_middle.nodes,
                              [self.network_right[SUPERIOR_RIGHT], self.network_right[MIDDLE_RIGHT]])
        self.assertFalse(edge_superior_middle.directed)
        self.assertEqual(edge_superior_middle.weight, 0)

        self.assertItemsEqual(self.network_right[INFERIOR_RIGHT].adjacent_edges.keys(), [LungEdge])
        edge_inferior_middle = self.network_right[INFERIOR_RIGHT].adjacent_edges[LungEdge][0]
        self.assertTrue(isinstance(edge_inferior_middle, LungEdge))
        self.assertItemsEqual(edge_inferior_middle.nodes,
                              [self.network_right[INFERIOR_RIGHT], self.network_right[MIDDLE_RIGHT]])
        self.assertFalse(edge_inferior_middle.directed)
        self.assertEqual(edge_inferior_middle.weight, 0)

        self.assertEqual(len(self.network_right[MIDDLE_RIGHT].adjacent_edges[LungEdge]), 2)
        self.assertItemsEqual(self.network_right[MIDDLE_RIGHT].adjacent_edges[LungEdge], [edge_inferior_middle,
                                                                                          edge_superior_middle])

        self.assertEqual(len(self.network_left.edges), 1)
        self.assertItemsEqual(self.network_left[SUPERIOR_LEFT].adjacent_edges.keys(), [LungEdge])
        self.assertItemsEqual(self.network_left[INFERIOR_LEFT].adjacent_edges.keys(), [LungEdge])
        self.assertItemsEqual(self.network_left[SUPERIOR_LEFT].adjacent_edges[LungEdge],
                              self.network_left[INFERIOR_LEFT].adjacent_edges[LungEdge])

if __name__ == '__main__':
    unittest.main()
