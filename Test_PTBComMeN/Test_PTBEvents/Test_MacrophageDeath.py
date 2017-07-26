import unittest
from PulmonaryTBComMeN import *
from SetUpNodes import *


class MacrophageDeathTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR, BACTERIUM_SLOW]
        self.nodes = get_nodes(compartments)
        self.event_natural_regular = MacrophageDeathNatural(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_natural_infected = MacrophageDeathNatural(0.2, self.nodes, MACROPHAGE_INFECTED)
        self.event_infection = MacrophageDeathInfection(0.3, self.nodes)
        u = UpdateHandler([self.event_natural_regular, self.event_natural_infected, self.event_infection])

    def test_state_variable(self):
        for e in [self.event_natural_regular, self.event_natural_infected, self.event_infection]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 10})
        self.assertEqual(self.event_natural_regular.rate, 0.1 * 10)
        self.assertEqual(self.event_natural_infected.rate, 0)
        self.assertEqual(self.event_infection.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event_natural_regular.rate, 0.1 * 10)
        self.assertEqual(self.event_natural_infected.rate, 0.2 * 7)
        self.assertEqual(self.event_infection.rate, 0)
        self.nodes[0].update({BACTERIUM_INTRACELLULAR: 8})
        self.assertEqual(self.event_infection.rate, 0.3 * 7 * 8)

    def test_perform(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 10})
        self.event_natural_regular.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 9)
        self.nodes[1].update({MACROPHAGE_INFECTED: 8, BACTERIUM_INTRACELLULAR: 17})
        self.event_natural_infected.perform()
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 7)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 17-2)
        self.assertEqual(self.nodes[1][BACTERIUM_SLOW], 2)

