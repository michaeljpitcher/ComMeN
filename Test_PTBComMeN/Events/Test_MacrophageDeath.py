import unittest
from PTBComMeN import *


class MacrophageDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.event = MacrophageDeathStandard(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_inf = MacrophageDeathStandard(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_inf])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(self.event_inf.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_inf.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_inf.rate, 0.2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR_MACROPHAGE: 10})
        self.event_inf.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_MACROPHAGE], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 10)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, BACTERIUM_INTRACELLULAR_MACROPHAGE: 10})
        self.event_inf.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_MACROPHAGE], 5)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 5)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 3, BACTERIUM_INTRACELLULAR_MACROPHAGE: 10})
        self.event_inf.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_MACROPHAGE], 7)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 3)


class GetMacrophageDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rates = {MACROPHAGE_REGULAR: 0.1, MACROPHAGE_ACTIVATED: 0.2, MACROPHAGE_INFECTED: 0.3}
        self.t_cell_death_rate = 0.4
        self.bursting_rate = 0.5
        self.carrying_capacity = 20
        self.hill_exponent = 2

        self.events = get_macrophage_standard_death_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 3)
        standard_regular = next(i for i in self.events if isinstance(i, MacrophageDeathStandard) and
                                i._compartment_destroyed == MACROPHAGE_REGULAR)
        self.assertEqual(standard_regular.reaction_parameter, 0.1)
        standard_activated = next(i for i in self.events if isinstance(i, MacrophageDeathStandard) and
                                  i._compartment_destroyed == MACROPHAGE_ACTIVATED)
        self.assertEqual(standard_activated.reaction_parameter, 0.2)
        standard_infected = next(i for i in self.events if isinstance(i, MacrophageDeathStandard) and
                                 i._compartment_destroyed == MACROPHAGE_INFECTED)
        self.assertEqual(standard_infected.reaction_parameter, 0.3)


if __name__ == '__main__':
    unittest.main()
