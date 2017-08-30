import unittest
from PTBComMeN import *


class MacrophageRecruitmentLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageRecruitmentLung(0.1, self.nodes)
        self.event_external = MacrophageRecruitmentLung(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_external])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1 * 0.3)
        self.assertEqual(self.event_external.rate, 0.2 * 0.3 * 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event_external.rate, 0.2 * 0.3 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)
        self.event_external.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class MacrophageRecruitmentLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.event = MacrophageRecruitmentLymph(0.1, self.nodes)
        self.event_external = MacrophageRecruitmentLymph(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_external])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_external.rate, 0.1 * 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event_external.rate, 0.2 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)
        self.event_external.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)


class GetMacrophageRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.lung_rates = {STANDARD: 0.1, MACROPHAGE_INFECTED: 0.3, BACTERIUM_FAST: 0.4}
        self.lymph_rates = {STANDARD:0.2, MACROPHAGE_INFECTED: 0.5, BACTERIUM_FAST: 0.6}
        self.events = get_macrophage_recruitment_events([self.nodes[0]], [self.nodes[1]],
                                                        self.lung_rates, self.lymph_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 6)
        standard_lung = next(n for n in self.events if isinstance(n, RecruitmentByPerfusion) and
                             not n._influencing_compartments)
        self.assertEqual(standard_lung.reaction_parameter, 0.1)
        standard_lymph = next(n for n in self.events if isinstance(n, Create) and
                              not n._influencing_compartments and
                              n.state_variable_composition.keys() == [self.nodes[1]])
        self.assertEqual(standard_lymph.reaction_parameter, 0.2)
        m_i_lung = next(n for n in self.events if isinstance(n, RecruitmentByPerfusion) and
                             n._influencing_compartments == [MACROPHAGE_INFECTED])
        self.assertEqual(m_i_lung.reaction_parameter, 0.3)
        b_f_lung = next(n for n in self.events if isinstance(n, RecruitmentByPerfusion) and
                        n._influencing_compartments == [BACTERIUM_FAST])
        self.assertEqual(b_f_lung.reaction_parameter, 0.4)
        m_i_lymph = next(n for n in self.events if isinstance(n, Create) and
                              n._influencing_compartments == [MACROPHAGE_INFECTED] and
                              n.state_variable_composition.keys() == [self.nodes[1]])
        self.assertEqual(m_i_lymph.reaction_parameter, 0.5)
        b_f_lymph = next(n for n in self.events if isinstance(n, Create) and
                         n._influencing_compartments == [BACTERIUM_FAST] and
                         n.state_variable_composition.keys() == [self.nodes[1]])
        self.assertEqual(b_f_lymph.reaction_parameter, 0.6)

if __name__ == '__main__':
    unittest.main()
