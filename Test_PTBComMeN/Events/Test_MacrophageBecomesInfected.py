import unittest
from PTBComMeN import *


class MacrophageBecomesInfectedTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, BACTERIUM_FAST, BACTERIUM_INTRACELLULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = MacrophageBecomesInfected(0.1, self.nodes, BACTERIUM_FAST, MACROPHAGE_REGULAR)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2, BACTERIUM_FAST: 5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 4)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 1)


class GetMacrophageBecomesInfectedEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW,
                        BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.rates = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2}
        self.events = get_macrophage_becomes_infected_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        regular_fast = next(e for e in self.events if e._influencing_compartments[0] == MACROPHAGE_REGULAR and
                            e._compartment_from == BACTERIUM_FAST)
        self.assertEqual(regular_fast.reaction_parameter, 0.1)
        regular_slow = next(e for e in self.events if e._influencing_compartments[0] == MACROPHAGE_REGULAR and
                            e._compartment_from == BACTERIUM_SLOW)
        self.assertEqual(regular_slow.reaction_parameter, 0.2)


if __name__ == '__main__':
    unittest.main()
