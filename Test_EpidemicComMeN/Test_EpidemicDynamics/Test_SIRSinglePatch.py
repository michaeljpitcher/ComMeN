import unittest

from EpidemicComMeN import *


class InfectTestCase(unittest.TestCase):
    def setUp(self):
        self.birth_rate = 0.1
        self.infection_rate = 3
        self.recovery_rate = 1/3.0
        self.death_rate = 0.1
        self.death_by_infection_rate = 0.001
        self.seeding = {0:}

        self.dynamics = SIRSinglePatchDynamics(self.birth_rate, self.infection_rate, self.recovery_rate,
                                               self.death_rate, self.death_by_infection_rate, self.seeding)