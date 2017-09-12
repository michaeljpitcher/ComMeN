import unittest
from LungComMeN import *
import numpy as np


class RecruitmentByPerfusionTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a','b','c']

        self.nodes = [LungPatch(1, self.compartments, 1.0, 1.0),
                      LungPatch(2, self.compartments, 1.0, 2.0)]
        self.event = RecruitmentByPerfusion(0.1, self.nodes, self.compartments[0])
        self.event_infl = RecruitmentByPerfusion(0.1, self.nodes, self.compartments[0], [self.compartments[1],
                                                                                    self.compartments[2]])
        uh = UpdateHandler([self.event])

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Create))
        self.assertEqual(self.event._compartment_created, self.compartments[0])
        self.assertFalse(self.event._influencing_compartments)
        self.assertItemsEqual(self.event_infl._influencing_compartments, [self.compartments[1], self.compartments[2]])

    def test_calculate_state_variable_from_node(self):
        self.assertEqual(self.event._calculate_state_variable_at_node(self.nodes[0]), 1.0)
        self.assertEqual(self.event._calculate_state_variable_at_node(self.nodes[1]), 2.0)

        self.assertEqual(self.event_infl._calculate_state_variable_at_node(self.nodes[0]), 0.0)
        self.assertEqual(self.event_infl._calculate_state_variable_at_node(self.nodes[1]), 0.0)

        self.nodes[0].update({self.compartments[1]: 1, self.compartments[2]: 2})
        self.nodes[1].update({self.compartments[1]: 3, self.compartments[2]: 4})

        self.assertEqual(self.event_infl._calculate_state_variable_at_node(self.nodes[0]), 1.0 * 3)
        self.assertEqual(self.event_infl._calculate_state_variable_at_node(self.nodes[1]), 2.0 * 7)

if __name__ == '__main__':
    unittest.main()
