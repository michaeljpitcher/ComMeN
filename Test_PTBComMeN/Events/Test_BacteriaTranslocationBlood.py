import unittest
from PTBComMeN import *


class BacteriaTranslocationBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LymphPatch(1, ALL_TB_COMPARTMENTS), LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.edges = [BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateBlood(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)

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


class BacteriaTranslocateLymphangitisTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LymphPatch(1, ALL_TB_COMPARTMENTS), LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.edges = [BloodEdge(self.nodes[0], self.nodes[1]), LymphEdge(self.nodes[1], self.nodes[0], 3)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = BacteriaTranslocateLymphangitis(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)

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
        self.rates_blood = {BACTERIUM_EXTRACELLULAR_FAST: 0.5, BACTERIUM_EXTRACELLULAR_SLOW: 0.6}
        self.lymphangitis_rates = {BACTERIUM_EXTRACELLULAR_FAST: 0.7, BACTERIUM_EXTRACELLULAR_SLOW: 0.8}
        self.events = get_bacteria_translocation_blood_events([self.nodes[2]], self.rates_blood, self.lymphangitis_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 4)
        blood = [e for e in self.events if isinstance(e, BloodTranslocatePerfusion)]
        for b in blood:
            self.assertEqual(b.reaction_parameter, self.rates_blood[b._compartment_translocating])
        lymphangitis = [e for e in self.events if isinstance(e, BacteriaTranslocateLymphangitis)]
        for e in lymphangitis:
            self.assertEqual(e.reaction_parameter, self.lymphangitis_rates[e._compartment_translocating])

if __name__ == '__main__':
    unittest.main()
