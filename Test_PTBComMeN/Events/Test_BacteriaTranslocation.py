import unittest
from PTBComMeN import *


class BacteriaTranslocationLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LungPatch(1, compartments, 0.9, 0.3)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateLung(0.1, self.nodes, BACTERIUM_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)
        self.nodes[1].update({BACTERIUM_FAST: 7})
        self.assertEqual(self.event.rate, 0.1 * 10)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 3)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 1)


class BacteriaTranslocationLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateLymph(0.1, self.nodes, BACTERIUM_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.27)
        self.nodes[1].update({BACTERIUM_FAST: 7})
        self.assertEqual(self.event.rate, 0.27)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 3)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 1)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 2)


class BacteriaTranslocationBloodTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [BACTERIUM_FAST]
        self.nodes = [LymphPatch(1, compartments), LungPatch(0, compartments, 0.9, 0.3)]
        self.edges = [BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateBlood(0.1, self.nodes, BACTERIUM_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)

    def test_update(self):
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 3)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 2)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 1)
        self.event.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_FAST], 2)


class GetBacteriaTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.5), LungPatch(1, compartments, 0.9, 0.2),
                      LymphPatch(2, compartments)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9), LungEdge(self.nodes[0], self.nodes[1], 0.9),
                      BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.rates_lung = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2}
        self.rates_lymph = {BACTERIUM_FAST: 0.3, BACTERIUM_SLOW: 0.4}
        self.rates_blood = {BACTERIUM_FAST: 0.5, BACTERIUM_SLOW: 0.6}
        self.events = get_bacteria_translocation_events([self.nodes[0], self.nodes[1]], [self.nodes[2]],
                                                        self.rates_lung, self.rates_lymph, self.rates_blood)

    def test_events(self):
        self.assertEqual(len(self.events), 6)
        lung_events = [n for n in self.events if isinstance(n, LungTranslocateWeight)]
        self.assertEqual(len(lung_events), 2)
        for a in lung_events:
            self.assertEqual(a.reaction_parameter, self.rates_lung[a._compartment_translocating])
        lymph_events = [n for n in self.events if isinstance(n, LymphTranslocateDrainage)]
        self.assertEqual(len(lymph_events), 2)
        for a in lymph_events:
            self.assertEqual(a.reaction_parameter, self.rates_lymph[a._compartment_translocating])
        blood_events = [n for n in self.events if isinstance(n, BloodTranslocatePerfusion)]
        self.assertEqual(len(blood_events), 2)
        for a in blood_events:
            self.assertEqual(a.reaction_parameter, self.rates_blood[a._compartment_translocating])

if __name__ == '__main__':
    unittest.main()
