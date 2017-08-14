import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class MacrophageRecruitmentTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = get_nodes(compartments)
        self.event = MacrophageRecruitment(0.1, self.nodes)
        self.event_cyto = MacrophageRecruitmentByCytokine(0.2, self.nodes, [MACROPHAGE_INFECTED])
        u = UpdateHandler([self.event, self.event_cyto])

    def test_state_variable(self):
        self.assertEqual(self.event.rate, 0.1 * len(self.nodes))
        self.assertEqual(self.event_cyto.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 2})
        self.assertEqual(self.event_cyto.rate, 0.2 * 2)
        self.nodes[1].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_cyto.rate, 0.2 * (2+3))

    def test_perform(self):
        self.event.perform()
        total = sum([self.nodes[n][MACROPHAGE_REGULAR] for n in range(0,4)])
        self.assertEqual(total, 1)

if __name__ == '__main__':
    unittest.main()
