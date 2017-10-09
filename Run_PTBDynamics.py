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

time_limit = 1
network_config_filename = 'Experiments/1/PulmonaryNetwork.cfg'
event_config_filename = 'Experiments/1/PTBModel_Events.cfg'
seeding_config_filename = 'Experiments/1/PTBModel_Seeding.cfg'

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

for run_id in range(1, 2):
    import cProfile
    cp = cProfile.Profile()

    model = PTBDynamics(network_config, event_config)
    cp.enable()
    model.run(time_limit, seeding, 1, 0.1)
    cp.disable()
    cp.print_stats("tottime")
