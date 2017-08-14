import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class BacteriaChangeTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW]
        nodes = get_nodes(compartments)
        self.viable_nodes = [n for n in nodes if isinstance(n, LungPatch)]
        self.event_f_to_s = OxygenChangeFastToSlow(0.1, self.viable_nodes)
        self.event_s_to_f = OxygenChangeSlowToFast(0.2, self.viable_nodes)
        e = UpdateHandler([self.event_f_to_s, self.event_s_to_f])

    def test_state_variable(self):
        self.assertEqual(self.event_f_to_s.rate, 0)
        self.assertEqual(self.event_s_to_f.rate, 0)

        self.viable_nodes[0].update({BACTERIUM_FAST: 1})
        self.assertEqual(self.event_f_to_s.rate, 0.1 * 1 * (1/self.viable_nodes[0].oxygen_tension))
        self.assertEqual(self.event_s_to_f.rate, 0)

        self.viable_nodes[1].update({BACTERIUM_SLOW: 1})
        self.assertEqual(self.event_s_to_f.rate, 0.2 * 1 * self.viable_nodes[1].oxygen_tension)
        self.assertEqual(self.event_f_to_s.rate, 0.1 * 1 * (1/self.viable_nodes[0].oxygen_tension))

    def test_perform_fast_to_slow(self):
        self.viable_nodes[0].update({BACTERIUM_FAST: 1})
        self.event_f_to_s.perform()
        self.assertEqual(self.viable_nodes[0][BACTERIUM_FAST], 0)
        self.assertEqual(self.viable_nodes[0][BACTERIUM_SLOW], 1)

    def perform_slow_to_fast(self):
        self.viable_nodes[1].update({BACTERIUM_SLOW: 1})
        self.event_s_to_f.perform()
        self.assertEqual(self.viable_nodes[1][BACTERIUM_SLOW], 0)
        self.assertEqual(self.viable_nodes[1][BACTERIUM_FAST], 1)

if __name__ == '__main__':
    unittest.main()

