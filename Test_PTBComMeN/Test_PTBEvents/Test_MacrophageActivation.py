import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class MacrophageActivationTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED, T_CELL_HELPER_ACTIVATED]
        self.nodes = get_nodes(compartments)
        self.event_spont = MacrophageSpontaneousActivation(0.1, self.nodes)
        self.event_cytok = MacrophageActivationByExternals(0.2, self.nodes, [MACROPHAGE_INFECTED])
        u = UpdateHandler([self.event_spont, self.event_cytok])

    def test_state_variable(self):
        self.assertEqual(self.event_spont.rate, 0)
        self.assertEqual(self.event_cytok.rate, 0)

        self.nodes[0].update({MACROPHAGE_REGULAR: 10})
        self.assertEqual(self.event_spont.rate, 0.1 * 10)
        self.assertEqual(self.event_cytok.rate, 0)

        self.nodes[0].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event_spont.rate, 0.1 * 10)
        self.assertEqual(self.event_cytok.rate, 0.2 * 10 * 7)

    def test_perform(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 10})
        self.event_spont.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 9)
        self.assertEqual(self.nodes[0][MACROPHAGE_ACTIVATED], 1)
        self.nodes[1].update({MACROPHAGE_INFECTED: 7})
        self.nodes[1].update({MACROPHAGE_REGULAR: 10})
        self.event_cytok.perform()
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 9)
        self.assertEqual(self.nodes[1][MACROPHAGE_ACTIVATED], 1)
