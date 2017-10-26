import unittest
from PTBComMeN import *


class DendriticCellTranslocationMaturationTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3), LymphPatch(1, ALL_TB_COMPARTMENTS)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = DendriticCellTranslocation(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 3})
        self.assertAlmostEqual(self.event.rate, 0.1 * 3 * 0.9)


    def test_update(self):
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 3})
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 3)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_MATURE], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 2)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_MATURE], 1)


class GetDendriticCellTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.5)]
        self.edges = []
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.events = get_dendritic_cell_translocation_events(self.nodes, 0.1)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        self.assertTrue(isinstance(self.events[0], DendriticCellTranslocation))
        self.assertEqual(self.events[0].reaction_parameter, 0.1)


if __name__ == '__main__':
    unittest.main()
