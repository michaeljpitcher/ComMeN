import unittest
from PTBComMeN import *


class MacrophageTranslocationLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = InfectedMacrophageTranslocateLymph(0.1, self.nodes)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3, BACTERIUM_INTRACELLULAR: 10})
        self.assertEqual(self.event.rate, 3 * 0.9 * 0.1)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, BACTERIUM_INTRACELLULAR: 10})
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 2)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 10)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 5)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 3, BACTERIUM_INTRACELLULAR: 10})
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 3)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 10)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 2)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 7)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 3)


class GetMacrophageTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.5)]
        self.edges = []
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.events = get_macrophage_translocation_events(self.nodes, 0.1)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        self.assertTrue(isinstance(self.events[0], InfectedMacrophageTranslocateLymph))
        self.assertEqual(self.events[0].reaction_parameter, 0.1)
        self.assertItemsEqual(self.events[0].state_variable_composition.keys(), self.nodes)


if __name__ == '__main__':
    unittest.main()
