import unittest

from ComMeN import *


class ChangeTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment_from = 'a'
        self.compartment_to = 'd'
        self.infl_compartments = ['b','c']
        self.node = Patch(0, ['a','b','c','d'])
        self.event = Change(0.1, [self.node], self.compartment_from, self.compartment_to)
        self.event_infl = Change(0.2, [self.node], self.compartment_from, self.compartment_to, self.infl_compartments)
        uh = UpdateHandler([self.event, self.event_infl])

    def test_rates(self):
        self.assertEqual(self.event.rate, 0.1 * 0)
        self.assertEqual(self.event_infl.rate, 0.2 * 0)

        self.node.update({'a':1})
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * 0)

        self.node.update({'b':2})
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * 2)

        self.node.update({'c':3})
        self.assertEqual(self.event.rate, 0.1 * 1)
        self.assertEqual(self.event_infl.rate, 0.2 * 1 * (2+3))

    def test_perform(self):
        self.node.update({'a':1})
        self.assertEqual(self.node[self.compartment_from], 1)
        self.assertEqual(self.node[self.compartment_to], 0)
        self.event.perform()
        self.assertEqual(self.node[self.compartment_from], 0)
        self.assertEqual(self.node[self.compartment_to], 1)


if __name__ == '__main__':
    unittest.main()
