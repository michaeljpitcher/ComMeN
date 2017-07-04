import unittest

from ComMeN import *


class EdgeTestCase(unittest.TestCase):
    def setUp(self):
        self.patches = [Patch(1, ['a','b']), Patch(2, ['a','b']), Patch(3, ['a','b']), Patch(4, ['a','b']), ]
        self.edge = Edge(self.patches[0], self.patches[1])
        self.edge_directed = Edge(self.patches[2], self.patches[3], True)

    def test_initialise(self):
        self.assertFalse(self.edge.directed)
        self.assertTrue(self.edge_directed.directed)

        self.assertItemsEqual(self.patches[0].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.patches[0].adjacent_edges[Edge], [self.edge])
        self.assertItemsEqual(self.patches[1].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.patches[1].adjacent_edges[Edge], [self.edge])
        self.assertItemsEqual(self.patches[2].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.patches[2].adjacent_edges[Edge], [self.edge_directed])
        self.assertItemsEqual(self.patches[3].adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.patches[3].adjacent_edges[Edge], [self.edge_directed])

    def test_getitem(self):
        self.assertEqual(self.edge[self.patches[0]], self.patches[1])
        self.assertEqual(self.edge[self.patches[1]], self.patches[0])

if __name__ == '__main__':
    unittest.main()
