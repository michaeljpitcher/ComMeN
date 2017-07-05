import unittest

from ComMeN.Network import *


class NetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [Patch(0, ['a']), Patch(1, ['a'])]
        self.edges = [Edge(self.nodes[0], self.nodes[1])]
        self.network = MetapopulationNetwork(self.nodes, self.edges)

    def test_initialise(self):
        self.assertItemsEqual(self.network.nodes, self.nodes)
        self.assertItemsEqual(self.network.edges, self.edges)

        # Test fail patch - non-unique IDs
        nodes = [Patch(0, ['a']), Patch(0, ['a'])]
        edges = [Edge(nodes[0], nodes[1])]
        with self.assertRaises(AssertionError) as context:
            network_full = MetapopulationNetwork(nodes, self.edges)
        self.assertEqual(str(context.exception), 'Node ID 0 already exists in network')

        # test fail edge - node not in network
        nodes = [Patch(0, ['a']), Patch(1, ['a'])]
        edges = [Edge(nodes[0], Patch(3, ['a']))]
        with self.assertRaises(AssertionError) as context:
            network_full = MetapopulationNetwork(nodes, self.edges)
        self.assertTrue('is not in the network' in str(context.exception))


