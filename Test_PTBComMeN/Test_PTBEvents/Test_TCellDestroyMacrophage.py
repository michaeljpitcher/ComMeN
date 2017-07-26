import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class TCellDestroyMacrophageTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_CYTOTOXIC_ACTIVATED, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR, BACTERIUM_SLOW]
        self.nodes = get_nodes(compartments)
        self.event_destroy = TCellDestroysMacrophageDestroyInternals(0.1, self.nodes)
        self.event_release = TCellDestroysMacrophageReleaseInternals(0.2, self.nodes)
        u = UpdateHandler([self.event_destroy, self.event_release])

    def test_state_variable(self):
        self.assertEqual(self.event_destroy.rate, 0)
        self.assertEqual(self.event_release.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 2})
        self.assertEqual(self.event_destroy.rate, 0)
        self.assertEqual(self.event_release.rate, 0)
        self.nodes[0].update({T_CELL_CYTOTOXIC_ACTIVATED: 3})
        self.assertEqual(self.event_destroy.rate, 0.1 * 2 * 3)
        self.assertEqual(self.event_release.rate, 0.2 * 2 * 3)

    def test_perform(self):
        self.nodes[0].update({T_CELL_CYTOTOXIC_ACTIVATED: 3, MACROPHAGE_INFECTED: 2, BACTERIUM_INTRACELLULAR: 10})
        self.event_destroy.perform()
        self.assertEqual(self.nodes[0][T_CELL_CYTOTOXIC_ACTIVATED], 3)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 0)
        self.event_release.perform()
        self.assertEqual(self.nodes[0][T_CELL_CYTOTOXIC_ACTIVATED], 3)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 5)
