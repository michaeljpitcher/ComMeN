import unittest

from ComMeN import *

class PatchTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a','b','c']
        self.patch = Patch(1, self.compartments)

    def test_initialise(self):
        self.assertEqual(self.patch.node_id, 1)
        self.assertItemsEqual(self.patch._subpopulation.keys(), self.compartments)
        for c in self.compartments:
            self.assertEqual(self.patch._subpopulation[c], 0)
        self.assertFalse(len(self.patch.adjacent_edges))
        self.assertFalse(self.patch.update_handler)

    def test_update(self):
        self.patch.update({self.compartments[0]:9})
        self.assertEqual(self.patch._subpopulation[self.compartments[0]], 9)
        self.assertEqual(self.patch._subpopulation[self.compartments[1]], 0)
        self.assertEqual(self.patch._subpopulation[self.compartments[2]], 0)

        # Fail - negative value
        with self.assertRaises(AssertionError) as context:
            self.patch.update({self.compartments[1]:-1})
        self.assertEqual('New value cannot be negative', str(context.exception))

    def test_add_adjacent_edge(self):
        patch2 = Patch(2, self.compartments)
        e = Edge(self.patch, patch2)
        self.patch.adjacent_edges.clear()
        self.patch.add_adjacent_edge(e)
        self.assertItemsEqual(self.patch.adjacent_edges.keys(), [Edge])
        self.assertItemsEqual(self.patch.adjacent_edges[Edge], [e])

    def test_reset(self):
        self.patch.update({'a':1,'b':2,'c':3})
        self.assertEqual(self.patch['a'], 1)
        self.assertEqual(self.patch['b'], 2)
        self.assertEqual(self.patch['c'], 3)
        self.patch.reset()
        for comp in ['a','b','c']:
            self.assertEqual(self.patch[comp], 0)

if __name__ == '__main__':
    unittest.main()
