import unittest
from PTBComMeN import *


class DendriticCellRecruitmentLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [DENDRITIC_CELL_IMMATURE]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = DendriticCellRecruitmentLungStandard(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1 * 0.3)

    def test_update(self):
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 1)


class GetDendriticCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [DENDRITIC_CELL_IMMATURE]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lung_rate_standard = 0.1
        self.events = get_dendritic_cell_recruitment_standard_events([self.nodes[0]], self.lung_rate_standard)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        standard_lung = next(n for n in self.events if isinstance(n, DendriticCellRecruitmentLungStandard))
        self.assertEqual(standard_lung.reaction_parameter, 0.1)


if __name__ == '__main__':
    unittest.main()
