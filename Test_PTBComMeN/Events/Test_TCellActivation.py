import unittest
from PTBComMeN import *


class TCellActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = TCellActivationByExternal(0.1, self.nodes, MACROPHAGE_INFECTED)
        self.event2 = TCellActivationByExternal(0.2, self.nodes, BACTERIUM_FAST)
        uh = UpdateHandler([self.event, self.event2])

    def test_rate(self):
        for e in [self.event, self.event2]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({T_CELL_NAIVE: 6})
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(self.event2.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event.rate, 1.8)
        self.assertEqual(self.event2.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event.rate, 1.8)
        self.assertEqual(self.event2.rate, 0.2 * 2.0 * 6.0)

    def test_update(self):
        self.nodes[0].update({T_CELL_NAIVE: 6, BACTERIUM_FAST: 1, MACROPHAGE_INFECTED: 1})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 5)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.event2.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 4)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)


class GetTCellActivationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {BACTERIUM_FAST: 0.1, MACROPHAGE_INFECTED: 0.2}
        self.events = get_t_cell_activation_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), len(self.rates))
        for key,value in self.rates.iteritems():
            event = next(e for e in self.events if e._influencing_compartments[0] == key)
            self.assertTrue(isinstance(event, TCellActivationByExternal))
            self.assertEqual(event._compartment_from, T_CELL_NAIVE)
            self.assertEqual(event._compartment_to, T_CELL_ACTIVATED)
            self.assertEqual(event.reaction_parameter, value)


if __name__ == '__main__':
    unittest.main()
