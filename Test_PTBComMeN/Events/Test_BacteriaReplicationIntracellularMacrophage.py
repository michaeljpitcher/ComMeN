import unittest
from PTBComMeN import *


class IntracellularBacteriaReplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.carrying_capacity = 10
        self.hill_exponent = 2
        self.event_i = IntracellularBacteriaMacrophageReplication(0.3, self.nodes, self.carrying_capacity,
                                                                  self.hill_exponent)
        uh = UpdateHandler([self.event_i])

    def test_rate(self):
        self.assertEqual(self.event_i.rate, 0)

        mi = 1
        bi = 1
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR_MACROPHAGE: bi})
        self.assertEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi**self.hill_exponent) / (bi**self.hill_exponent +
                                                   (self.carrying_capacity * mi)**self.hill_exponent)))

        mi = 1
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR_MACROPHAGE: bi})
        self.assertEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi ** self.hill_exponent) / (bi ** self.hill_exponent +
                                                 (self.carrying_capacity * mi) ** self.hill_exponent)))
        mi = 4
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({MACROPHAGE_INFECTED: mi, BACTERIUM_INTRACELLULAR_MACROPHAGE: bi})
        self.assertAlmostEqual(self.event_i.rate, 0.3 * bi * (1 - float(bi ** self.hill_exponent) / (
                         bi ** self.hill_exponent + (self.carrying_capacity * mi) ** self.hill_exponent)))

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_INFECTED: 1, BACTERIUM_INTRACELLULAR_MACROPHAGE: 5})
        self.event_i.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_MACROPHAGE], 6)


class GetBacteriaReplicationEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rate = 0.3
        self.carrying_capacity = 20
        self.hill_exponent = 2
        self.events = get_bacteria_replication_intracellular_macrophage_events(self.nodes, self.rate,
                                                                               self.carrying_capacity,
                                                                               self.hill_exponent)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        int = self.events[0]
        self.assertEqual(int.reaction_parameter, 0.3)
        self.assertEqual(int._macrophage_carrying_capacity, self.carrying_capacity)


if __name__ == '__main__':
    unittest.main()
