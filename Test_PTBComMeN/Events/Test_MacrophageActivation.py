import unittest
from PTBComMeN import *


class MacrophageActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageActivationByExternal(0.1, self.nodes, BACTERIUM_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event.rate, 3 * 2 * 0.1)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_FAST: 1, MACROPHAGE_REGULAR: 6})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 5)
        self.assertEqual(self.nodes[0][MACROPHAGE_ACTIVATED], 1)


class GetMacrophageActivationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2, T_CELL_ACTIVATED: 0.3}
        self.events = get_macrophage_activation_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), len(self.rates))
        for a in self.events:
            self.assertTrue(isinstance(a, Change))
            self.assertEqual(a.reaction_parameter, self.rates[a._influencing_compartments[0]])


if __name__ == '__main__':
    unittest.main()
