import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class TCellActivationTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_HELPER_NAIVE, T_CELL_HELPER_ACTIVATED, MACROPHAGE_INFECTED]
        self.nodes = get_nodes(compartments)
        self.event = TCellActivation(0.1, self.nodes, T_CELL_HELPER_NAIVE, T_CELL_HELPER_ACTIVATED, [MACROPHAGE_INFECTED])
        u = UpdateHandler([self.event])

    def test_state_variable(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_HELPER_NAIVE: 3})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 2})
        self.assertEqual(self.event.rate, 0.1 * 3 * 2)

    def test_perform(self):
        self.nodes[0].update({T_CELL_HELPER_NAIVE: 3, MACROPHAGE_INFECTED: 2})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_HELPER_NAIVE], 2)
        self.assertEqual(self.nodes[0][T_CELL_HELPER_ACTIVATED], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 2)
