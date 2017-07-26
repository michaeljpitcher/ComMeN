import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class TCellDeathTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_HELPER_ACTIVATED]
        self.nodes = get_nodes(compartments)
        self.event = TCellDeath(0.1, self.nodes, T_CELL_HELPER_ACTIVATED)
        u = UpdateHandler([self.event])

    def test_state_variable(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_HELPER_ACTIVATED: 10})
        self.assertEqual(self.event.rate, 0.1 * 10)

    def test_perform(self):
        self.nodes[0].update({T_CELL_HELPER_ACTIVATED: 10})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_HELPER_ACTIVATED], 9)
