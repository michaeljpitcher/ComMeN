import unittest
from PTBComMeN import *


class BacteriaChangeStateTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]

        self.sigmoid = 1.2
        self.half_sat = 1.0

        self.event_f = BacteriaChangeByOxygen(0.1, self.nodes, BACTERIUM_FAST, BACTERIUM_SLOW, -1 * self.sigmoid,
                                              self.half_sat)
        self.event_s = BacteriaChangeByOxygen(0.2, self.nodes, BACTERIUM_SLOW, BACTERIUM_FAST, self.sigmoid,
                                              self.half_sat)
        uh = UpdateHandler([self.event_f, self.event_s])

    def test_rate(self):
        for e in [self.event_f, self.event_s]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event_f.rate, 0.1 * (2 * (self.nodes[0].oxygen_tension ** (-1 * self.sigmoid))) / \
               (self.half_sat ** (-1 * self.sigmoid) + self.nodes[0].oxygen_tension ** (-1 * self.sigmoid)))
        self.assertEqual(self.event_s.rate, 0)
        self.nodes[0].update({BACTERIUM_SLOW: 5})
        self.assertEqual(self.event_s.rate, 0.2 * (5 * (self.nodes[0].oxygen_tension ** self.sigmoid)) / \
                         (self.half_sat ** self.sigmoid + self.nodes[0].oxygen_tension ** self.sigmoid))

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
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.sigmoid = 1.1
        self.half_sat = 1.2
        self.events = get_bacteria_change_events(self.nodes, {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2, SIGMOID:
                                                              self.sigmoid, HALF_SAT: self.half_sat})

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        fast_event = next(e for e in self.events if e._compartment_from == BACTERIUM_FAST)
        slow_event = next(e for e in self.events if e._compartment_from == BACTERIUM_SLOW)

        self.assertEqual(fast_event._compartment_to, BACTERIUM_SLOW)
        self.assertEqual(fast_event.reaction_parameter, 0.1)
        self.assertEqual(fast_event._sigmoid, -1 * self.sigmoid)
        self.assertEqual(fast_event._half_sat, self.half_sat)

        self.assertEqual(slow_event._compartment_to, BACTERIUM_FAST)
        self.assertEqual(slow_event.reaction_parameter, 0.2)
        self.assertEqual(slow_event._sigmoid, self.sigmoid)
        self.assertEqual(slow_event._half_sat, self.half_sat)


if __name__ == '__main__':
    unittest.main()
