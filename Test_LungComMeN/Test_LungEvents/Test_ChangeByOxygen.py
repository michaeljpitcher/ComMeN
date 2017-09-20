import unittest
from LungComMeN import *


class ChangeByOxygenTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a', 'b']

        self.nodes = [LungPatch(1, self.compartments, 0.9, 1.0),
                      LungPatch(2, self.compartments, 2.0, 1.0)]
        self.event_high = ChangeByOxygen_OLD(0.1, self.nodes, self.compartments[0], self.compartments[1], False)
        self.event_low = ChangeByOxygen_OLD(0.1, self.nodes, self.compartments[1], self.compartments[0], True)
        uh = UpdateHandler([self.event_high, self.event_low])

    def test_initialise(self):
        self.assertTrue(isinstance(self.event_low, Change))
        self.assertTrue(isinstance(self.event_high, Change))
        self.assertEqual(self.event_high._compartment_from, self.compartments[0])
        self.assertEqual(self.event_high._compartment_to, self.compartments[1])
        self.assertFalse(self.event_high._oxygen_low)
        self.assertEqual(self.event_low._compartment_from, self.compartments[1])
        self.assertEqual(self.event_low._compartment_to, self.compartments[0])
        self.assertTrue(self.event_low._oxygen_low)

    def test_calculate_state_variable_at_node(self):
        for e in [self.event_high, self.event_low]:
            for n in self.nodes:
                self.assertEqual(e._calculate_state_variable_at_node(n), 0)

        self.nodes[0].update({self.compartments[0]: 2, self.compartments[1]: 3})
        state_var_high = self.event_high._calculate_state_variable_at_node(self.nodes[0])
        state_var_low = self.event_low._calculate_state_variable_at_node(self.nodes[0])
        self.assertEqual(state_var_high, 2 * self.nodes[0].oxygen_tension)
        self.assertEqual(state_var_low, 3 * (1 / self.nodes[0].oxygen_tension))

        self.nodes[1].update({self.compartments[0]: 2, self.compartments[1]: 3})
        state_var_high = self.event_high._calculate_state_variable_at_node(self.nodes[1])
        state_var_low = self.event_low._calculate_state_variable_at_node(self.nodes[1])
        self.assertEqual(state_var_high, 2 * self.nodes[1].oxygen_tension)
        self.assertEqual(state_var_low, 3 * (1 / self.nodes[1].oxygen_tension))


class ChangeByOxygenVersion2TestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a', 'b']

        self.sigmoid_high = -1.0
        self.sigmoid_low = 1.0

        self.half_sat = 1.0

        self.nodes = [LungPatch(1, self.compartments, 0.5, 1.0),
                      LungPatch(2, self.compartments, 2.0, 1.0)]
        self.event_high = ChangeByOxygen(0.1, self.nodes, self.compartments[0], self.compartments[1],
                                         self.sigmoid_high, self.half_sat)
        self.event_low = ChangeByOxygen(0.1, self.nodes, self.compartments[1], self.compartments[0],
                                        self.sigmoid_low, self.half_sat)
        uh = UpdateHandler([self.event_high, self.event_low])

    def test_initialise(self):
        self.assertTrue(isinstance(self.event_low, Change))
        self.assertTrue(isinstance(self.event_high, Change))
        self.assertEqual(self.event_high._compartment_from, self.compartments[0])
        self.assertEqual(self.event_high._compartment_to, self.compartments[1])
        self.assertEqual(self.event_high._sigmoid, self.sigmoid_high)
        self.assertEqual(self.event_low._compartment_from, self.compartments[1])
        self.assertEqual(self.event_low._compartment_to, self.compartments[0])
        self.assertEqual(self.event_low._sigmoid, self.sigmoid_low)

    def test_calculate_state_variable_at_node(self):
        for e in [self.event_high, self.event_low]:
            for n in self.nodes:
                self.assertEqual(e._calculate_state_variable_at_node(n), 0)
        self.nodes[0].update({self.compartments[0]: 2, self.compartments[1]: 3})
        self.assertEqual(self.event_high._calculate_state_variable_at_node(self.nodes[0]),
                         2 * (self.nodes[0].oxygen_tension ** self.sigmoid_high) /
                         (self.half_sat ** self.sigmoid_high + self.nodes[0].oxygen_tension ** self.sigmoid_high))
        self.assertEqual(self.event_low._calculate_state_variable_at_node(self.nodes[0]),
                         3 * (self.nodes[0].oxygen_tension ** self.sigmoid_low) /
                         (self.half_sat ** self.sigmoid_low + self.nodes[0].oxygen_tension ** self.sigmoid_low))

        self.nodes[1].update({self.compartments[0]: 2, self.compartments[1]: 3})
        self.assertEqual(self.event_high._calculate_state_variable_at_node(self.nodes[1]),
                         2 * (self.nodes[1].oxygen_tension ** self.sigmoid_high) /
                         (self.half_sat ** self.sigmoid_high + self.nodes[1].oxygen_tension ** self.sigmoid_high))
        self.assertEqual(self.event_low._calculate_state_variable_at_node(self.nodes[1]),
                         3 * (self.nodes[1].oxygen_tension ** self.sigmoid_low) /
                         (self.half_sat ** self.sigmoid_low + self.nodes[1].oxygen_tension ** self.sigmoid_low))


if __name__ == '__main__':
    unittest.main()
