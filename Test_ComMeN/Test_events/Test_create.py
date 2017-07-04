import unittest

from ComMeN import *


class CreateTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment_created = 'a'
        self.infl_compartments = ['b','c']
        self.node = Patch(0, ['a','b','c','d'])
        self.event = Create(0.1, [self.node], self.compartment_created)
        self.event_infl = Create(0.2, [self.node], self.compartment_created, self.infl_compartments)
        uh = UpdateHandler([self.event, self.event_infl])

    def test_rates(self):
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_infl.rate, 0.2 * 0)

        self.node.update({'b':2})
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_infl.rate, 0.2 * 2)

        self.node.update({'c':3})
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_infl.rate, 0.2 * 5)

        self.node.update({'d':4})
        self.assertEqual(self.event.rate, 0.1)
        self.assertEqual(self.event_infl.rate, 0.2 * 5)

    def test_perform(self):
        self.assertEqual(self.node[self.compartment_created], 0)
        self.event.perform()
        self.assertEqual(self.node[self.compartment_created], 1)


if __name__ == '__main__':
    unittest.main()
