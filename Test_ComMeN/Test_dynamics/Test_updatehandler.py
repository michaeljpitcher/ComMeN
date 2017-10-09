import unittest

from ComMeN import *


class NonAbstractEvent(Event):
    def __init__(self, reaction_parameter, nodes):
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        return node['a']

    def _update_node(self, node):
        node.update('b', 1)
        return [node]


class UpdateHandlerTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b']
        self.nodes = [Patch(0, compartments), Patch(1, compartments)]
        self.nodes[0]._subpopulation['a'] = 1
        self.nodes[1]._subpopulation['a'] = 13
        self.events = [NonAbstractEvent(0.1, [self.nodes[0]]), NonAbstractEvent(0.2, [self.nodes[1]]),
                       NonAbstractEvent(0.3, [self.nodes[0]])]
        self.update_handler = UpdateHandler(self.events)

    def test_initialise(self):
        self.assertEqual(self.nodes[0]._subpopulation['a'], 1)
        self.assertEqual(self.nodes[1]._subpopulation['a'], 13)
        self.assertItemsEqual(self.events[0].state_variable_composition.keys(), [self.nodes[0].node_id])
        self.assertItemsEqual(self.events[1].state_variable_composition.keys(), [self.nodes[1].node_id])
        self.assertItemsEqual(self.events[2].state_variable_composition.keys(), [self.nodes[0].node_id])
        self.assertEqual(self.events[0].rate, 0.1 * 1)
        self.assertEqual(self.events[1].rate, 0.2 * 13)
        self.assertEqual(self.events[2].rate, 0.3 * 1)

    def test_propagate_node_update(self):
        self.nodes[0]._subpopulation['a'] = 2
        self.update_handler.propagate_node_update(self.nodes[0])
        self.assertEqual(self.events[0].rate, 0.1 * 2)
        self.assertEqual(self.events[1].rate, 0.2 * 13)
        self.assertEqual(self.events[2].rate, 0.3 * 2)
        self.nodes[1]._subpopulation['a'] = 88
        self.update_handler.propagate_node_update(self.nodes[1])
        self.assertEqual(self.events[0].rate, 0.1 * 2)
        self.assertEqual(self.events[1].rate, 0.2 * 88)
        self.assertEqual(self.events[2].rate, 0.3 * 2)

