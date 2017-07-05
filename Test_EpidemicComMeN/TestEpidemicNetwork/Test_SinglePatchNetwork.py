import unittest

from EpidemicComMeN import *


class SinglePatchNetworkTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a','b','c']
        self.network = SinglePatchEpidemicNetwork(compartments)

    def test_initialise(self):
        self.assertEqual(len(self.network.nodes), 1)
        self.assertFalse(self.network.edges)
