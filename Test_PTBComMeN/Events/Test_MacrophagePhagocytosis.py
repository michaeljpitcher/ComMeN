import unittest
from PTBComMeN import *


class PhagocytosisDestroyTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, BACTERIUM_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = PhagocytosisDestroy(0.1, self.nodes, BACTERIUM_FAST, MACROPHAGE_REGULAR)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2, BACTERIUM_FAST:5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 4)


class PhagocytosisRetainTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, BACTERIUM_FAST, BACTERIUM_INTRACELLULAR, MACROPHAGE_INFECTED]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = PhagocytosisRetain(0.1, self.nodes, BACTERIUM_FAST, MACROPHAGE_REGULAR)
        self.event_i = PhagocytosisRetain(0.2, self.nodes, BACTERIUM_FAST, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event, self.event_i])

    def test_rate(self):
        for e in [self.event, self.event_i]:
            self.assertEqual(e.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2, BACTERIUM_FAST:5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 4)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 1)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, BACTERIUM_FAST: 5})
        self.event_i.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_FAST], 4)
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 1)


class GetMacrophagePhagocytosisEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED, BACTERIUM_FAST, BACTERIUM_SLOW,
                        BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]

        self.destroy_rates = {}
        counter = 0.1
        for o in MACROPHAGE_PHAGOCYTOSIS_DESTROY_OPTIONS:
            self.destroy_rates[o] = counter
            counter += 0.1
        self.retain_rates = {}
        counter = 0.1
        for o in MACROPHAGE_PHAGOCYTOSIS_RETAIN_OPTIONS:
            self.retain_rates[o] = counter
            counter += 0.1
        self.events = get_phagocytosis_events(self.nodes, self.destroy_rates, self.retain_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 8)
        destroy = [e for e in self.events if isinstance(e, PhagocytosisDestroy)]
        for d in destroy:
            key = d._influencing_compartments[0] + "_" + d._compartment_destroyed
            self.assertEqual(self.destroy_rates[key], d.reaction_parameter)
        retain = [e for e in self.events if isinstance(e, PhagocytosisRetain)]
        for r in retain:
            key = r._influencing_compartments[0] + "_" + r._compartment_from
            self.assertEqual(self.retain_rates[key], r.reaction_parameter)

if __name__ == '__main__':
    unittest.main()
