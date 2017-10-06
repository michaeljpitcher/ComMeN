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


class TCellRecruitmentByInfectedMacrophageTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [T_CELL_NAIVE, MACROPHAGE_INFECTED]
        self.nodes = [LymphPatch(0, compartments)]
        self.event = TCellRecruitmentByInfectedMacrophage(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0.0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.event.rate, 0.1 * 4)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 4})
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][T_CELL_NAIVE], 1)


class GetTCellRecruitmentEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_FAST]
        self.nodes = [LymphPatch(0, compartments)]
        self.rate_standard = 0.1
        self.rate_infected = 0.2
        self.events = get_t_cell_recruitment_events(self.nodes, self.rate_standard, self.rate_infected)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        standard = next(i for i in self.events if isinstance(i, TCellRecruitmentStandard))
        self.assertEqual(standard.reaction_parameter, 0.1)
        infected = next(i for i in self.events if isinstance(i, TCellRecruitmentByInfectedMacrophage))
        self.assertEqual(infected.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
