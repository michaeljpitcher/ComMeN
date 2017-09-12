import unittest
from PTBComMeN import *


class BacteriaChangeStateTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event_f = BacteriaChangeByOxygen(0.1, self.nodes, BACTERIUM_FAST)
        self.event_s = BacteriaChangeByOxygen(0.2, self.nodes, BACTERIUM_SLOW)
        uh = UpdateHandler([self.event_f, self.event_s])

    def test_rate(self):
        for e in [self.event_f, self.event_s]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event_f.rate, 0.1 * 2 * (1 / self.nodes[0].oxygen_tension))
        self.assertEqual(self.event_s.rate, 0)
        self.nodes[0].update({BACTERIUM_SLOW: 3})
        self.assertEqual(self.event_s.rate, 1.8)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_SLOW: 2, BACTERIUM_FAST: 3})
        self.event_f.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 3)
        self.event_s.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 3)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 2)


class GetBacteriaChangeEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.events = get_bacteria_change_events(self.nodes, {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2})

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        for a in self.events:
            self.assertTrue(isinstance(a, BacteriaChangeByOxygen))
            if a._compartment_from == BACTERIUM_FAST:
                self.assertEqual(a.reaction_parameter, 0.1)
            else:
                self.assertEqual(a.reaction_parameter, 0.2)

if __name__ == '__main__':
    unittest.main()
