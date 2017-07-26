import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class MacrophageTranslocateTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_HELPER_ACTIVATED, T_CELL_CYTOTOXIC_ACTIVATED]
        self.nodes = get_nodes(compartments)
        self.lungnodes = [n for n in self.nodes if isinstance(n, LungPatch)]
        self.lymphnodes = [n for n in self.nodes if isinstance(n, LymphPatch)]
        self.event = TCellTranslocateLymphToLung(0.1, self.lymphnodes, T_CELL_CYTOTOXIC_ACTIVATED)
        u = UpdateHandler([self.event])

    def test_state_variable(self):
        self.assertEqual(self.event.rate, 0)
        self.lungnodes[0].update({T_CELL_CYTOTOXIC_ACTIVATED: 1})
        self.assertEqual(self.event.rate, 0)
        self.lymphnodes[0].update({T_CELL_CYTOTOXIC_ACTIVATED: 1})
        self.assertEqual(self.event.rate, 0.1 * 1)

if __name__ == '__main__':
    unittest.main()
