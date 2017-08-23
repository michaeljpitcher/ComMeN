import unittest
from PTBComMeN import *
from LungComMeN import *


class DendriticTranslocationTestCase(unittest.TestCase):

    def setUp(self):
        self.compartments = [DENDRITIC_MATURE, DENDRITIC_IMMATURE, BACTERIUM_FAST, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, self.compartments, 0.1, 0.01), LymphPatch(1, self.compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 1)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)

        self.event = DendriticTranslocation(0.1, [self.nodes[0]], BACTERIUM_FAST)
        eh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({DENDRITIC_IMMATURE: 1})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 2})
        self.assertEqual(self.event.rate, 0.1 * 1 * 2)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 1 * (2 + 3))

    def test_update(self):
        self.nodes[0].update({DENDRITIC_IMMATURE: 1, BACTERIUM_FAST: 2})
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_IMMATURE], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 1)
        self.assertEqual(self.nodes[1][DENDRITIC_MATURE], 1)
