import unittest
from PTBComMeN import *


class MacrophageRecruitmentLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event_external = MacrophageRecruitmentLungEnhanced(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event_external])

    def test_rate(self):
        self.assertEqual(self.event_external.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event_external.rate, 0.2 * 0.3 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event_external.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class GetMacrophageRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lung_rates_enhanced = {MACROPHAGE_INFECTED: 0.2, BACTERIUM_FAST: 0.3}
        self.events = get_macrophage_recruitment_lung_enhanced_events([self.nodes[0]], self.lung_rates_enhanced)

    def test_events(self):
        self.assertEqual(len(self.events), 2)

        m_i_lung = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLungEnhanced) and
                        n._influencing_compartments == [MACROPHAGE_INFECTED])
        self.assertEqual(m_i_lung.reaction_parameter, 0.2)
        b_f_lung = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLungEnhanced) and
                        n._influencing_compartments == [BACTERIUM_FAST])
        self.assertEqual(b_f_lung.reaction_parameter, 0.3)


if __name__ == '__main__':
    unittest.main()
