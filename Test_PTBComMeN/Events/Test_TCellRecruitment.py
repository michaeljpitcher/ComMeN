import unittest
from PTBComMeN import *


class TCellRecruitmentLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.event = TCellRecruitmentLymph(0.1, self.nodes)
        self.event_external = TCellRecruitmentLymph(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_external])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_external.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_external.rate, 0.2 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 1})
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 1)
        self.event_external.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 2)


class GetTCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LymphPatch(0, compartments)]
        self.external_rates = {MACROPHAGE_INFECTED: 0.2, BACTERIUM_FAST: 0.3}
        self.events = get_t_cell_recruitment_events(self.nodes, 0.1, self.external_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 3)
        for e in self.events:
            self.assertTrue(isinstance(e, TCellRecruitmentLymph))
        standard = next(e for e in self.events if not e._influencing_compartments)
        self.assertEqual(standard.reaction_parameter, 0.1)
        external_1 = next(e for e in self.events if e._influencing_compartments == [MACROPHAGE_INFECTED])
        self.assertEqual(external_1.reaction_parameter, 0.2)
        external_2 = next(e for e in self.events if e._influencing_compartments == [BACTERIUM_FAST])
        self.assertEqual(external_2.reaction_parameter, 0.3)


if __name__ == '__main__':
    unittest.main()
