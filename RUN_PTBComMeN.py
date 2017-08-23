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


config_filename = 'PTBModel.cfg'
config = cp.ConfigParser()
config.read(config_filename)

# Network set-up
joining_method = config.get("Network", "lung_edge_joining")
vents = {}
for (bps_id, value) in config.items("Ventilations"):
    vents[bps_id] = float(value)
perfs = {}
for (bps_id, value) in config.items("Perfusions"):
    perfs[bps_id] = float(value)

# Events
event_parameters = {}
for (parameter, value) in config.items("Event_parameters"):
    event_parameters[parameter] = float(value)

model = PTBDynamics(vents, perfs, joining_method, event_parameters)

#
# time_limit = 0
#
# # TODO - seeding
# seeding = None
#
# model.run(time_limit, seeding)