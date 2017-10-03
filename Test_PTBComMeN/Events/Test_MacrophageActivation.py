import unittest
from PTBComMeN import *


class MacrophageActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.half_sat = 1.2
        self.event = MacrophageActivation(0.1, self.nodes, self.half_sat)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 2})
        self.assertAlmostEqual(self.event.rate, 0.1 * 3 * (2.0 / (2.0 + self.half_sat)))

    def test_update(self):
        self.nodes[0].update({T_CELL_ACTIVATED: 1, MACROPHAGE_REGULAR: 6})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 5)
        self.assertEqual(self.nodes[0][MACROPHAGE_ACTIVATED], 1)


class GetMacrophageActivationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rate = 0.1
        self.half_sat = 1.1
        self.events = get_macrophage_activation_events(self.nodes, self.rate, self.half_sat)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        for a in self.events:
            self.assertTrue(isinstance(a, Change))
            self.assertEqual(a.reaction_parameter, self.rate)
            self.assertEqual(a._half_sat, self.half_sat)


if __name__ == '__main__':
    unittest.main()
