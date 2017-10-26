import unittest
from PTBComMeN import *


class IntracellularBacteriaDendriticReplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.carrying_capacity = 10
        self.hill_exponent = 2
        self.event_i = IntracellularBacteriaDendriticReplication(0.1, self.nodes, self.carrying_capacity,
                                                                  self.hill_exponent)
        uh = UpdateHandler([self.event_i])

    def test_rate(self):
        self.assertEqual(self.event_i.rate, 0)

        dc = 1
        bi = 1
        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_MATURE: dc, BACTERIUM_INTRACELLULAR_DENDRITIC: bi})
        self.assertEqual(self.event_i.rate, 0.1 * bi * (1 - float(bi**self.hill_exponent) / (bi**self.hill_exponent +
                                                   (self.carrying_capacity * dc)**self.hill_exponent)))
        rate_1_1 = self.event_i.rate

        mi = 1
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_MATURE: mi, BACTERIUM_INTRACELLULAR_DENDRITIC: bi})
        self.assertEqual(self.event_i.rate, 0.1 * bi * (1 - float(bi ** self.hill_exponent) / (bi ** self.hill_exponent +

                                                 (self.carrying_capacity * mi) ** self.hill_exponent)))
        rate_1_10 = self.event_i.rate

        mi = 4
        bi = 10
        self.nodes[0].reset()
        self.nodes[0].update({DENDRITIC_CELL_MATURE: mi, BACTERIUM_INTRACELLULAR_DENDRITIC: bi})
        self.assertAlmostEqual(self.event_i.rate, 0.1 * bi * (1 - float(bi ** self.hill_exponent) / (
                         bi ** self.hill_exponent + (self.carrying_capacity * mi) ** self.hill_exponent)))
        rate_4_10 = self.event_i.rate

        # More room so greater growth
        self.assertTrue(rate_1_10 < rate_4_10)


    def test_update(self):
        self.nodes[0].update({DENDRITIC_CELL_MATURE: 1, BACTERIUM_INTRACELLULAR_DENDRITIC: 5})
        self.event_i.perform()
        self.assertEqual(self.nodes[0][BACTERIUM_INTRACELLULAR_DENDRITIC], 6)


class GetBacteriaReplicationIntracellularDendriticEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rate = 0.1
        self.carrying_capacity = 20
        self.hill_exponent = 2
        self.events = get_bacteria_replication_intracellular_dendritic_events(self.nodes, self.rate,
                                                                              self.carrying_capacity,
                                                                              self.hill_exponent)

    def test_events(self):
        self.assertEqual(len(self.events), 1)
        int = self.events[0]
        self.assertEqual(int.reaction_parameter, 0.1)
        self.assertEqual(int._dendritic_carrying_capacity, self.carrying_capacity)


if __name__ == '__main__':
    unittest.main()
