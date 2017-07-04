import unittest

from ComMeN.Network.Patch import Patch


class PatchTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a','b','c']
        self.patch = Patch(1, self.compartments)

    def test_initialise(self):
        self.assertEqual(self.patch.node_id, 1)
        self.assertItemsEqual(self.patch._subpopulation.keys(), self.compartments)
        for c in self.compartments:
            self.assertEqual(self.patch._subpopulation[c], 0)
        self.assertFalse(len(self.patch.neighbours))
        self.assertFalse(self.patch.update_handler)

    def test_update(self):
        self.patch.update(self.compartments[0], 9)
        self.assertEqual(self.patch._subpopulation[self.compartments[0]], 9)
        self.assertEqual(self.patch._subpopulation[self.compartments[1]], 0)
        self.assertEqual(self.patch._subpopulation[self.compartments[2]], 0)

        # Fail - negative value
        with self.assertRaises(AssertionError) as context:
            self.patch.update(self.compartments[1], -1)
        self.assertEqual('New value cannot be negative', str(context.exception))

        # TODO - With update handler

if __name__ == '__main__':
    unittest.main()
