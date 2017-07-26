import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class MacrophageTranslocateTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR]
        self.nodes = get_nodes(compartments)
        self.lungnodes = [n for n in self.nodes if isinstance(n, LungPatch)]
        self.lymphnodes = [n for n in self.nodes if isinstance(n, LymphPatch)]
        self.event_to_lymph = MacrophageTranslocateLungToLymph(0.2, self.lungnodes, MACROPHAGE_REGULAR)
        self.event_from_lymph = MacrophageTranslocateLymphToLung(0.3, self.lymphnodes, MACROPHAGE_REGULAR)
        u = UpdateHandler([self.event_from_lymph, self.event_to_lymph])

    def test_state_variable(self):
        for e in [self.event_from_lymph, self.event_to_lymph]:
            self.assertEqual(e.rate, 0)
        self.lungnodes[0].update({MACROPHAGE_REGULAR: 1})
        self.assertEqual(self.event_to_lymph.rate, 0.2 * 1 * 1.4)
        self.assertEqual(self.event_from_lymph.rate, 0)

        self.lymphnodes[0].update({MACROPHAGE_REGULAR: 1})
        self.assertEqual(self.event_to_lymph.rate, 0.2 * 1 * 1.4)
        self.assertEqual(self.event_from_lymph.rate, 0.3 * 1)

    def test_perform(self):
        self.lungnodes[0].update({MACROPHAGE_REGULAR: 1})
        self.event_to_lymph.perform()
        self.assertEqual(self.lungnodes[0][MACROPHAGE_REGULAR], 0)
        self.assertEqual(self.lymphnodes[0][MACROPHAGE_REGULAR], 1)
        self.event_from_lymph.perform()
        self.assertEqual(self.lungnodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.lymphnodes[0][MACROPHAGE_REGULAR], 0)

if __name__ == '__main__':
    unittest.main()
