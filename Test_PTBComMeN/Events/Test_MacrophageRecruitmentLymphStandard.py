import unittest
from PTBComMeN import *


class MacrophageRecruitmentLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.event = MacrophageRecruitmentLymphStandard(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class GetMacrophageRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lymph_rate_standard = 0.4
        self.events = get_macrophage_recruitment_lymph_standard_events([self.nodes[1]], self.lymph_rate_standard)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        standard_lymph = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLymphStandard))
        self.assertEqual(standard_lymph.reaction_parameter, 0.4)


if __name__ == '__main__':
    unittest.main()
