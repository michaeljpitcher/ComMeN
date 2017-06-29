import unittest
from ComMeN.Patch.Patch import Patch


class PatchTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a','b','c']
        self.patch = Patch(self.compartments)

    def test_initialise(self):
        self.assertItemsEqual(self.patch.subpopulation.keys(), self.compartments)
        for c in self.compartments:
            self.assertEqual(self.patch.subpopulation[c], 0)

    def test_update(self):
        self.patch.update(self.compartments[0], 9)
        self.assertEqual(self.patch.subpopulation[self.compartments[0]], 9)
        self.assertEqual(self.patch.subpopulation[self.compartments[1]], 0)
        self.assertEqual(self.patch.subpopulation[self.compartments[2]], 0)

        # Fail negative
        with self.assertRaises(AssertionError) as context:
            self.patch.update(self.compartments[1], -1)
        self.assertEqual('New value cannot be negative', str(context.exception))


if __name__ == '__main__':
    unittest.main()
