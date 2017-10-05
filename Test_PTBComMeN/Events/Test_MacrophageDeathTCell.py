import unittest
from PTBComMeN import *


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, T_CELL_ACTIVATED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.half_sat = 1.1
        self.event = InfectedMacrophageDeathByTCell(0.1, self.nodes, self.half_sat)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * ((3.0 / 2.0) / ((3.0 / 2.0) + self.half_sat)))

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, T_CELL_ACTIVATED: 3, BACTERIUM_INTRACELLULAR:10})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 3)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)

        self.nodes[0].reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 2, T_CELL_ACTIVATED: 3, BACTERIUM_INTRACELLULAR: 10})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 3)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)


class GetMacrophageDeathByTCellEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.t_cell_death_rate = 0.4
        self.half_sat = 1.1
        self.events = get_macrophage_death_by_t_cell_events(self.nodes, self.t_cell_death_rate, self.half_sat)

    def test_events(self):
        self.assertEqual(len(self.events), 1)

        infected_t_cell = self.events[0]
        self.assertTrue(isinstance(infected_t_cell, InfectedMacrophageDeathByTCell))
        self.assertEqual(infected_t_cell.reaction_parameter, 0.4)
        self.assertEqual(infected_t_cell._half_sat, self.half_sat)


if __name__ == '__main__':
    unittest.main()
