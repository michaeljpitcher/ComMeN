import unittest
from PTBComMeN import *


class BacteriaTranslocationBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LymphPatch(1, ALL_TB_COMPARTMENTS), LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
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
        self.rates_blood = {BACTERIUM_FAST: 0.5, BACTERIUM_SLOW: 0.6}
        self.events = get_bacteria_translocation_blood_events([self.nodes[2]], self.rates_blood)

    def test_events(self):
        self.assertEqual(len(self.events), 2)
        for e in self.events:
            self.assertTrue(isinstance(e, BloodTranslocatePerfusion))
            self.assertEqual(e.reaction_parameter, self.rates_blood[e._compartment_translocating])


if __name__ == '__main__':
    unittest.main()
