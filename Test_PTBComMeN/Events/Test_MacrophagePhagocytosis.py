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
        self.regular_infect_rates = {BACTERIUM_FAST: 0.1, BACTERIUM_SLOW: 0.2}
        self.regular_destroy_rates = {BACTERIUM_FAST: 0.3, BACTERIUM_SLOW: 0.4}
        self.infected_retain_rates = {BACTERIUM_FAST: 0.5, BACTERIUM_SLOW: 0.6}
        self.activated_destroy_rates= {BACTERIUM_FAST: 0.7, BACTERIUM_SLOW: 0.8}
        self.events = get_phagocytosis_events(self.nodes, self.regular_infect_rates, self.regular_destroy_rates,
                                              self.infected_retain_rates, self.activated_destroy_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 8)
        for b in self.regular_infect_rates.keys():
            regular_infect_event = next(n for n in self.events if isinstance(n, PhagocytosisRetain) and
                                   n._influencing_compartments[0] == MACROPHAGE_REGULAR and
                                   n._compartment_from == b)
            self.assertEqual(regular_infect_event.reaction_parameter, self.regular_infect_rates[b])
        for b in self.regular_destroy_rates.keys():
            regular_destroy_event = next(n for n in self.events if isinstance(n, PhagocytosisDestroy) and
                                   n._influencing_compartments[0] == MACROPHAGE_REGULAR and
                                   n._compartment_destroyed == b)
            self.assertEqual(regular_destroy_event.reaction_parameter, self.regular_destroy_rates[b])
        for b in self.infected_retain_rates.keys():
            infected_infect_event = next(n for n in self.events if isinstance(n, PhagocytosisRetain) and
                                   n._influencing_compartments[0] == MACROPHAGE_INFECTED and
                                   n._compartment_from == b)
            self.assertEqual(infected_infect_event.reaction_parameter, self.infected_retain_rates[b])
        for b in self.activated_destroy_rates.keys():
            activated_destroy_event = next(n for n in self.events if isinstance(n, PhagocytosisDestroy) and
                                   n._influencing_compartments[0] == MACROPHAGE_ACTIVATED and
                                   n._compartment_destroyed == b)
            self.assertEqual(activated_destroy_event.reaction_parameter, self.activated_destroy_rates[b])

if __name__ == '__main__':
    unittest.main()
