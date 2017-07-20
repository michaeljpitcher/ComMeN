import unittest
from LungComMeN import *


class LymphPatchTestCase(unittest.TestCase):
    def setUp(self):
        self.patch = LymphPatch(0, ['a'])

if __name__ == '__main__':
    unittest.main()
