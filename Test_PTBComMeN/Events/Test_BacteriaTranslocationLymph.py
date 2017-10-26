import unittest
from PTBComMeN import *


class BacteriaTranslocationLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateLymph(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.27)
        self.nodes[1].update({BACTERIUM_EXTRACELLULAR_FAST: 7})
        self.assertEqual(self.event.rate, 0.27)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 3)
        self.assertEqual(self.nodes[1][BACTERIUM_EXTRACELLULAR_FAST], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 2)
        self.assertEqual(self.nodes[1][BACTERIUM_EXTRACELLULAR_FAST], 1)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_EXTRACELLULAR_FAST], 2)


class GetBacteriaTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.5), LungPatch(1, compartments, 0.9, 0.2),
                      LymphPatch(2, compartments)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9), LungEdge(self.nodes[0], self.nodes[1], 0.9),
                      BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.rates_lymph = {BACTERIUM_EXTRACELLULAR_FAST: 0.3, BACTERIUM_EXTRACELLULAR_SLOW: 0.4}
        self.events = get_bacteria_translocation_lymph_events([self.nodes[0], self.nodes[1]], self.rates_lymph)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        for a in self.events:
            self.assertTrue(isinstance(a, LymphTranslocateDrainage))
            self.assertEqual(a.reaction_parameter, self.rates_lymph[a._compartment_translocating])


if __name__ == '__main__':
    unittest.main()
