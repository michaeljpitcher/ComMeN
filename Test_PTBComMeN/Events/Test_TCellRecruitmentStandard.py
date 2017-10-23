import unittest
from PTBComMeN import *


class TCellRecruitmentStandardTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE]
        self.nodes = [LymphPatch(0, compartments)]
        self.event = TCellRecruitmentStandard(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1)

    def test_update(self):
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 1)


class GetTCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LymphPatch(0, compartments)]
        self.rate_standard = 0.1
        self.events = get_t_cell_recruitment_standard_events(self.nodes, self.rate_standard)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        standard = next(i for i in self.events if isinstance(i, TCellRecruitmentStandard))
        self.assertEqual(standard.reaction_parameter, 0.1)


if __name__ == '__main__':
    unittest.main()
