import unittest
from PTBComMeN import *


class MacrophageRecruitmentLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageRecruitmentLungStandard(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1 * 0.3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class GetMacrophageRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lung_rate_standard = 0.1
        self.events = get_macrophage_recruitment_lung_standard_events([self.nodes[0]], self.lung_rate_standard)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        standard_lung = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLungStandard))
        self.assertEqual(standard_lung.reaction_parameter, 0.1)


if __name__ == '__main__':
    unittest.main()
