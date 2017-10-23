import unittest
from PTBComMeN import *


class TCellActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, MACROPHAGE_INFECTED, BACTERIUM_FAST, DENDRITIC_CELL_MATURE]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event_mi = TCellDifferentiationByAPC(0.1, self.nodes, MACROPHAGE_INFECTED)
        self.event_dcm = TCellDifferentiationByAPC(0.2, self.nodes, DENDRITIC_CELL_MATURE)
        uh = UpdateHandler([self.event_mi, self.event_dcm])

    def test_rate(self):
        self.assertEqual(self.event_mi.rate, 0)
        self.assertEqual(self.event_dcm.rate, 0)
        self.nodes[0].update({T_CELL_NAIVE: 6})
        self.assertEqual(self.event_mi.rate, 0)
        self.assertEqual(self.event_dcm.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_mi.rate, 1.8)
        self.assertEqual(self.event_dcm.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 7})
        self.assertEqual(self.event_mi.rate, 1.8)
        self.assertEqual(self.event_dcm.rate, 8.4)

    def test_update(self):
        self.nodes[0].update({T_CELL_NAIVE: 6, BACTERIUM_FAST: 1, MACROPHAGE_INFECTED: 1})
        self.event_mi.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 5)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)


class GetTCellActivationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST, MACROPHAGE_INFECTED, DENDRITIC_CELL_MATURE]
        self.nodes = [LymphPatch(0, compartments)]
        self.rates = {MACROPHAGE_INFECTED: 0.1, DENDRITIC_CELL_MATURE: 0.2}
        self.events = get_t_cell_differentiation_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        mi = next(n for n in self.events if n._influencing_compartments[0] == MACROPHAGE_INFECTED)
        self.assertEqual(mi.reaction_parameter, 0.1)
        dcm = next(n for n in self.events if n._influencing_compartments[0] == DENDRITIC_CELL_MATURE)
        self.assertEqual(dcm.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
