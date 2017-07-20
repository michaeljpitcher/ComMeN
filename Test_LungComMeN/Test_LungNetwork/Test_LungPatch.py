import unittest
from LungComMeN import *


class LungPatchTestCase(unittest.TestCase):
    def setUp(self):
        self.vent = 0.9
        self.perf = 0.1
        self.patch = LungPatch(0, ['a'], self.vent, self.perf)
        self.vent2 = 0.4
        self.perf2 = 0.8
        self.patch_no_o2 = LungPatch(0, ['a'], self.vent2, self.perf2)

    def test_initialise(self):
        self.assertEqual(self.patch.ventilation, self.vent)
        self.assertEqual(self.patch.perfusion, self.perf)
        self.assertEqual(self.patch.oxygen_tension, self.vent-self.perf)
        self.assertEqual(self.patch_no_o2.ventilation, self.vent2)
        self.assertEqual(self.patch_no_o2.perfusion, self.perf2)
        self.assertEqual(self.patch_no_o2.oxygen_tension, 0)


if __name__ == '__main__':
    unittest.main()
