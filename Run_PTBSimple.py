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

test_file_name = 'test.cfg'
#
# create_event_config_file(test_file_name)

network_config_filename = DEFAULT_NETWORK_CONFIG_FILE
network_config = cp.ConfigParser()
network_config.read(network_config_filename)

event_config_filename = test_file_name
event_config = cp.ConfigParser()
event_config.read(event_config_filename)

model = PTBDynamicsSimple(network_config, event_config)

seeding = {APICAL_RIGHT: {BACTERIUM_FAST: 100}}

model.run(100, seeding, True, 1)