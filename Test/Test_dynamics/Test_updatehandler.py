import unittest

from ComMeN.Dynamics import *
from ComMeN.Network import *


class NonAbstractEvent(Event):
    def __init__(self, reaction_parameter, nodes):
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        return node.subpopulation['a']

    def _update_node(self, node):
        node.update('b', 1)
        return [node]


class UpdateHandlerTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b']
        self.nodes = [Patch(compartments), Patch(compartments)]
        self.nodes[0].subpopulation['a'] = 1
        self.nodes[1].subpopulation['a'] = 13
        self.events = [NonAbstractEvent(0.1, [self.nodes[0]]), NonAbstractEvent(0.2, [self.nodes[1]]),
                       NonAbstractEvent(0.3, [self.nodes[0]])]
        self.update_handler = UpdateHandler(self.events)

    def test_initialise(self):
        self.assertEqual(self.nodes[0].subpopulation['a'], 1)
        self.assertEqual(self.nodes[1].subpopulation['a'], 13)
        self.assertItemsEqual(self.events[0].state_variable_composition.keys(), [self.nodes[0]])
        self.assertItemsEqual(self.events[1].state_variable_composition.keys(), [self.nodes[1]])
        self.assertItemsEqual(self.events[2].state_variable_composition.keys(), [self.nodes[0]])
        self.assertEqual(self.events[0].probability, 0.1 * 1)
        self.assertEqual(self.events[1].probability, 0.2 * 13)
        self.assertEqual(self.events[2].probability, 0.3 * 1)

    def test_propagate_node_update(self):
        self.nodes[0].subpopulation['a'] = 2
        self.update_handler.propagate_node_update(self.nodes[0])
        self.assertEqual(self.events[0].probability, 0.1 * 2)
        self.assertEqual(self.events[1].probability, 0.2 * 13)
        self.assertEqual(self.events[2].probability, 0.3 * 2)
        self.nodes[1].subpopulation['a'] = 88
        self.update_handler.propagate_node_update(self.nodes[1])
        self.assertEqual(self.events[0].probability, 0.1 * 2)
        self.assertEqual(self.events[1].probability, 0.2 * 88)
        self.assertEqual(self.events[2].probability, 0.3 * 2)

