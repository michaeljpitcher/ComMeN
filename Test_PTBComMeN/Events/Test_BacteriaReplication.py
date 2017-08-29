import unittest
from PTBComMeN import *


class BacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event_f = BacteriaReplication(0.1, self.nodes, BACTERIUM_FAST)
        self.event_s = BacteriaReplication(0.2, self.nodes, BACTERIUM_SLOW)
        self.event_i = BacteriaReplication(0.3, self.nodes, BACTERIUM_INTRACELLULAR)
        uh = UpdateHandler([self.event_f, self.event_s, self.event_i])

    def test_rate(self):
        for e in [self.event_f, self.event_s]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0)
        self.assertEqual(self.event_i.rate, 0)
        self.nodes[0].update({BACTERIUM_SLOW: 3})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0.2 * 3)
        self.assertEqual(self.event_i.rate, 0)
        self.nodes[0].update({BACTERIUM_INTRACELLULAR: 5})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0.2 * 3)
        self.assertEqual(self.event_i.rate, 0.3 * 5)


    def test_update(self):
        self.nodes[0].update({BACTERIUM_FAST: 1, BACTERIUM_SLOW: 3, BACTERIUM_INTRACELLULAR: 5})
        self.event_f.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 3)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.event_s.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.event_i.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 6)


class GetBacteriaReplicationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2, BACTERIUM_INTRACELLULAR: 0.3}
        self.events = get_bacteria_replication_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 3)
        for a in self.events:
            self.assertTrue(isinstance(a, Create))
            self.assertEqual(a.reaction_parameter, self.rates[a._compartment_created])


if __name__ == '__main__':
    unittest.main()
