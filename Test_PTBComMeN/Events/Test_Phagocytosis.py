import unittest
from PTBComMeN import *
from LungComMeN import *
import numpy.random as rand


class PhagocytosisTestCase(unittest.TestCase):

    def setUp(self):
        self.compartments = ALL_MACROPHAGES + ALL_BACTERIA
        self.node = LungPatch(0, self.compartments, 1, 1)
        self.network = MetapopulationNetwork([self.node], None)
        self.event_M_R_B_F = Phagocytosis(0.1, [self.node], MACROPHAGE_REGULAR, BACTERIUM_FAST, 0.5)
        self.event_M_R_B_S = Phagocytosis(0.2, [self.node], MACROPHAGE_REGULAR, BACTERIUM_SLOW, 0.3)
        self.event_M_A_B_F = Phagocytosis(0.3, [self.node], MACROPHAGE_ACTIVATED, BACTERIUM_FAST, 0.0)
        self.event_M_A_B_S = Phagocytosis(0.4, [self.node], MACROPHAGE_ACTIVATED, BACTERIUM_SLOW, 0.0)
        self.event_M_I_B_F = Phagocytosis(0.5, [self.node], MACROPHAGE_INFECTED, BACTERIUM_FAST, 1.0)
        self.event_M_I_B_S = Phagocytosis(0.6, [self.node], MACROPHAGE_INFECTED, BACTERIUM_SLOW, 1.0)
        self.events = [self.event_M_R_B_F, self.event_M_R_B_S, self.event_M_A_B_F, self.event_M_A_B_S,
                       self.event_M_I_B_F, self.event_M_I_B_S]

    def test_calc_state_var(self):
        for e in self.events:
            self.assertEqual(e.rate, 0)
        self.node.update({MACROPHAGE_REGULAR:1, MACROPHAGE_ACTIVATED: 2, MACROPHAGE_INFECTED: 3})
        for e in self.events:
            e.update_state_variable_from_node(self.node)
            self.assertEqual(e.rate, 0)
        self.node.update({BACTERIUM_FAST: 4, BACTERIUM_SLOW: 5})
        for e in self.events:
            e.update_state_variable_from_node(self.node)
        self.assertEqual(self.event_M_R_B_F.rate, 0.1 * 1 * 4)
        self.assertEqual(self.event_M_R_B_S.rate, 0.2 * 1 * 5)
        self.assertEqual(self.event_M_A_B_F.rate, 0.3 * 2 * 4)
        self.assertEqual(self.event_M_A_B_S.rate, 0.4 * 2 * 5)
        self.assertEqual(self.event_M_I_B_F.rate, 0.5 * 3 * 4)
        self.assertEqual(self.event_M_I_B_S.rate, 0.6 * 3 * 5)

    def test_update(self):
        rand.seed(101)
        self.node.update({MACROPHAGE_REGULAR: 6, MACROPHAGE_ACTIVATED: 6, MACROPHAGE_INFECTED: 6,
                          BACTERIUM_FAST: 10, BACTERIUM_SLOW: 10})
        for e in self.events:
            e.update_state_variable_from_node(self.node)
        self.event_M_R_B_F.perform()
        self.assertEqual(self.node[BACTERIUM_FAST], 9)
        self.assertEqual(self.node[BACTERIUM_SLOW], 10)
        self.assertEqual(self.node[MACROPHAGE_REGULAR], 6)
        self.assertEqual(self.node[MACROPHAGE_INFECTED], 6)
        self.assertEqual(self.node[BACTERIUM_INTRACELLULAR], 0)

        self.node.reset()
        rand.seed(10)
        self.node.update({MACROPHAGE_REGULAR: 6, MACROPHAGE_ACTIVATED: 6, MACROPHAGE_INFECTED: 6,
                          BACTERIUM_FAST: 10, BACTERIUM_SLOW: 10})
        for e in self.events:
            e.update_state_variable_from_node(self.node)
        self.event_M_R_B_F.perform()
        self.assertEqual(self.node[BACTERIUM_FAST], 9)
        self.assertEqual(self.node[BACTERIUM_SLOW], 10)
        self.assertEqual(self.node[MACROPHAGE_REGULAR], 5)
        self.assertEqual(self.node[MACROPHAGE_INFECTED], 7)
        self.assertEqual(self.node[BACTERIUM_INTRACELLULAR], 1)

        self.node.reset()
        rand.seed()
        self.node.update({MACROPHAGE_REGULAR: 6, MACROPHAGE_ACTIVATED: 6, MACROPHAGE_INFECTED: 6,
                          BACTERIUM_FAST: 10, BACTERIUM_SLOW: 10})
        for e in self.events:
            e.update_state_variable_from_node(self.node)
        self.event_M_I_B_F.perform()
        self.assertEqual(self.node[BACTERIUM_FAST], 9)
        self.assertEqual(self.node[BACTERIUM_SLOW], 10)
        self.assertEqual(self.node[MACROPHAGE_REGULAR], 6)
        self.assertEqual(self.node[MACROPHAGE_INFECTED], 6)
        self.assertEqual(self.node[BACTERIUM_INTRACELLULAR], 1)
