import unittest
from PTBComMeN import *


class TCellDeathTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = TCellDeath(0.1, self.nodes, T_CELL_NAIVE)
        self.event_external = TCellDeath(0.2, self.nodes, T_CELL_ACTIVATED, BACTERIUM_FAST)
        uh = UpdateHandler([self.event, self.event_external])

    def test_rate(self):
        for e in [self.event, self.event_external]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({T_CELL_NAIVE: 2})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_external.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_external.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 5})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_external.rate, 3.0)

    def test_update(self):
        self.nodes[0].update({T_CELL_NAIVE:1, T_CELL_ACTIVATED:1, BACTERIUM_FAST:2})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.event_external.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)
        self.assertEqual(self.nodes[0][T_CELL_ACTIVATED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)


class GetTCellDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [T_CELL_NAIVE, T_CELL_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.standard_death_rates = {T_CELL_NAIVE: 0.1, T_CELL_ACTIVATED: 0.2}
        self.external_rates = {T_CELL_NAIVE: {BACTERIUM_FAST: 0.3}, T_CELL_ACTIVATED: {BACTERIUM_SLOW: 0.4}}
        self.events = get_t_cell_death_events(self.nodes, self.standard_death_rates, self.external_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 4)
        for a in self.events:
            self.assertTrue(isinstance(a, TCellDeath))
        standard_naive = next(e for e in self.events if e._compartment_destroyed == T_CELL_NAIVE and not
                              e._influencing_compartments)
        self.assertEqual(standard_naive.reaction_parameter, 0.1)
        standard_activated = next(e for e in self.events if e._compartment_destroyed == T_CELL_ACTIVATED and not
                                  e._influencing_compartments)
        self.assertEqual(standard_activated.reaction_parameter, 0.2)

        external_naive = next(e for e in self.events if e._compartment_destroyed == T_CELL_NAIVE and
                              e._influencing_compartments is not None)
        self.assertEqual(external_naive.reaction_parameter, 0.3)
        self.assertItemsEqual(external_naive._influencing_compartments, [BACTERIUM_FAST])
        external_activated = next(e for e in self.events if e._compartment_destroyed == T_CELL_ACTIVATED and
                                  e._influencing_compartments is not None)
        self.assertEqual(external_activated.reaction_parameter, 0.4)
        self.assertItemsEqual(external_activated._influencing_compartments, [BACTERIUM_SLOW])


if __name__ == '__main__':
    unittest.main()
