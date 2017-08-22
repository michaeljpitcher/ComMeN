import unittest

from ComMeN import *


class Edge_Type1(Edge):
    def __init__(self, n1, n2, directed):
        Edge.__init__(self, n1, n2, directed)


class Edge_Type2(Edge):
    def __init__(self, n1, n2, directed):
        Edge.__init__(self, n1, n2, directed)


class TranslocateTestCase(unittest.TestCase):
    def setUp(self):
        compartments = ['a', 'b', 'c', 'd']
        self.nodes = [Patch(0, compartments), Patch(1, compartments), Patch(2, compartments), Patch(3, compartments),
                      Patch(4, compartments)]

        edges = [Edge_Type1(self.nodes[0], self.nodes[1], False), Edge_Type1(self.nodes[0], self.nodes[2], True),
                 Edge_Type2(self.nodes[0], self.nodes[3], False), Edge_Type2(self.nodes[4], self.nodes[0], True)]

        self.network = MetapopulationNetwork(self.nodes, edges)
        self.event = Translocate(0.1, self.nodes, compartments[0], edge_class=Edge_Type1)
        self.event_not_number_edges = Translocate(0.2, self.nodes, compartments[0], edge_class=Edge_Type2,
                                                  rate_increases_with_edges=False)
        self.event_influencers = Translocate(0.3, self.nodes, compartments[0], edge_class=Edge_Type1,
                                                  influencing_compartments=['b', 'c'])
        events = [self.event, self.event_not_number_edges, self.event_influencers]
        uh = UpdateHandler(events)

    def test_rates(self):
        self.nodes[0].update({'a': 1})
        self.nodes[1].update({'a': 2})
        self.nodes[2].update({'a': 3})
        self.nodes[3].update({'a': 4})
        self.nodes[4].update({'a': 5})
        self.assertEqual(self.event.rate, 0.1 * (self.nodes[0]['a'] * 2 + self.nodes[1]['a'] * 1 +
                                                 self.nodes[2]['a'] * 0 + self.nodes[3]['a'] * 0 +
                                                 self.nodes[4]['a'] * 0))
        self.assertEqual(self.event_not_number_edges.rate, 0.2 * (self.nodes[0]['a'] * 1 + self.nodes[1]['a'] * 0 +
                                                                  self.nodes[2]['a'] * 0 + self.nodes[3]['a'] * 1 +
                                                                  self.nodes[4]['a'] * 1))
        self.assertEqual(self.event_influencers.rate, 0)
        self.nodes[0].update({'b': 2})
        self.assertEqual(self.event_influencers.rate, 0.3 * self.nodes[0]['a'] * self.nodes[0]['b'] * 2)
        self.nodes[0].update({'c': 2})
        self.assertEqual(self.event_influencers.rate, 0.3 * self.nodes[0]['a'] *
                         (self.nodes[0]['b'] + self.nodes[0]['c']) * 2)

if __name__ == '__main__':
    unittest.main()
