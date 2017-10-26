import unittest
from PTBComMeN import *


class DendriticCellRecruitmentLungEnhancedBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [DENDRITIC_CELL_IMMATURE, BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.half_sat = 20
        self.event = DendriticCellRecruitmentLungEnhancedByBacteria(0.1, self.nodes, self.half_sat)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 1})
        self.assertEqual(self.event.rate, 0.1 * (1.0 / (1 + 20)))
        rate_1 = self.event.rate

        self.nodes[0].reset()
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_SLOW: 5})
        self.assertEqual(self.event.rate, 0.1 * (5.0 / (5 + 20)))
        rate_5 = self.event.rate

        self.assertTrue(rate_5 > rate_1)

        self.nodes[0].reset()
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 15, BACTERIUM_EXTRACELLULAR_SLOW: 5})
        self.assertEqual(self.event.rate, 0.1 * (20.0 / (20 + 20)))
        rate_20 = self.event.rate

        self.assertTrue(rate_20 > rate_5 > rate_1)

    def test_update(self):
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 1)


class GetDendriticCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, BACTERIUM_EXTRACELLULAR_SLOW, BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rate = 0.2
        self.half_sat = 20
        self.events = get_dendritic_cell_recruitment_enhanced_events(self.nodes, self.rate, self.half_sat)

    def test_events(self):
        self.assertEqual(len(self.events), 1)

        self.assertTrue(isinstance(self.events[0], DendriticCellRecruitmentLungEnhancedByBacteria))
        self.assertEqual(self.events[0].reaction_parameter, self.rate)
        self.assertEqual(self.events[0]._half_sat, self.half_sat)


if __name__ == '__main__':
    unittest.main()
