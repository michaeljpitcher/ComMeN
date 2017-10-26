import unittest
from PTBComMeN import *


class DendriticCellDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.event_idc = DendriticCellDeathStandard(0.1, self.nodes, DENDRITIC_CELL_IMMATURE)
        self.event_mdc = DendriticCellDeathStandard(0.2, self.nodes, DENDRITIC_CELL_MATURE)
        uh = UpdateHandler([self.event_idc, self.event_mdc])

    def test_rate(self):
        self.assertEqual(self.event_idc.rate, 0)
        self.assertEqual(self.event_mdc.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 2})
        self.assertEqual(self.event_idc.rate, 0.1 * 2)
        self.assertEqual(self.event_mdc.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 3})
        self.assertEqual(self.event_mdc.rate, 0.2 * 3)

    def test_update(self):
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 2})
        self.event_idc.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 1)

        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 7, BACTERIUM_INTRACELLULAR_DENDRITIC: 14})
        self.event_mdc.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 6)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_DENDRITIC], 12)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_SLOW], 2)


class GetDendriticCellDeathEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rates = {DENDRITIC_CELL_IMMATURE: 0.1, DENDRITIC_CELL_MATURE: 0.2}

        self.events = get_dendritic_cell_standard_death_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        standard_immature = next(i for i in self.events if isinstance(i, DendriticCellDeathStandard) and
                                i._compartment_destroyed == DENDRITIC_CELL_IMMATURE)
        self.assertEqual(standard_immature.reaction_parameter, 0.1)
        standard_mature = next(i for i in self.events if isinstance(i, DendriticCellDeathStandard) and
                              i._compartment_destroyed == DENDRITIC_CELL_MATURE)
        self.assertEqual(standard_mature.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
