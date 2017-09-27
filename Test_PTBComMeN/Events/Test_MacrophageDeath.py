import unittest
from PTBComMeN import *


class MacrophageDeathTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageDeath(0.1, self.nodes, MACROPHAGE_REGULAR)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0.1 * 2)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, T_CELL_ACTIVATED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = InfectedMacrophageDeathByTCell(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, T_CELL_ACTIVATED: 3, BACTERIUM_INTRACELLULAR:10})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 3)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 10)


class InfectedMacrophageBurstsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.carrying_capacity = 20
        self.hill_exponent = 2
        self.event = InfectedMacrophageBursts(1.0, self.nodes, self.carrying_capacity, self.hill_exponent)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        mac = 2
        bac = 20
        self.nodes[0].update({MACROPHAGE_INFECTED: mac, BACTERIUM_INTRACELLULAR: bac})
        self.assertEqual(self.event.rate, 1.0 * mac * (1.0 * bac ** self.hill_exponent / (
                        bac ** self.hill_exponent + (self.carrying_capacity * mac) ** self.hill_exponent)))

    def test_perform(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR: 20})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 20)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, BACTERIUM_INTRACELLULAR: 39})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 19)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 20)


class GetMacrophageDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_INTRACELLULAR,
                        BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {MACROPHAGE_REGULAR: 0.1, MACROPHAGE_ACTIVATED: 0.2, MACROPHAGE_INFECTED: 0.3}
        self.t_cell_death_rate = 0.4
        self.bursting_rate = 0.5
        self.carrying_capacity = 20
        self.hill_exponent = 2

        self.events = get_macrophage_death_events(self.nodes, self.rates, self.t_cell_death_rate, self.bursting_rate,
                                                  self.carrying_capacity, self.hill_exponent)

    def test_events(self):
        self.assertEqual(len(self.events), 5)
        standard_regular = next(i for i in self.events if isinstance(i, MacrophageDeath) and
                                i._compartment_destroyed == MACROPHAGE_REGULAR)
        self.assertEqual(standard_regular.reaction_parameter, 0.1)
        standard_activated = next(i for i in self.events if isinstance(i, MacrophageDeath) and
                                  i._compartment_destroyed == MACROPHAGE_ACTIVATED)
        self.assertEqual(standard_activated.reaction_parameter, 0.2)
        standard_infected = next(i for i in self.events if isinstance(i, MacrophageDeath) and
                                  i._compartment_destroyed == MACROPHAGE_INFECTED)
        self.assertEqual(standard_infected.reaction_parameter, 0.3)

        infected_t_cell = next(i for i in self.events if isinstance(i, InfectedMacrophageDeathByTCell))
        self.assertEqual(infected_t_cell.reaction_parameter, 0.4)

        infected_bursts = next(i for i in self.events if isinstance(i, InfectedMacrophageBursts))
        self.assertEqual(infected_bursts.reaction_parameter, 0.5)
        self.assertEqual(infected_bursts._carrying_capacity, self.carrying_capacity)
        self.assertEqual(infected_bursts._hill_exponent, self.hill_exponent)


if __name__ == '__main__':
    unittest.main()
