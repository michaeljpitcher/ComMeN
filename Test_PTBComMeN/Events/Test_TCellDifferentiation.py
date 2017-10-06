import unittest
from PTBComMeN import *


class TCellActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = TCellDifferentiationByInfectedMacrophages(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_NAIVE: 6})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event.rate, 1.8)

    def test_update(self):
        self.nodes[0].update({T_CELL_NAIVE: 6, BACTERIUM_FAST: 1, MACROPHAGE_INFECTED: 1})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 5)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)



class GetTCellActivationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.rate = 0.1
        self.events = get_t_cell_differentiation_events(self.nodes, self.rate)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        self.assertEqual(self.events[0].reaction_parameter, 0.1)
        self.assertTrue(isinstance(self.events[0], TCellDifferentiationByInfectedMacrophages))



if __name__ == '__main__':
    unittest.main()
