import unittest

from ComMeN.Network import *


class NetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.network_empty = MetapopulationNetwork()
        self.nodes = [Patch(['a']), Patch(['a'])]
        self.edges = [Edge(self.nodes[0], self.nodes[1])]
        self.network_full = MetapopulationNetwork(self.nodes, self.edges)

    def test_initialise(self):
        self.assertFalse(len(self.network_empty.nodes))
        self.assertFalse(len(self.network_empty.edges))
        self.assertItemsEqual(self.network_full.nodes, self.nodes)
        self.assertItemsEqual(self.network_full.edges, self.edges)


    def test_add_node(self):
        p = Patch(['a','b'])
        self.network_empty.add_node(p)
        self.assertItemsEqual(self.network_empty.nodes, [p])

        # Fail - not a Patch instance
        with self.assertRaises(AssertionError) as context:
            self.network_empty.add_node("c")
        self.assertEqual('Node c is not instance of Patch class', str(context.exception))

    def test_add_edge(self):
        p1 = Patch(['a', 'b'])
        p2 = Patch(['a', 'b'])
        self.network_empty.add_node(p1)
        self.network_empty.add_node(p2)
        edge = Edge(p1, p2)
        self.network_empty.add_edge(edge)
        self.assertItemsEqual(self.network_empty.nodes, [p1,p2])
        self.assertItemsEqual(self.network_empty.edges, [edge])

        # Fail - node1 not in network
        p3 = Patch(['a', 'b'])
        edge2 = Edge(p3, p2)
        with self.assertRaises(AssertionError) as context:
            self.network_empty.add_edge(edge2)
        self.assertTrue('is not in the network' in str(context.exception))
        edge3 = Edge(p1, p3)
        with self.assertRaises(AssertionError) as context:
            self.network_empty.add_edge(edge3)
        self.assertTrue('is not in the network' in str(context.exception))
