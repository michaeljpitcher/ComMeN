import unittest
from PTBComMeN import *


class InfectedMacrophageBurstsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR, BACTERIUM_SLOW]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.carrying_capacity = 13
        self.hill_exponent = 2
        self.event = InfectedMacrophageBursts(1.0, self.nodes, self.carrying_capacity, self.hill_exponent)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        mac = 2
        bac = 20
        self.nodes[0].update({MACROPHAGE_INFECTED: mac, BACTERIUM_INTRACELLULAR: bac})
        self.assertEqual(self.event.rate, 1.0 * mac * (1.0 * bac ** self.hill_exponent / (
                        bac ** self.hill_exponent + (self.carrying_capacity * mac) ** self.hill_exponent)))

    def test_perform(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR: 20})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 0)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 20)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 2, BACTERIUM_INTRACELLULAR: 83})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 41)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 42)

        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: 5, BACTERIUM_INTRACELLULAR: 61})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR], 49)
        self.assertEqual(self.nodes[0][BACTERIUM_SLOW], 12)


class GetMacrophageBurstingEventsTestCase(unittest.TestCase):

    def setUp(self):
        compartments = [MACROPHAGE_INFECTED, BACTERIUM_INTRACELLULAR]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.bursting_rate = 0.5
        self.carrying_capacity = 20
        self.hill_exponent = 2

        self.events = get_macrophage_bursting_events(self.nodes, self.bursting_rate, self.carrying_capacity,
                                                     self.hill_exponent)

    def test_events(self):
        self.assertEqual(len(self.events), 1)

        infected_bursts = self.events[0]
        self.assertEqual(infected_bursts.reaction_parameter, 0.5)
        self.assertEqual(infected_bursts._carrying_capacity, self.carrying_capacity)
        self.assertEqual(infected_bursts._hill_exponent, self.hill_exponent)


if __name__ == '__main__':
    unittest.main()
