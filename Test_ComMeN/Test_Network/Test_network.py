import unittest

from ComMeN.Network import *


class NetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [Patch(0, ['a', 'b', 'c']), Patch(9, ['a', 'b', 'c'])]
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

        self.assertItemsEqual(self.nodes[0].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.nodes[0].adjacent_edges[Edge], [self.edges[0]])
        self.assertItemsEqual(self.nodes[1].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.nodes[1].adjacent_edges[Edge], [self.edges[0]])

    def test_seed(self):
        self.network.seed({0:{'a':1, 'b':2}, 9:{'a':3, 'c':4}})
        self.assertEqual(self.nodes[0]['a'], 1)
        self.assertEqual(self.nodes[0]['b'], 2)
        self.assertEqual(self.nodes[0]['c'], 0)
        self.assertEqual(self.nodes[1]['a'], 3)
        self.assertEqual(self.nodes[1]['b'], 0)
        self.assertEqual(self.nodes[1]['c'], 4)

    def test_getitem(self):
        self.assertEqual(self.network[0], self.nodes[0])
        self.assertEqual(self.network[9], self.nodes[1])
        with self.assertRaises(Exception) as context:
            a = self.network[1]
        self.assertEqual(str(context.exception), "Node with id '1' not found in network")

    def test_reset(self):
        updates_1 = {'a':1,'b':2,'c':3}
        updates_2 = {'a':4,'b':5,'c':6}
        self.nodes[0].update(updates_1)
        self.nodes[1].update(updates_2)
        for comp in updates_1:
            self.assertEqual(self.nodes[0][comp], updates_1[comp])
            self.assertEqual(self.nodes[1][comp], updates_2[comp])
        self.network.reset()
        for comp in updates_1:
            self.assertEqual(self.nodes[0][comp], 0)
            self.assertEqual(self.nodes[1][comp], 0)
