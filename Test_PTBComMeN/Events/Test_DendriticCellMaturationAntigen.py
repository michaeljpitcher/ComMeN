import unittest
from PTBComMeN import *


class DendriticCellMaturationAntigenTestCase(unittest.TestCase):
    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.event = DendriticCellMaturationAntigen(0.1, self.nodes, MACROPHAGE_INFECTED)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 10})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_INFECTED: 7})
        self.assertEqual(self.event.rate, 7.0)

    def test_update(self):
        self.nodes[0].update({DENDRITIC_CELL_IMMATURE: 10, MACROPHAGE_INFECTED: 1})
        self.event.perform()
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_IMMATURE], 9)
        self.assertEqual(self.nodes[0][DENDRITIC_CELL_MATURE], 1)


class GetDendriticCellMaturationAntigenEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.rates = {MACROPHAGE_INFECTED: 0.1, MACROPHAGE_ACTIVATED: 0.2}
        self.events = get_dendritic_cell_maturation_antigen_events(self.nodes, self.rates)

    def test_events(self):
        self.assertEqual(len(self.events), len(self.rates))
        for ap, rate in self.rates.iteritems():
            event = next(n for n in self.events if n._influencing_compartments[0] == ap)
            self.assertEqual(event.reaction_parameter, rate)


if __name__ == '__main__':
    unittest.main()
