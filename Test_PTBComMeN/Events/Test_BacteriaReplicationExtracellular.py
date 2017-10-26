import unittest
from PTBComMeN import *


class ExtracellularBacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.event_f = ExtracellularBacteriaReplication(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        self.event_s = ExtracellularBacteriaReplication(0.2, self.nodes, BACTERIUM_EXTRACELLULAR_SLOW)
        uh = UpdateHandler([self.event_f, self.event_s])

    def test_rate(self):
        for e in [self.event_f, self.event_s]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 2})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_SLOW: 3})
        self.assertEqual(self.event_f.rate, 0.1 * 2)
        self.assertEqual(self.event_s.rate, 0.2 * 3)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 1, BACTERIUM_EXTRACELLULAR_SLOW: 3})
        self.event_f.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 3)

        self.event_s.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 4)


class GetBacteriaReplicationEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rates = {BACTERIUM_EXTRACELLULAR_FAST: 0.1, BACTERIUM_EXTRACELLULAR_SLOW: 0.2}
        self.events = get_bacteria_replication_extracellular_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        ext_events = [n for n in self.events if isinstance(n, ExtracellularBacteriaReplication)]
        self.assertEqual(len(ext_events), 2)
        fast = next(n for n in ext_events if n._compartment_created == BACTERIUM_EXTRACELLULAR_FAST)
        self.assertEqual(fast.reaction_parameter, 0.1)

        slow = next(n for n in ext_events if n._compartment_created == BACTERIUM_EXTRACELLULAR_SLOW)
        self.assertEqual(slow.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
