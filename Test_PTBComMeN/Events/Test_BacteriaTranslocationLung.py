import unittest
from PTBComMeN import *


class BacteriaTranslocationLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LungPatch(1, compartments, 0.9, 0.3)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateLung(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)
        self.nodes[1].update({BACTERIUM_EXTRACELLULAR_FAST: 7})
        self.assertEqual(self.event.rate, 0.1 * 10)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 3)
        self.assertEqual(self.nodes[1][BACTERIUM_EXTRACELLULAR_FAST], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 2)
        self.assertEqual(self.nodes[1][BACTERIUM_EXTRACELLULAR_FAST], 1)


class GetBacteriaTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.5), LungPatch(1, compartments, 0.9, 0.2),
                      LymphPatch(2, compartments)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9), LungEdge(self.nodes[0], self.nodes[1], 0.9),
                      BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.rates_lung = {BACTERIUM_EXTRACELLULAR_FAST: 0.1, BACTERIUM_EXTRACELLULAR_SLOW: 0.2}
        self.events = get_bacteria_translocation_lung_events([self.nodes[0], self.nodes[1]], self.rates_lung)

    def test_events(self):
        self.assertEqual(len(self.events), 2)

        for a in self.events:
            self.assertTrue(isinstance(a, LungTranslocateWeight))
            self.assertEqual(a.reaction_parameter, self.rates_lung[a._compartment_translocating])


if __name__ == '__main__':
    unittest.main()
