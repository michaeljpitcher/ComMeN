import unittest

from ComMeN import *


class NonAbstractEvent(Event):
    def __init__(self, reaction_parameter, nodes):
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        return node['a']

    def _update_node(self, node):
        node.update({'b':1})
        return [node]


class EventTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b']
        self.reaction_parameter = 0.1
        self.nodes = [Patch(None, compartments), Patch(None, compartments)]
        self.event = NonAbstractEvent(self.reaction_parameter, self.nodes)

    def test_initialise(self):
        self.assertEqual(self.event.rate, 0)

    def test_update_state_variable_from_node(self):
        self.event.update_state_variable_from_node(self.nodes[0])
        self.assertEqual(self.event.rate, 0)

        self.nodes[0].update({'a':2})
        self.event.update_state_variable_from_node(self.nodes[0])
        self.assertEqual(self.event.rate, 0.1 * 2)
        self.nodes[1].update({'a':3})
        self.event.update_state_variable_from_node(self.nodes[1])
        self.assertEqual(self.event.rate, 0.1 * 5)
        self.nodes[1].update({'a':-1})
        self.event.update_state_variable_from_node(self.nodes[1])
        self.assertEqual(self.event.rate, 0.1 * 4)

    def test_perform(self):
        self.nodes[0].update({'a':2})
        self.event.update_state_variable_from_node(self.nodes[0])
        self.assertEqual(self.event.rate, 0.1 * 2)
        result = self.event.perform()


if __name__ == '__main__':
    unittest.main()
