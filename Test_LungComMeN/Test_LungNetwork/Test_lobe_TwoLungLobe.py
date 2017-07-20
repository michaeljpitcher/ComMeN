import unittest
from LungComMeN import *


class TwoLungLobeMetapopulationNetworkTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b']
        self.vent = {INFERIOR_RIGHT: 1.5, MIDDLE_RIGHT: 1.0, SUPERIOR_RIGHT: 0.4, SUPERIOR_LEFT: 0.3,
                     INFERIOR_LEFT: 0.9}
        self.perf = {INFERIOR_RIGHT: 1.5, MIDDLE_RIGHT: 0.9, SUPERIOR_RIGHT: 0.1, SUPERIOR_LEFT: 0.2,
                     INFERIOR_LEFT: 1.1}
        self.network = TwoLungLobeMetapopulationNetwork(compartments, self.vent, self.perf)

    def get_neighbour_ids(self, node_id):
        return [edge[node_id].node_id for edge in self.network[node_id].adjacent_edges[LungEdge]]

    def test_initialise(self):
        self.assertItemsEqual([n.node_id for n in self.network.nodes],
                              [SUPERIOR_RIGHT, MIDDLE_RIGHT, INFERIOR_RIGHT, SUPERIOR_LEFT, INFERIOR_LEFT])

        self.assertEqual(len(self.network[INFERIOR_RIGHT].adjacent_edges[LungEdge]), 1)
        self.assertItemsEqual(self.get_neighbour_ids(INFERIOR_RIGHT), [MIDDLE_RIGHT])

        self.assertEqual(len(self.network[MIDDLE_RIGHT].adjacent_edges[LungEdge]), 2)
        self.assertItemsEqual(self.get_neighbour_ids(MIDDLE_RIGHT), [SUPERIOR_RIGHT, INFERIOR_RIGHT])

        self.assertEqual(len(self.network[SUPERIOR_RIGHT].adjacent_edges[LungEdge]), 2)
        self.assertItemsEqual(self.get_neighbour_ids(SUPERIOR_RIGHT), [SUPERIOR_LEFT, MIDDLE_RIGHT])

        self.assertEqual(len(self.network[SUPERIOR_LEFT].adjacent_edges[LungEdge]), 2)
        self.assertItemsEqual(self.get_neighbour_ids(SUPERIOR_LEFT), [INFERIOR_LEFT, SUPERIOR_RIGHT])

        self.assertEqual(len(self.network[INFERIOR_LEFT].adjacent_edges[LungEdge]), 1)
        self.assertItemsEqual(self.get_neighbour_ids(INFERIOR_LEFT), [SUPERIOR_LEFT])


if __name__ == '__main__':
    unittest.main()
