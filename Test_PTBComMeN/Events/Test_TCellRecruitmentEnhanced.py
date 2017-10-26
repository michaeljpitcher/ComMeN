import unittest
from PTBComMeN import *


class TCellRecruitmentByInfectedMacrophageTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, MACROPHAGE_INFECTED, BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LymphPatch(0, compartments)]
        self.event_mi = TCellRecruitmentEnhanced(0.1, self.nodes, MACROPHAGE_INFECTED)
        self.event_bf = TCellRecruitmentEnhanced(0.2, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event_mi, self.event_bf])

    def test_rate(self):
        self.assertEqual(self.event_mi.rate, 0.0)
        self.assertEqual(self.event_bf.rate, 0.0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event_mi.rate, 0.1 * 4)
        self.assertEqual(self.event_bf.rate, 0.0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event_mi.rate, 0.1 * 4)
        self.assertEqual(self.event_bf.rate, 0.2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)
        self.event_mi.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 1)


class GetTCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LymphPatch(0, compartments)]
        self.rates = {MACROPHAGE_INFECTED: 0.1, BACTERIUM_EXTRACELLULAR_FAST: 0.2}
        self.events = get_t_cell_recruitment_enhanced_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        for e, rate in self.rates.iteritems():
            event = next(k for k in self.events if k._influencing_compartments[0] == e)
            self.assertEqual(event.reaction_parameter, rate)


if __name__ == '__main__':
    unittest.main()
