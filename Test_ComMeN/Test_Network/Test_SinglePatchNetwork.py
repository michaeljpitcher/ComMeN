import unittest

from ComMeN import *


class SinglePatchNetworkTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b','c']
        self.network = SinglePatchMetapopulation(compartments)

    def test_initialise(self):
        self.assertEqual(len(self.network.nodes), 1)
        self.assertFalse(self.network.edges)
