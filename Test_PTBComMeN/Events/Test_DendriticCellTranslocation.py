import unittest
from PTBComMeN import *


class DendriticCellTranslocationMaturationTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3), LymphPatch(1, ALL_TB_COMPARTMENTS)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.half_sat = 20
        self.event = DendriticCellTranslocationMaturation(0.1, self.nodes, self.half_sat)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 3})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertAlmostEqual(self.event.rate, 0.1 * 3 * (2.0 / (2.0 + self.half_sat)))

        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 5, BACTERIUM_SLOW: 9})
        self.assertAlmostEqual(self.event.rate, 0.1 * 5 * (9.0 / (9.0 + self.half_sat)))

        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 4, BACTERIUM_SLOW: 9, BACTERIUM_FAST:12})
        self.assertAlmostEqual(self.event.rate, 0.1 * 4 * (21.0 / (21.0 + self.half_sat)))

    def test_update(self):
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 3, BACTERIUM_FAST: 10})
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 3)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_IMMATURE], 0)
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 0)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_MATURE], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 2)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_IMMATURE], 0)
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 0)
        self.assertEqual(self.nodes[1][DENDRITIC_CELL_MATURE], 1)


class GetDendriticCellTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.5)]
        self.edges = []
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.half_sat = 20
        self.events = get_dendritic_cell_translocation_maturation_events(self.nodes, 0.1, self.half_sat)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        self.assertTrue(isinstance(self.events[0], DendriticCellTranslocationMaturation))
        self.assertEqual(self.events[0].reaction_parameter, 0.1)
        self.assertEqual(self.events[0]._half_sat, self.half_sat)


if __name__ == '__main__':
    unittest.main()
