import unittest
from PTBComMeN import *


class TCellTranslocationBloodTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_ACTIVATED]
        self.nodes = [LymphPatch(1, compartments), LungPatch(0, compartments, 0.9, 0.3)]
        self.edges = [BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = TCellTranslocationBlood(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)

    def test_update(self):
        self.nodes[0].update({T_CELL_ACTIVATED: 3})
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 3)
        self.assertEqual(self.nodes[1][T_CELL_ACTIVATED], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 2)
        self.assertEqual(self.nodes[1][T_CELL_ACTIVATED], 1)
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 1)
        self.assertEqual(self.nodes[1][T_CELL_ACTIVATED], 2)


class GetTCellTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_ACTIVATED]
        self.nodes = [LymphPatch(0, compartments)]
        self.rate = 0.1
        self.events = get_t_cell_translocation_events(self.nodes, self.rate)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        for e in self.events:
            self.assertTrue(isinstance(e, TCellTranslocationBlood))
        self.assertEqual(self.events[0].reaction_parameter, 0.1)


if __name__ == '__main__':
    unittest.main()
