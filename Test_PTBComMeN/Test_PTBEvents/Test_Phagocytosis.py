import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class PhagocytosisTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_FAST,
                        BACTERIUM_INTRACELLULAR]
        self.nodes = get_nodes(compartments)
        self.phagocytosis = Phagocytosis(0.1, self.nodes, MACROPHAGE_ACTIVATED, BACTERIUM_FAST)
        self.phagocy_internalise_infect = PhagocytosisInternalise(0.2, self.nodes, MACROPHAGE_REGULAR, BACTERIUM_FAST,
                                                                  MACROPHAGE_INFECTED)
        self.phagocy_internalise = PhagocytosisInternalise(0.3, self.nodes, MACROPHAGE_INFECTED, BACTERIUM_FAST)
        u = UpdateHandler([self.phagocytosis, self.phagocy_internalise, self.phagocy_internalise_infect])

    def test_state_variable(self):
        for e in [self.phagocytosis, self.phagocy_internalise, self.phagocy_internalise_infect]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 20})
        for e in [self.phagocytosis, self.phagocy_internalise, self.phagocy_internalise_infect]:
            self.assertEqual(e.rate, 0)

        self.nodes[0].update({MACROPHAGE_ACTIVATED: 4})
        self.assertEqual(self.phagocytosis.rate, 0.1 * 4 * 20)
        self.assertEqual(self.phagocy_internalise.rate, 0)
        self.assertEqual(self.phagocy_internalise_infect.rate, 0)

        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.phagocytosis.rate, 0.1 * 4 * 20)
        self.assertEqual(self.phagocy_internalise.rate, 0.3 * 3 * 20)
        self.assertEqual(self.phagocy_internalise_infect.rate, 0)

        self.nodes[0].update({MACROPHAGE_REGULAR: 5})
        self.assertEqual(self.phagocytosis.rate, 0.1 * 4 * 20)
        self.assertEqual(self.phagocy_internalise.rate, 0.3 * 3 * 20)
        self.assertEqual(self.phagocy_internalise_infect.rate, 0.2 * 5 * 20)

    def test_perform(self):
        self.nodes[0].update({MACROPHAGE_ACTIVATED: 4, MACROPHAGE_REGULAR: 3,
                              BACTERIUM_FAST: 10})
        self.phagocytosis.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_ACTIVATED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 9)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 0)

        self.phagocy_internalise_infect.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 8)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 1)

        self.phagocy_internalise.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 7)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 2)
