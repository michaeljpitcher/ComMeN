#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Dynamics import *
from LungComMeN import *
from ..PTBEvents import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PTBDynamicsSimple(Dynamics):

    def __init__(self, network_config, event_config):

        compartments = [BACTERIUM_FAST]

        # --------------------------------------------------
        # Network
        # --------------------------------------------------
        for section in ['Ventilations', 'Perfusions']:
            assert section in network_config.sections(), "Section {0} missing from network config. Use " \
                                                         "create_network_config_file() to generate a correct " \
                                                         "configuration file".format(section)

        edge_joining = JOINING_NONE

        ventilations = {}
        for (bps_id, value) in network_config.items('Ventilations'):
            ventilations[bps_id] = float(value)
        perfusions = {}
        for (bps_id, value) in network_config.items('Perfusions'):
            perfusions[bps_id] = float(value)

        network = BronchopulmonarySegmentSingleLymphMetapopulationNetwork(compartments, ventilations, perfusions,
                                                                          edge_joining)

        # --------------------------------------------------
        # Events
        # --------------------------------------------------
        events = []

        # Bacteria replication
        rate = event_config.getfloat('Event_rates', 'Bacterium_replication_lung')
        events.append(BacteriaReplicationByOxygen(rate, network.lung_patches, BACTERIUM_FAST))
        rate = event_config.getfloat('Event_rates', 'Bacterium_replication_lymph')
        events.append(BacteriaReplication(rate, network.lymph_patches, BACTERIUM_FAST))

        Dynamics.__init__(self, network, events)
