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

create_event_config_file("test")

network_config_filename = DEFAULT_NETWORK_CONFIG_FILE
network_config = cp.ConfigParser()
network_config.read(network_config_filename)

event_config_filename = DEFAULT_EVENT_CONFIG_FILE
event_config = cp.ConfigParser()
event_config.read(event_config_filename)

model = PTBDynamics(network_config, event_config)
