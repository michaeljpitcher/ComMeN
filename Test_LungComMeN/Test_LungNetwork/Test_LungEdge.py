import unittest
from LungComMeN import *


class LungEdgeTestCase(unittest.TestCase):
    def setUp(self):
        self.node1 = Patch(0, ['a'])
        self.node2 = Patch(1, ['a'])
        self.weight = 3
        self.edge = LungEdge(self.node1, self.node2, self.weight)

    def test_initialise(self):
        self.assertEqual(self.edge.weight, self.weight)
        self.assertFalse(self.edge.directed)


if __name__ == '__main__':
    unittest.main()
