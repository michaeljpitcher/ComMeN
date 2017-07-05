import unittest

from EpidemicComMeN import *


class InfectTestCase(unittest.TestCase):
    def setUp(self):
        self.sus_comp = 'S'
        self.infected_comp = 'E'
        self.infectious_comps = ['I','N']
        self.node = Patch(0, [self.sus_comp, self.infected_comp, self.infectious_comps[0], self.infectious_comps[1]])

        self.event_pop = Infect(0.1, [self.node], self.sus_comp, self.infected_comp, self.infectious_comps, True)
        self.event_non_pop = Infect(0.2, [self.node], self.sus_comp, self.infected_comp, self.infectious_comps, False)

        uh = UpdateHandler([self.event_pop, self.event_non_pop])

    def test_rate(self):
        self.assertFalse(self.event_pop.rate)
        self.assertFalse(self.event_non_pop.rate)

        self.node.update({self.sus_comp: 8})
        self.assertFalse(self.event_pop.rate)
        self.assertFalse(self.event_non_pop.rate)

        self.node.update({self.infected_comp: 3})
        self.assertFalse(self.event_pop.rate)
        self.assertFalse(self.event_non_pop.rate)

        self.node.update({self.infectious_comps[0]: 4})
        self.assertEqual(self.event_pop.rate, 0.1 * ((8 * 4) / float(8 + 3 + 4)))
        self.assertEqual(self.event_non_pop.rate, 0.2 * (8 * 4))

        self.node.update({self.infectious_comps[1]: 2})
        self.assertEqual(self.event_pop.rate, 0.1 * ((8 * (4+2)) / float(8 + 3 + 4 + 2)))
        self.assertEqual(self.event_non_pop.rate, 0.2 * (8 * (4+2)))


if __name__ == '__main__':
    unittest.main()
