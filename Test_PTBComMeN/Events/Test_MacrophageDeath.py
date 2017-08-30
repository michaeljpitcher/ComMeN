import unittest
from PTBComMeN import *


class MacrophageDeathTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR,
                        BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageDeath(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_inf_release = MacrophageDeath(0.2, self.nodes, MACROPHAGE_INFECTED, destroy_bacteria=False)
        self.event_inf_destroy = MacrophageDeath(0.3, self.nodes, MACROPHAGE_INFECTED,
                                                 influencing_compartment=T_CELL_ACTIVATED, destroy_bacteria=True)
        uh = UpdateHandler([self.event, self.event_inf_release, self.event_inf_destroy])

    def test_rate(self):
        for e in [self.event, self.event_inf_destroy, self.event_inf_release]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_inf_release.rate, 0)
        self.assertEqual(self.event_inf_destroy.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_inf_release.rate, 0.2 * 3)
        self.assertEqual(self.event_inf_destroy.rate, 0)
        self.nodes[0].update({T_CELL_ACTIVATED: 4})
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.assertEqual(self.event_inf_release.rate, 0.2 * 3)
        self.assertEqual(self.event_inf_destroy.rate, 0.3 * 3 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.event.perform()
        for t in self.nodes[0].compartments:
            if t != MACROPHAGE_REGULAR:
                self.assertEqual(self.nodes[0][t], 0)
            else:
                self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 10})
        self.event_inf_release.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 8)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 2)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 9})
        self.event_inf_release.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 7)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 2)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 6})
        self.event_inf_release.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 1)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 10, T_CELL_ACTIVATED: 10})
        self.event_inf_destroy.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 8)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 0)


class GetMacrophageDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_INTRACELLULAR,
                        BACTERIUM_SLOW, T_CELL_ACTIVATED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {MACROPHAGE_REGULAR: 0.1, MACROPHAGE_ACTIVATED: 0.2, MACROPHAGE_INFECTED: 0.3}
        self.inf_rates = {T_CELL_ACTIVATED: 0.4, BACTERIUM_INTRACELLULAR: 0.5}
        self.events = get_macrophage_death_events(self.nodes, self.rates, self.inf_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 5)
        for a in self.events:
            self.assertTrue(isinstance(a, MacrophageDeath))
        m_r_standard = next(i for i in self.events if i._compartment_destroyed == MACROPHAGE_REGULAR)
        self.assertEqual(m_r_standard.reaction_parameter, 0.1)
        self.assertFalse(m_r_standard._influencing_compartments)
        m_a_standard = next(i for i in self.events if i._compartment_destroyed == MACROPHAGE_ACTIVATED)
        self.assertEqual(m_a_standard.reaction_parameter, 0.2)
        self.assertFalse(m_a_standard._influencing_compartments)
        m_i_standard = next(i for i in self.events if i._compartment_destroyed == MACROPHAGE_INFECTED and
                            not i._influencing_compartments)
        self.assertEqual(m_i_standard.reaction_parameter, 0.3)

        m_i_t_cell = next(i for i in self.events if i._compartment_destroyed == MACROPHAGE_INFECTED and
                          i._influencing_compartments == [T_CELL_ACTIVATED])
        self.assertEqual(m_i_t_cell.reaction_parameter, 0.4)
        self.assertTrue(m_i_t_cell._destroy_bacteria)

        m_i_intracell = next(i for i in self.events if i._compartment_destroyed == MACROPHAGE_INFECTED and
                          i._influencing_compartments == [BACTERIUM_INTRACELLULAR])
        self.assertEqual(m_i_intracell.reaction_parameter, 0.5)
        self.assertFalse(m_i_intracell._destroy_bacteria)


if __name__ == '__main__':
    unittest.main()
