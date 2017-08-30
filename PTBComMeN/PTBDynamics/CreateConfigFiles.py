#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from PTBDynamics import *
from ..PTBEvents import *
import ConfigParser

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def create_network_config_file(filename=DEFAULT_NETWORK_CONFIG_FILE):
    config_network_file = open(filename, 'w')
    config_network = ConfigParser.ConfigParser()
    for n in NETWORK_CONFIGURATION_SECTIONS:
        config_network.add_section(n)
    # Set value for joining
    config_network.set(NETWORK_CONFIGURATION_SECTIONS[0], LUNG_EDGE_JOINING, JOINING_NONE)
    # Set ventilation / perfusion values (as 1)
    for bps in ALL_BPS:
        config_network.set(NETWORK_CONFIGURATION_SECTIONS[1], bps, 1.0)
        config_network.set(NETWORK_CONFIGURATION_SECTIONS[2], bps, 1.0)
    # Write to file and close
    config_network.write(config_network_file)
    config_network_file.close()


def create_event_config_file(filename=DEFAULT_EVENT_CONFIG_FILE):
    config_event_file = open(filename, 'w')
    config_event = ConfigParser.ConfigParser()
    for n in EVENT_CONFIGURATION_SECTIONS:
        config_event.add_section(n)

    for o in BACTERIA_CHANGE_STATE_OPTIONS:
        config_event.set(BacteriaChangeByOxygen.__name__, o, 0.0)

    for o in BACTERIA_REPLICATION_OPTIONS:
        config_event.set(BacteriaReplication.__name__, o, 0.0)

    for o in BACTERIA_TRANSLOCATION_OPTIONS:
        config_event.set(BacteriaTranslocateLung.__name__, o, 0.0)
        config_event.set(BacteriaTranslocateLymph.__name__, o, 0.0)
        config_event.set(BacteriaTranslocateBlood.__name__, o, 0.0)

    for o in MACROPHAGE_ACTIVATION_OPTIONS:
        config_event.set(MacrophageActivationByExternal.__name__, o, 0.0)

    for o in MACROPHAGE_DEATH_OPTIONS:
        config_event.set(MacrophageDeath.__name__, o, 0.0)

    for o in INFECTED_MACROPHAGE_DEATH_OPTIONS:
        config_event.set(InfectedMacrophageDeathExternal.__name__, o, 0.0)

    for o in MACROPHAGE_PHAGOCYTOSIS_DESTROY_OPTIONS:
        config_event.set(PhagocytosisDestroy.__name__, o, 0.0)
    for o in MACROPHAGE_PHAGOCYTOSIS_RETAIN_OPTIONS:
        config_event.set(PhagocytosisRetain.__name__, o, 0.0)

    for o in MACROPHAGE_RECRUITMENT_OPTIONS:
        config_event.set(MacrophageRecruitmentLung.__name__, o, 0.0)
        config_event.set(MacrophageRecruitmentLymph.__name__, o, 0.0)

    for o in MACROPHAGE_TRANSLOCATION_OPTIONS:
        config_event.set(MacrophageTranslocateLung.__name__, o, 0.0)
        config_event.set(MacrophageTranslocateLymph.__name__, o, 0.0)
        config_event.set(MacrophageTranslocateBlood.__name__, o, 0.0)

    for o in T_CELL_ACTIVATION_OPTIONS:
        config_event.set(TCellActivationByExternal.__name__, o, 0.0)

    for o in T_CELL_DEATH_OPTIONS:
        config_event.set(TCellDeath.__name__, o, 0.0)

    for o in T_CELL_RECRUITMENT_OPTIONS:
        config_event.set(TCellRecruitmentLymph.__name__, o, 0.0)

    for o in T_CELL_TRANSLOCATION_OPTIONS:
        config_event.set(TCellTranslocationBlood.__name__, o, 0.0)

    # Write to file and close
    config_event.write(config_event_file)
    config_event_file.close()
