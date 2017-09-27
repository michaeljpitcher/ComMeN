import unittest
from PTBComMeN import *


class ExtracellularBacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event_f = ExtracellularBacteriaReplication(0.1, self.nodes, BACTERIUM_FAST)
        self.event_s = ExtracellularBacteriaReplication(0.2, self.nodes, BACTERIUM_SLOW)
        uh = UpdateHandler([self.event_f, self.event_s])

    def test_rate(self):
        for e in [self.event_f, self.event_s]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0)
        self.nodes[0].update({BACTERIUM_SLOW: 3})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0.2 * 3)
        self.nodes[0].update({BACTERIUM_INTRACELLULAR: 5})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0.2 * 3)

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


class IntracellularBacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_INTRACELLULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.carrying_capacity = 10
        self.hill_exponent = 2
        self.event_i = IntracellularBacteriaReplication(0.3, self.nodes, self.carrying_capacity, self.hill_exponent)
        uh = UpdateHandler([self.event_i])

    def test_rate(self):
        self.assertEqual(self.event_i.rate, 0)

        mi = 1
        bi = 1
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR: bi})
        self.assertEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi**self.hill_exponent) / (bi**self.hill_exponent +
                                                   (self.carrying_capacity * mi)**self.hill_exponent)))

        mi = 1
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR: bi})
        self.assertEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi ** self.hill_exponent) / (bi ** self.hill_exponent +
                                                 (self.carrying_capacity * mi) ** self.hill_exponent)))
        mi = 4
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR: bi})
        self.assertAlmostEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi ** self.hill_exponent) / (
                         bi ** self.hill_exponent + (self.carrying_capacity * mi) ** self.hill_exponent)))

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR: 5})
        self.event_i.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 6)


class GetBacteriaReplicationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates_int = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2}
        self.rate_ext = 0.3
        self.carrying_capacity = 20
        self.hill_exponent = 2
        self.events = get_bacteria_replication_events(self.nodes, self.rates_int, self.rate_ext, self.carrying_capacity,
                                                      self.hill_exponent)

    def test_events(self):
        self.assertEqual(len(self.events), 3)
        ext_events = [n for n in self.events if isinstance(n, ExtracellularBacteriaReplication)]
        self.assertEqual(len(ext_events), 2)
        fast = next(n for n in ext_events if n._compartment_created == BACTERIUM_FAST)
        self.assertEqual(fast.reaction_parameter, 0.1)

        slow = next(n for n in ext_events if n._compartment_created == BACTERIUM_SLOW)
        self.assertEqual(slow.reaction_parameter, 0.2)

        int_events = [n for n in self.events if isinstance(n, IntracellularBacteriaReplication)]
        self.assertEqual(len(int_events), 1)
        int = int_events[0]
        self.assertEqual(int.reaction_parameter, 0.3)
        self.assertEqual(int._macrophage_carrying_capacity, self.carrying_capacity)


if __name__ == '__main__':
    unittest.main()
