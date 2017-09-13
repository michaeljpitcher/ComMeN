import unittest
from PTBComMeN import *


class MacrophageTranslocationLungTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LungPatch(1, compartments, 0.9, 0.3)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = MacrophageTranslocateLung(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_internals = MacrophageTranslocateLung(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_internals])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.event.rate, 0.1 * 3)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[1].update({MACROPHAGE_REGULAR: 7})
        self.assertEqual(self.event.rate, 0.1 * (3 + 7))
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_internals.rate, 0.2 * 3)
        self.nodes[1].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event_internals.rate, 0.2 * (3 + 7))

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 3)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 1)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 10})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 8)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 9})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 7)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 6})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 1)


class MacrophageTranslocationLymphTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3), LymphPatch(1, compartments)]
        self.edges = [LymphEdge(self.nodes[0], self.nodes[1], 0.9)]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = MacrophageTranslocateLymph(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_internals = MacrophageTranslocateLymph(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_internals])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.event.rate, 0.27)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[1].update({MACROPHAGE_REGULAR: 7})
        self.assertEqual(self.event.rate, 0.27)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_internals.rate, 0.54)
        self.nodes[1].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event_internals.rate, 0.54)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 3)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 1)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 10})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 8)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 9})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 7)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 6})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 1)


class MacrophageTranslocationBloodTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LymphPatch(1, compartments), LungPatch(0, compartments, 0.9, 0.3)]
        self.edges = [BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.event = MacrophageTranslocateBlood(0.1, self.nodes, MACROPHAGE_REGULAR)
        self.event_internals = MacrophageTranslocateBlood(0.2, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_internals])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.event.rate, 3 * 0.1)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[1].update({MACROPHAGE_REGULAR: 7})
        self.assertEqual(self.event.rate, 3 * 0.1)
        self.assertEqual(self.event_internals.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 3})
        self.assertEqual(self.event_internals.rate, 3 * 0.2)
        self.nodes[1].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event_internals.rate, 3 * 0.2)


    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 3})
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 3)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 0)
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[1][MACROPHAGE_REGULAR], 1)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 10})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 8)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 9})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 7)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 2)

        for n in self.nodes:
            n.reset()

        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 6})
        self.event_internals.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 5)
        self.assertEqual(self.nodes[1][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[1][BACTERIUM_INTRACELLULAR], 1)


class GetMacrophageTranslocationEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.5), LungPatch(1, compartments, 0.9, 0.2),
                      LymphPatch(2, compartments)]
        self.edges = [LungEdge(self.nodes[0], self.nodes[1], 0.9), LungEdge(self.nodes[0], self.nodes[1], 0.9),
                      BloodEdge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.rates_lung = {MACROPHAGE_REGULAR: 0.1, MACROPHAGE_INFECTED: 0.2, MACROPHAGE_ACTIVATED: 0.3}
        self.rates_lymph = {MACROPHAGE_REGULAR: 0.4, MACROPHAGE_INFECTED: 0.5, MACROPHAGE_ACTIVATED: 0.6}
        self.rates_blood = {MACROPHAGE_REGULAR: 0.7, MACROPHAGE_INFECTED: 0.8, MACROPHAGE_ACTIVATED: 0.9}
        self.events = get_macrophage_translocation_events([self.nodes[0], self.nodes[1]], [self.nodes[2]],
                                                        self.rates_lung, self.rates_lymph, self.rates_blood)

    def test_events(self):
        self.assertEqual(len(self.events), 9)
        lung_events = [n for n in self.events if isinstance(n, LungTranslocateWeight)]
        self.assertEqual(len(lung_events), 3)
        for a in lung_events:
            self.assertEqual(a.reaction_parameter, self.rates_lung[a._compartment_translocating])
        lymph_events = [n for n in self.events if isinstance(n, LymphTranslocateDrainage)]
        self.assertEqual(len(lymph_events), 3)
        for a in lymph_events:
            self.assertEqual(a.reaction_parameter, self.rates_lymph[a._compartment_translocating])
        blood_events = [n for n in self.events if isinstance(n, BloodTranslocatePerfusion)]
        self.assertEqual(len(blood_events), 3)
        for a in blood_events:
            self.assertEqual(a.reaction_parameter, self.rates_blood[a._compartment_translocating])

if __name__ == '__main__':
    unittest.main()
