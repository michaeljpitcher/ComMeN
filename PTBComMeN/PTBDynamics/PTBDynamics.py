#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN import *
from ..PTBEvents import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"




EVENT_CONFIGURATION_SECTIONS = [BacteriaChangeByOxygen.__name__, BacteriaReplication.__name__,
                                BacteriaTranslocateLung.__name__, BacteriaTranslocateLymph.__name__,
                                BacteriaTranslocateBlood.__name__, MacrophageActivationByExternal.__name__,
                                MacrophageDeath.__name__, InfectedMacrophageDeathExternal.__name__,
                                PhagocytosisDestroy.__name__, PhagocytosisRetain.__name__,
                                MacrophageRecruitmentLung.__name__, MacrophageRecruitmentLymph.__name__,
                                MacrophageTranslocateLung.__name__, MacrophageTranslocateLymph.__name__,
                                MacrophageTranslocateBlood.__name__, TCellActivationByExternal.__name__,
                                TCellDeath.__name__, TCellRecruitmentLymph.__name__, TCellTranslocationBlood.__name__]


def get_rates(event_classname, event_config):
    return dict([(k, float(v)) for (k, v) in event_config.items(event_classname)])


class PTBDynamics(Dynamics):

    def __init__(self, network_config, event_config):

        # --------------------------------------------------
        # Network
        # --------------------------------------------------
        for section in NETWORK_CONFIGURATION_SECTIONS:
            assert section in network_config.sections(), "Section {0} missing from network config. Use " \
                                                         "create_network_config_file() to generate a correct " \
                                                         "configuration file".format(section)

        edge_weight_within_lobe = network_config.get(NETWORK_CONFIGURATION_SECTIONS[0], EDGE_WEIGHT_WITHIN_LOBE)
        edge_weight_adjacent_lobe = network_config.get(NETWORK_CONFIGURATION_SECTIONS[0], EDGE_WEIGHT_BETWEEN_LOBE)

        ventilations = {}
        for (bps_id, value) in network_config.items(NETWORK_CONFIGURATION_SECTIONS[1]):
            ventilations[bps_id] = float(value)
        perfusions = {}
        for (bps_id, value) in network_config.items(NETWORK_CONFIGURATION_SECTIONS[2]):
            perfusions[bps_id] = float(value)

        # Lymphatic drainage
        lymph_drainage_values = None

        print network_config.sections()
        print LYMPH_DRAINAGE

        if network_config.has_section(LYMPH_DRAINAGE):
            print "YASS"
            lymph_drainage_values = dict(network_config.items(LYMPH_DRAINAGE))

        network = PulmonaryNetwork(ALL_TB_COMPARTMENTS, ventilations, perfusions, edge_weight_within_lobe,
                                   edge_weight_adjacent_lobe, lymph_drainage_values)

        # --------------------------------------------------
        # Events
        # --------------------------------------------------
        events = []
        for section in EVENT_CONFIGURATION_SECTIONS:
            assert section in event_config.sections(), "Section {0} missing from event config. Use " \
                                                       "create_event_config_file() to generate a correct " \
                                                       "configuration file".format(section)

        # Bacteria change state
        rates = get_rates(BacteriaChangeByOxygen.__name__, event_config)
        events += get_bacteria_change_events(network.lung_patches, rates)

        # Bacteria replicate
        rates = get_rates(BacteriaReplication.__name__, event_config)
        events += get_bacteria_replication_events(network.nodes, rates)

        # Bacteria translocate
        lung_rates = get_rates(BacteriaTranslocateLung.__name__, event_config)
        lymph_rates = get_rates(BacteriaTranslocateLymph.__name__, event_config)
        blood_rates = get_rates(BacteriaTranslocateBlood.__name__, event_config)
        events += get_bacteria_translocation_events(network.lung_patches, network.lymph_patches, lung_rates,
                                                    lymph_rates, blood_rates)

        # Macrophage activation
        rates = get_rates(MacrophageActivationByExternal.__name__, event_config)
        events += get_macrophage_activation_events(network.nodes, rates)

        # Macrophage death
        standard_rates = get_rates(MacrophageDeath.__name__, event_config)
        infected_rates = get_rates(InfectedMacrophageDeathExternal.__name__, event_config)
        events += get_macrophage_death_events(network.nodes, standard_rates, infected_rates)

        # Macrophage phagocytosis
        destroy_rates = get_rates(PhagocytosisDestroy.__name__, event_config)
        retain_rates = get_rates(PhagocytosisRetain.__name__, event_config)
        events += get_phagocytosis_events(network.nodes, destroy_rates, retain_rates)

        # Macrophage recruitment
        lung_rates = get_rates(MacrophageRecruitmentLung.__name__, event_config)
        lymph_rates = get_rates(MacrophageRecruitmentLymph.__name__, event_config)
        events += get_macrophage_recruitment_events(network.lung_patches, network.lymph_patches, lung_rates,
                                                    lymph_rates)

        # Macrophage translocation
        lung_rates = get_rates(MacrophageTranslocateLung.__name__, event_config)
        lymph_rates = get_rates(MacrophageTranslocateLymph.__name__, event_config)
        blood_rates = get_rates(MacrophageTranslocateLung.__name__, event_config)
        events += get_macrophage_translocation_events(network.lung_patches, network.lymph_patches, lung_rates,
                                                      lymph_rates, blood_rates)

        # T cell activation
        rates = get_rates(TCellActivationByExternal.__name__, event_config)
        events += get_t_cell_activation_events(network.nodes, rates)

        # T cell death
        rates = get_rates(TCellDeath.__name__, event_config)
        events += get_t_cell_death_events(network.nodes, rates)

        # T cell recruitment
        rates = get_rates(TCellRecruitmentLymph.__name__, event_config)
        events += get_t_cell_recruitment_events(network.lymph_patches, rates)

        # T cell translocation
        rates = get_rates(TCellTranslocationBlood.__name__, event_config)
        events += get_t_cell_translocation_events(network.lymph_patches, rates)

        Dynamics.__init__(self, network, events)
