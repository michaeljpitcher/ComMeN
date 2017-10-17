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
# EXPERIMENT 2 - Bacteria switching and replication
#
# Seeding:
# Each patch is seeded with fast and slow bacteria.
#
# Events:
# Bacteria switch by oxygen
# (Extracellular) bacteria replicate

time_limit = 5.0
network_config_filename = 'PulmonaryNetwork_EXP2.cfg'
event_config_filename = 'PTBModel_Events_EXP2.cfg'
seeding_config_filename = 'PTBModel_Seeding_EXP2.cfg'

network_config = cp.ConfigParser()
network_config.read(network_config_filename)
event_config = cp.ConfigParser()
event_config.read(event_config_filename)

# Seed
seeding_config = cp.ConfigParser()
seeding_config.read(seeding_config_filename)
seeding = {}

for node_id in LUNG_BPS + [LYMPH]:
    if node_id in seeding_config.sections():
        seeding[node_id] = {}
        for compartment, value in seeding_config.items(node_id):
            seeding[node_id][compartment] = float(value)

for run_id in range(1, 11):
    model = PTBDynamics(network_config, event_config)
    model.run(time_limit, seeding, run_id, 0.1)
