#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from PTBComMeN import *
import ConfigParser as cp

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

#
# EXPERIMENT 1 - BACTERIA ONLY
#
# Only bacteria compartments/events. No translocation.
# So looking at how the differences in environment affect just bacterial growth.
#
# ISSUES - bacteria can't be destroyed and there's no carrying capacity, so they grow like crazy
#

time_limit = 5.0
network_config_filename = 'PulmonaryNetwork_EXP1.cfg'
event_config_filename = 'PTBModel_Events_EXP1.cfg'
seeding_config_filename = 'PTBModel_Seeding_EXP1.cfg'

network_config = cp.ConfigParser()
network_config.read(network_config_filename)
event_config = cp.ConfigParser()
event_config.read(event_config_filename)

# Seed
seeding_config = cp.ConfigParser()
seeding_config.read(seeding_config_filename)
seeding = {}
for node_id in ALL_BPS + [LYMPH]:
    if node_id in seeding_config.sections():
        seeding[node_id] = {}
        for compartment, value in seeding_config.items(node_id):
            seeding[node_id][compartment] = float(value)

for run_id in range(1, 11):
    model = PTBDynamics(network_config, event_config)
    model.run(time_limit, seeding, run_id, 0.1)
