import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class BacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = get_nodes(compartments)
        self.events = [BacteriaReplicate(0.1, self.nodes, BACTERIUM_FAST),
                       BacteriaReplicate(0.2, self.nodes, BACTERIUM_SLOW),
                       BacteriaReplicate(0.3, self.nodes, BACTERIUM_INTRACELLULAR)]
        u = UpdateHandler(self.events)

    def test_state_variable(self):
        for e in self.events:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 1})
        self.assertEqual(self.events[0].rate, 0.1 * 1)
        self.assertEqual(self.events[1].rate, 0)
        self.assertEqual(self.events[2].rate, 0)
        self.nodes[1].update({BACTERIUM_SLOW: 2})
        self.assertEqual(self.events[0].rate, 0.1 * 1)
        self.assertEqual(self.events[1].rate, 0.2 * 2)
        self.assertEqual(self.events[2].rate, 0)
        self.nodes[2].update({BACTERIUM_INTRACELLULAR: 3})
        self.assertEqual(self.events[0].rate, 0.1 * 1)
        self.assertEqual(self.events[1].rate, 0.2 * 2)
        self.assertEqual(self.events[2].rate, 0.3 * 3)


if __name__ == '__main__':
    unittest.main()
