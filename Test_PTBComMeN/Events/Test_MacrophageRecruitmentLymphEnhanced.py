import unittest
from PTBComMeN import *


class MacrophageRecruitmentLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.event_external = MacrophageRecruitmentLymphEnhanced(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event_external])

    def test_rate(self):
        self.assertEqual(self.event_external.rate, 0.1 * 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event_external.rate, 0.2 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event_external.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class GetMacrophageRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lymph_rates_enhanced = {MACROPHAGE_INFECTED: 0.5, BACTERIUM_FAST: 0.6}
        self.events = get_macrophage_recruitment_lymph_enhanced_events([self.nodes[1]], self.lymph_rates_enhanced)

    def test_events(self):
        self.assertEqual(len(self.events), 2)

        m_i_lymph = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLymphEnhanced) and
                              n._influencing_compartments == [MACROPHAGE_INFECTED])
        self.assertEqual(m_i_lymph.reaction_parameter, 0.5)
        b_f_lymph = next(n for n in self.events if isinstance(n, MacrophageRecruitmentLymphEnhanced) and
                         n._influencing_compartments == [BACTERIUM_FAST])
        self.assertEqual(b_f_lymph.reaction_parameter, 0.6)

if __name__ == '__main__':
    unittest.main()
