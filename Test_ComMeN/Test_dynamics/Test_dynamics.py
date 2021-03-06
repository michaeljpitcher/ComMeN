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


class DynamicsTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [Patch(0, ['a','b','c']), Patch(1, ['a','b','d'])]
        self.edges = [Edge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)
        self.events = [NonAbstractEvent(0.1, [self.nodes[0]]), NonAbstractEvent(0.2, [self.nodes[1]]),
                       NonAbstractEvent(0.3, [self.nodes[0]])]
        self.dynamics = Dynamics(self.network, self.events)

    def test_initialise(self):
        pass

    def test_run(self):
        rand.seed(101)
        seeding = {0: {'a':2}}

        self.dynamics.run(time_limit=100, seeding=seeding, run_id=99, timestep_for_data_record=1)
