import unittest
from PTBComMeN import *


class TCellDeathTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = TCellDeath(0.1, self.nodes, T_CELL_NAIVE)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({T_CELL_NAIVE: 2})
        self.assertEqual(self.event.rate, 0.1 * 2)

    def test_update(self):
        self.nodes[0].update({T_CELL_NAIVE:1})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)


class GetTCellDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.death_rates = {T_CELL_NAIVE: 0.1, T_CELL_ACTIVATED: 0.2}
        self.events = get_t_cell_death_events(self.nodes, self.death_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        for a in self.events:
            self.assertTrue(isinstance(a, TCellDeath))
        standard_naive = next(e for e in self.events if e._compartment_destroyed == T_CELL_NAIVE and not
                              e._influencing_compartments)
        self.assertEqual(standard_naive.reaction_parameter, 0.1)
        standard_activated = next(e for e in self.events if e._compartment_destroyed == T_CELL_ACTIVATED and not
                                  e._influencing_compartments)
        self.assertEqual(standard_activated.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
