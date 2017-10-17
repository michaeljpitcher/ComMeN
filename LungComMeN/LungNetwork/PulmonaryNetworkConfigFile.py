#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from BronchopulmonarySegments import *
import ConfigParser

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

NETWORK_CONFIGURATION_SECTIONS = ['Network_joining', 'Ventilations', 'Perfusions']
DEFAULT_NETWORK_CONFIG_FILE = "PulmonaryNetwork.cfg"
EDGE_WEIGHT_WITHIN_LOBE = "edge_weight_within_lobe"
EDGE_WEIGHT_BETWEEN_LOBE = "edge_weight_between_lobe"
LYMPH_DRAINAGE = "LymphaticDrainage"

def create_network_config_file(filename=DEFAULT_NETWORK_CONFIG_FILE):
    config_network_file = open(filename, 'w')
    config_network = ConfigParser.ConfigParser(allow_no_value=True)
    for n in NETWORK_CONFIGURATION_SECTIONS:
        config_network.add_section(n)
    # Set value for lung edge joining weights
    config_network.set(NETWORK_CONFIGURATION_SECTIONS[0], EDGE_WEIGHT_WITHIN_LOBE, 0)
    config_network.set(NETWORK_CONFIGURATION_SECTIONS[0], EDGE_WEIGHT_BETWEEN_LOBE, 0)

    config_network.set(NETWORK_CONFIGURATION_SECTIONS[1], "# Ventilation values for lung patches")
    config_network.set(NETWORK_CONFIGURATION_SECTIONS[2], "# Perfusion values for lung patches")
    # Set ventilation / perfusion values (as 1)
    for bps in LUNG_BPS:
        config_network.set(NETWORK_CONFIGURATION_SECTIONS[1], bps, 1.0)
        config_network.set(NETWORK_CONFIGURATION_SECTIONS[2], bps, 1.0)
    # Write to file and close
    config_network.write(config_network_file)
    config_network_file.close()
