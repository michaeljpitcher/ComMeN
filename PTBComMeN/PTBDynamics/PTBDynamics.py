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

RATE = 'rate'

MACROPHAGE_ATTRIBUTES = 'MacrophageAttributes'
MACROPHAGE_CARRYING_CAPACITY = 'macrophage_internal_carrying_capacity'
BACTERIAL_ATTRIBUTES = 'BacterialAttributes'
INTRACELLULAR_BACTERIUM_HILL_EXPONENT = 'intracellular_bacterium_hill_exponent'

EVENT_CONFIGURATION_SECTIONS = [MACROPHAGE_ATTRIBUTES, BACTERIAL_ATTRIBUTES, BacteriaChangeByOxygen.__name__,
                                ExtracellularBacteriaReplication.__name__, IntracellularBacteriaReplication.__name__,
                                BacteriaTranslocateLung.__name__, BacteriaTranslocateLymph.__name__,
                                BacteriaTranslocateBlood.__name__, MacrophageActivation.__name__,
                                MacrophageDeactivation.__name__,
                                MacrophageDeathStandard.__name__, InfectedMacrophageDeathByTCell.__name__,
                                InfectedMacrophageBursts.__name__,
                                RegularMacrophageDestroysBacteria.__name__,
                                ActivatedMacrophageDestroysBacteria.__name__,
                                MacrophageBecomesInfected.__name__,
                                MacrophageRecruitmentLungStandard.__name__, MacrophageRecruitmentLungEnhanced.__name__,
                                MacrophageRecruitmentLymphStandard.__name__,
                                MacrophageRecruitmentLymphEnhanced.__name__,
                                InfectedMacrophageTranslocateLymph.__name__,
                                TCellDifferentiationByInfectedMacrophages.__name__,
                                TCellDeath.__name__, TCellRecruitmentStandard.__name__,
                                TCellTranslocationBlood.__name__]


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

        if network_config.has_section(LYMPH_DRAINAGE):
            lymph_drainage_values = {}
            for node_id, value in network_config.items(LYMPH_DRAINAGE):
                lymph_drainage_values[node_id] = float(value)

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

        # Compartment attributes (used in multiple events)
        carrying_capacity = event_config.getfloat(MACROPHAGE_ATTRIBUTES, MACROPHAGE_CARRYING_CAPACITY)
        hill_exponent = event_config.getfloat(BACTERIAL_ATTRIBUTES, INTRACELLULAR_BACTERIUM_HILL_EXPONENT)

        # Bacteria change state
        rates = get_rates(BacteriaChangeByOxygen.__name__, event_config)
        events += get_bacteria_change_events(network.lung_patches, rates)

        # Bacteria replicate
        ext_rates = get_rates(ExtracellularBacteriaReplication.__name__, event_config)
        int_rate = event_config.getfloat(IntracellularBacteriaReplication.__name__, RATE)
        events += get_bacteria_replication_events(network.nodes, ext_rates, int_rate, carrying_capacity, hill_exponent)

        # Bacteria translocate
        lung_rates = get_rates(BacteriaTranslocateLung.__name__, event_config)
        lymph_rates = get_rates(BacteriaTranslocateLymph.__name__, event_config)
        blood_rates = get_rates(BacteriaTranslocateBlood.__name__, event_config)
        events += get_bacteria_translocation_events(network.lung_patches, network.lymph_patches, lung_rates,
                                                    lymph_rates, blood_rates)

        # Macrophage activation
        mac_act_rate = event_config.getfloat(MacrophageActivation.__name__, RATE)
        mac_act_half_sat = event_config.getfloat(MacrophageActivation.__name__, HALF_SAT)
        events += get_macrophage_activation_events(network.nodes, mac_act_rate, mac_act_half_sat)

        # Macrophage deactivation
        mac_deact_rate = event_config.getfloat(MacrophageDeactivation.__name__, RATE)
        mac_deact_half_sat = event_config.getfloat(MacrophageDeactivation.__name__, HALF_SAT)
        events += get_macrophage_deactivation_events(network.nodes, mac_deact_rate, mac_deact_half_sat)

        # Macrophage death
        standard_rates = get_rates(MacrophageDeathStandard.__name__, event_config)
        events += get_macrophage_standard_death_events(network.nodes, standard_rates)

        # Macrophage death by T-cell
        t_cell_kill_macrophage_rate = event_config.getfloat(InfectedMacrophageDeathByTCell.__name__, RATE)
        t_cell_kill_half_sat = event_config.getfloat(InfectedMacrophageDeathByTCell.__name__, HALF_SAT)
        events += get_macrophage_death_by_t_cell_events(network.nodes, t_cell_kill_macrophage_rate, t_cell_kill_half_sat)

        # Macrophage burst
        bursting_rate = event_config.getfloat(InfectedMacrophageBursts.__name__, RATE)
        events += get_macrophage_bursting_events(network.nodes, bursting_rate, carrying_capacity, hill_exponent)

        # Macrophage destroys bacteria
        regular_destroy_rates = get_rates(RegularMacrophageDestroysBacteria.__name__, event_config)
        activated_destroy_rates = get_rates(ActivatedMacrophageDestroysBacteria.__name__, event_config)
        events += get_macrophage_destroy_bacteria_events(network.nodes, regular_destroy_rates, activated_destroy_rates)

        # Macrophage becomes infected
        mac_infection_rates = get_rates(MacrophageBecomesInfected.__name__, event_config)
        events += get_macrophage_becomes_infected_events(network.nodes, mac_infection_rates)

        # Macrophage recruitment
        lung_standard_rate = event_config.getfloat(MacrophageRecruitmentLungStandard.__name__, RATE)
        lung_enhanced_rates = get_rates(MacrophageRecruitmentLungEnhanced.__name__, event_config)
        lymph_standard_rate = event_config.getfloat(MacrophageRecruitmentLymphStandard.__name__, RATE)
        lymph_enhanced_rates = get_rates(MacrophageRecruitmentLymphEnhanced.__name__, event_config)
        events += get_macrophage_recruitment_events(network.lung_patches, network.lymph_patches, lung_standard_rate,
                                                    lung_enhanced_rates, lymph_standard_rate, lymph_enhanced_rates)

        # Macrophage translocation
        mac_translocate_rate = event_config.getfloat(InfectedMacrophageTranslocateLymph.__name__, RATE)
        events += get_macrophage_translocation_events(network.lung_patches, mac_translocate_rate)

        # T cell differentiation
        tcell_differentiation_rate = event_config.getfloat(TCellDifferentiationByInfectedMacrophages.__name__, RATE)
        events += get_t_cell_differentiation_events(network.nodes, tcell_differentiation_rate)

        # T cell death
        rates = get_rates(TCellDeath.__name__, event_config)
        events += get_t_cell_death_events(network.nodes, rates)

        # T cell recruitment
        standard_rate = event_config.getfloat(TCellRecruitmentStandard.__name__, RATE)
        infected_mac_rate = event_config.getfloat(TCellRecruitmentByInfectedMacrophage.__name__, RATE)
        events += get_t_cell_recruitment_events(network.lymph_patches, standard_rate, infected_mac_rate)

        # T cell translocation
        rates = get_rates(TCellTranslocationBlood.__name__, event_config)
        events += get_t_cell_translocation_events(network.lymph_patches, rates)

        Dynamics.__init__(self, network, events)
