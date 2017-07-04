import unittest

from ComMeN import *


class DestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment_destroyed = 'a'
        self.infl_compartments = ['b','c']
        self.node = Patch(0, ['a','b','c','d'])
        self.event = Destroy(0.1, [self.node], self.compartment_destroyed)
        self.event_infl = Destroy(0.2, [self.node], self.compartment_destroyed, self.infl_compartments)
        uh = UpdateHandler([self.event, self.event_infl])

    def test_rates(self):
        self.assertEqual(self.event.rate, 0.1 * 0)
        self.assertEqual(self.event_infl.rate, 0.2 * 0)

        self.node.update('a', 1)
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * 0)

        self.node.update('b', 2)
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * 2)

        self.node.update('c', 3)
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * (2+3))

    def test_perform(self):
        self.node.update('a', 1)
        self.assertEqual(self.node[self.compartment_destroyed], 1)
        self.event.perform()
        self.assertEqual(self.node[self.compartment_destroyed], 0)


if __name__ == '__main__':
    unittest.main()
