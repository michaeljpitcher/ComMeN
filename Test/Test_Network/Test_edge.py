import unittest

from ComMeN.Network.Edge import *


class EdgeTestCase(unittest.TestCase):
    def setUp(self):
        self.edge = Edge(('a','b'))
        self.edge_directed = Edge(('c', 'd'), True)

    def test_initialise(self):
        self.assertEqual(self.edge.node1, 'a')
        self.assertEqual(self.edge.node2, 'b')
        self.assertFalse(self.edge.directed)
        self.assertEqual(self.edge_directed.node1, 'c')
        self.assertEqual(self.edge_directed.node2, 'd')
        self.assertTrue(self.edge_directed.directed)

if __name__ == '__main__':
    unittest.main()
