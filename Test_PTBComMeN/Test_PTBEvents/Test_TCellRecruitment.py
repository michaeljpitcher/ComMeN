import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class TCellRecruitmentTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_HELPER_NAIVE]
        self.nodes = get_nodes(compartments)
        self.event = TCellRecruitment(0.1, self.nodes, T_CELL_HELPER_NAIVE)
        u = UpdateHandler([self.event])

    def test_state_variable(self):
        self.assertEqual(self.event.rate, 0.1 * len(self.nodes))

    def test_perform(self):
        self.event.perform()
        total = sum([node[T_CELL_HELPER_NAIVE] for node in self.nodes])
        self.assertEqual(total, 1)
