import unittest
from PTBComMeN import *


class RegularMacrophageDestroysBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_REGULAR, BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = RegularMacrophageDestroysBacteria(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_REGULAR: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_REGULAR: 2, BACTERIUM_EXTRACELLULAR_FAST:5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_REGULAR], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 4)


class ActivatedMacrophageDestroysBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        compartments = [MACROPHAGE_ACTIVATED, BACTERIUM_EXTRACELLULAR_FAST]
        self.nodes = [LungPatch(0, compartments, 0.9, 0.3)]
        self.event = ActivatedMacrophageDestroysBacteria(0.1, self.nodes, BACTERIUM_EXTRACELLULAR_FAST)
        uh = UpdateHandler([self.event])

    def test_rate(self):
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({MACROPHAGE_ACTIVATED: 2})
        self.assertEqual(self.event.rate, 0)
        self.nodes[0].update({BACTERIUM_EXTRACELLULAR_FAST: 3})
        self.assertEqual(self.event.rate, 0.1 * 2 * 3)

    def test_update(self):
        self.nodes[0].update({MACROPHAGE_ACTIVATED: 2, BACTERIUM_EXTRACELLULAR_FAST:5})
        self.event.perform()
        self.assertEqual(self.nodes[0][MACROPHAGE_ACTIVATED], 2)
        self.assertEqual(self.nodes[0][BACTERIUM_EXTRACELLULAR_FAST], 4)


class GetMacrophageDestroyBacteriaEventsTestCase(unittest.TestCase):

    def setUp(self):
        self.nodes = [LungPatch(0, ALL_TB_COMPARTMENTS, 0.9, 0.3)]
        self.regular_rates = {BACTERIUM_EXTRACELLULAR_FAST: 0.1, BACTERIUM_EXTRACELLULAR_SLOW: 0.2}
        self.activated_rates = {BACTERIUM_EXTRACELLULAR_FAST: 0.3, BACTERIUM_EXTRACELLULAR_SLOW: 0.4}
        self.events = get_macrophage_destroy_bacteria_events(self.nodes, self.regular_rates, self.activated_rates)

    def test_events(self):
        self.assertEqual(len(self.events), 4)
        regular_fast = next(e for e in self.events if isinstance(e, RegularMacrophageDestroysBacteria) and
                            e._compartment_destroyed == BACTERIUM_EXTRACELLULAR_FAST)
        self.assertEqual(regular_fast.reaction_parameter, 0.1)
        regular_slow = next(e for e in self.events if isinstance(e, RegularMacrophageDestroysBacteria) and
                            e._compartment_destroyed == BACTERIUM_EXTRACELLULAR_SLOW)
        self.assertEqual(regular_slow.reaction_parameter, 0.2)
        activated_fast = next(e for e in self.events if isinstance(e, ActivatedMacrophageDestroysBacteria) and
                              e._compartment_destroyed == BACTERIUM_EXTRACELLULAR_FAST)
        self.assertEqual(activated_fast.reaction_parameter, 0.3)
        activated_slow = next(e for e in self.events if isinstance(e, ActivatedMacrophageDestroysBacteria) and
                              e._compartment_destroyed == BACTERIUM_EXTRACELLULAR_SLOW)
        self.assertEqual(activated_slow.reaction_parameter, 0.4)


if __name__ == '__main__':
    unittest.main()
