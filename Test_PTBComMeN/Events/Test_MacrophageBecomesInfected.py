import unittest
from PTBComMeN import *


class MacrophageBecomesInfectedTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.half_sat = 100
        self.event = MacrophageBecomesInfected(0.1, self.nodes, self.half_sat)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * (3.0 / (3.0 + 100)))

        a = self.event.rate
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_SLOW: 56})
        self.assertEqual(self.event.rate, 0.1 * 2 * (59.0 / (59.0 + 100)))

        b = self.event.rate
        self.assertTrue(b > a)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2, BACTERIUM_EXTRACELLULAR_FAST: 5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 4)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_MACROPHAGE], 1)


class GetMacrophageBecomesInfectedEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rate = 0.1
        self.half_sat = 100
        self.events = get_macrophage_becomes_infected_events(self.nodes, self.rate, self.half_sat)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        self.assertTrue(isinstance(self.events[0], MacrophageBecomesInfected))
        self.assertEqual(self.events[0].reaction_parameter, self.rate)
        self.assertEqual(self.events[0]._half_sat, self.half_sat)



if __name__ == '__main__':
    unittest.main()
