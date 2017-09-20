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

run_id = 1
time_limit = 5

network_config_filename = DEFAULT_NETWORK_CONFIG_FILE
network_config = cp.ConfigParser()
network_config.read(network_config_filename)

event_config_filename = DEFAULT_EVENT_CONFIG_FILE
event_config = cp.ConfigParser()
event_config.read(event_config_filename)

model = PTBDynamics(network_config, event_config)

# Seed
seeding_config_filename = 'PTBModel_Seeding.cfg'
seeding_config = cp.ConfigParser()
seeding_config.read(seeding_config_filename)
seeding = {}
for node_id in ALL_BPS + [LYMPH]:
    if node_id in seeding_config.sections():
        seeding[node_id] = {}
        for compartment, value in seeding_config.items(node_id):
            seeding[node_id][compartment] = float(value)


# model.run(time_limit, seeding, True, run_id)

# draw_multiple_nodes_graph("1.csv", [MACROPHAGE_REGULAR])