import unittest
from LungComMeN import *


class LymphEdgeTestCase(unittest.TestCase):
    def setUp(self):
        self.node1 = Patch(0, ['a'])
        self.node2 = Patch(1, ['a'])
        self.drainage = 3
        self.edge = LymphEdge(self.node1, self.node2, False, self.drainage)

    def test_initialise(self):
        self.assertEqual(self.edge.drainage, self.drainage)


if __name__ == '__main__':
    unittest.main()
