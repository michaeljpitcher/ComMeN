#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import ConfigParser as cp

from ComMeN.Dynamics import *
from LungComMeN.LungNetwork import *
from PulmonaryTBComMeN.PulmonaryTBCompartments import *
from ..PulmonaryTBEvents import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModelBPSLymph(Dynamics):
    """
    Create a ComMeN model of a TB infection spreading over a set of lungs.
    """
    def __init__(self, config_filepath):
        """
        Create new model
        :param config_filepath: path to configuration file
        """

        config = cp.ConfigParser()
        config.read(config_filepath)

        compartments = BACTERIA + MACROPHAGES + T_CELLS
        # Compartments which give off cytokine
        cytokine_compartments = [MACROPHAGE_INFECTED]
        # Compartments which are antigen-presenting cells (for T-cell priming)
        apcs = [MACROPHAGE_INFECTED]

        # Configure spatial attributes
        ventilations = dict()
        perfusions = dict()
        try:
            for bps in ALL_BPS:
                ventilations[bps] = config.getfloat('Ventilations', bps)
                perfusions[bps] = config.getfloat('Perfusions', bps)
        except cp.NoSectionError as e:
            raise Exception("Configuration file error: {0}".format(e.message))

        edge_joining = config.get('Network', 'BPS_edge_joining')

        # Create a network
        network = BronchopulmonarySegmentSingleLymphMetapopulationNetwork(compartments, ventilations, perfusions,
                                                                          edge_joining)

        # --------------------------------------------
        # EVENTS
        events = []

        for compartment in BACTERIA:
            # Bacteria replication
            rate = config.getfloat("Events", compartment + "_replication_rate")
            events.append(BacteriaReplicate(rate, network.nodes, compartment))
        for compartment in [BACTERIUM_FAST, BACTERIUM_SLOW]:
            # Bacteria translocate
            rate = config.getfloat("Events", compartment + "_translocate_lung_rate")
            events.append(BacteriaTranslocateLung(rate, network.BPS_nodes, compartment))
            rate = config.getfloat("Events", compartment + "_translocate_to_lymph_rate")
            events.append(BacteriaTranslocateLungToLymph(rate, network.BPS_nodes, compartment))
            rate = config.getfloat("Events", compartment + "_translocate_from_lymph_rate")
            events.append(BacteriaTranslocateLymphToLung(rate, network.BPS_nodes, compartment))

        # Bacteria change state
        events.append(OxygenChangeFastToSlow(config.getfloat("Events", "change_oxygen_fast_to_slow_rate"),
                                             network.BPS_nodes))
        events.append(OxygenChangeSlowToFast(config.getfloat("Events", "change_oxygen_slow_to_fast_rate"),
                                             network.BPS_nodes))

        # Macrophage recruitment
        events.append(MacrophageRecruitmentPerfusionBased(config.getfloat("Events", "macrophage_recruitment_lung"),
                                            network.BPS_nodes))
        events.append(MacrophageRecruitmentByCytokinePerfusionBased(
            config.getfloat("Events", "macrophage_recruitment_lung_infection"), network.BPS_nodes,
            cytokine_compartments))
        events.append(MacrophageRecruitment(config.getfloat("Events", "macrophage_recruitment_lymph"),
                                            network.lymph_nodes))
        events.append(MacrophageRecruitmentByCytokine(config.getfloat("Events", "macrophage_recruitment_lymph_infection"),
                                            network.lymph_nodes, cytokine_compartments))
        # Macrophage death
        for m in MACROPHAGES:
            rate = config.getfloat("Events", m + "_natural_death_rate")
            events.append(MacrophageDeathNatural(rate, network.nodes, m))
        # Macrophage death infection
        events.append(MacrophageDeathInfection(config.getfloat("Events", "Macrophage_infection_death_rate"),
                                               network.nodes))
        # Macrophage translocation
        for compartment in MACROPHAGES:
            # Bacteria translocate
            rate = config.getfloat("Events", compartment + "_translocate_to_lymph_rate")
            events.append(MacrophageTranslocateLungToLymph(rate, network.BPS_nodes, compartment))
            rate = config.getfloat("Events", compartment + "_translocate_from_lymph_rate")
            events.append(MacrophageTranslocateLymphToLung(rate, network.BPS_nodes, compartment))

        # Macrophage activation
        events.append(MacrophageSpontaneousActivation(config.getfloat("Events", "Macrophage_spontaneous_activation"),
                                                      network.nodes))
        events.append(MacrophageActivationByExternals(config.getfloat("Events", "Macrophage_activation_by_t_cell"),
                                                      network.nodes, [T_CELL_HELPER_ACTIVATED]))
        events.append(MacrophageActivationByExternals(config.getfloat("Events", "Macrophage_activation_by_cytokine"),
                                                      network.nodes, cytokine_compartments))

        # Phagocytosis
        # TODO - assumes fast/slow affects chance of survival after ingestion by regular only
        for bacteria in [BACTERIUM_FAST, BACTERIUM_SLOW]:
            # Regular macrophage
            chance_of_bacteria_survival = config.getfloat("Events", bacteria + "_survive_phagocytosis_regular_macrophage")
            rate_of_phagocytosis = config.getfloat("Events", "regular_macrophage_ingest_bacteria")
            events.append(Phagocytosis((1 - chance_of_bacteria_survival) * rate_of_phagocytosis, network.nodes,
                                       MACROPHAGE_REGULAR, bacteria))
            events.append(PhagocytosisInternalise(chance_of_bacteria_survival * rate_of_phagocytosis, network.nodes,
                                                  MACROPHAGE_REGULAR, bacteria, MACROPHAGE_INFECTED))
            # Infected macrophage
            rate_of_phagocytosis = config.getfloat("Events", "infected_macrophage_ingest_bacteria")
            events.append(PhagocytosisInternalise(rate_of_phagocytosis, network.nodes, MACROPHAGE_INFECTED, bacteria))

            # Activated macrophage
            rate_of_phagocytosis = config.getfloat("Events", "activated_macrophage_ingest_bacteria")
            events.append(Phagocytosis(rate_of_phagocytosis, network.nodes, MACROPHAGE_ACTIVATED, bacteria))

        # Naive T-cell recruitment
        for state in [T_CELL_HELPER_NAIVE, T_CELL_CYTOTOXIC_NAIVE]:
            rate = config.getfloat("Events", state + "_recruitment_rate")
            events.append(TCellRecruitment(rate, network.lymph_nodes, state))

        # T-cell death
        for state in T_CELLS:
            rate = config.getfloat("Events", state + "_death_rate")
            events.append(TCellDeath(rate, network.nodes, state))

        # T-cell activation
        for (naive, activated) in [(T_CELL_HELPER_NAIVE, T_CELL_HELPER_ACTIVATED),
                                   (T_CELL_CYTOTOXIC_NAIVE, T_CELL_CYTOTOXIC_ACTIVATED)]:
            rate = config.getfloat("Events", naive + "_activation_by_apc_rate")
            events.append(TCellActivation(rate, network.lymph_nodes, naive, activated, apcs))

        for state in [T_CELL_CYTOTOXIC_ACTIVATED, T_CELL_HELPER_ACTIVATED]:
            # T-cell cloning
            rate = config.getfloat("Events", state + "_cloning_rate")
            events.append(TCellCloning(rate, network.nodes, state))
            # T-cell translocation
            rate = config.getfloat("Events", state + "_translocation_from_lymph_rate")
            events.append(TCellTranslocateLymphToLung(rate, network.lymph_nodes, state))

        # T-cell destroy macrophage
        events.append(TCellDestroysMacrophageDestroyInternals(
            config.getfloat("Events", "t_cell_destroy_macrophage_destroy_rate"), network.nodes))
        events.append(TCellDestroysMacrophageReleaseInternals(
            config.getfloat("Events", "t_cell_destroy_macrophage_release_rate"), network.nodes))

        Dynamics.__init__(self, network, events)
