import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class BacteriaTranslocateTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]
        self.nodes = get_nodes(compartments)
        self.lungnodes = [n for n in self.nodes if isinstance(n, LungPatch)]
        self.lymphnodes = [n for n in self.nodes if isinstance(n, LymphPatch)]
        self.event_lung = BacteriaTranslocateLung(0.1, self.lungnodes, BACTERIUM_FAST)
        self.event_to_lymph = BacteriaTranslocateLungToLymph(0.2, self.lungnodes, BACTERIUM_FAST)
        self.event_from_lymph = BacteriaTranslocateLymphToLung(0.3, self.lymphnodes, BACTERIUM_FAST)
        u = UpdateHandler([self.event_from_lymph, self.event_lung, self.event_to_lymph])

    def test_state_variable(self):
        for e in [self.event_from_lymph, self.event_lung, self.event_to_lymph]:
            self.assertEqual(e.rate, 0)
        self.lungnodes[0].update({BACTERIUM_FAST: 1})
        self.assertEqual(self.event_lung.rate, 0.1 * 1 * 1.3)
        self.assertEqual(self.event_to_lymph.rate, 0.2 * 1 * 1.4)
        self.assertEqual(self.event_from_lymph.rate, 0)

        self.lymphnodes[0].update({BACTERIUM_FAST: 1})
        self.assertEqual(self.event_lung.rate, 0.1 * 1 * 1.3)
        self.assertEqual(self.event_to_lymph.rate, 0.2 * 1 * 1.4)
        self.assertEqual(self.event_from_lymph.rate, 0.3 * 1)

    def test_perform(self):
        self.lungnodes[0].update({BACTERIUM_FAST: 1})
        self.event_lung.perform()
        self.assertEqual(self.lungnodes[0][BACTERIUM_FAST], 0)
        self.assertEqual(self.lungnodes[1][BACTERIUM_FAST], 1)
        self.event_to_lymph.perform()
        self.assertEqual(self.lungnodes[1][BACTERIUM_FAST], 0)
        self.assertEqual(self.lymphnodes[1][BACTERIUM_FAST], 1)
        self.event_from_lymph.perform()
        self.assertEqual(self.lungnodes[1][BACTERIUM_FAST], 1)
        self.assertEqual(self.lymphnodes[1][BACTERIUM_FAST], 0)


if __name__ == '__main__':
    unittest.main()
