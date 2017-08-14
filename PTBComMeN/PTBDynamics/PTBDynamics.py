#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN import *
from ComMeN import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PTBDynamics(Dynamics):

    def __init__(self, ventilations, perfusions, edge_joining, event_parameters):

        compartments = ALL_BACTERIA + ALL_MACROPHAGES

        # ===========================================
        # Network
        for bps in ALL_BPS:
            assert bps in ventilations, "Missing ventilation value for {0}".format(bps)
            assert bps in perfusions, "Missing perfusion value for {0}".format(bps)

        network = BronchopulmonarySegmentSingleLymphMetapopulationNetwork(compartments, ventilations, perfusions,
                                                                          edge_joining)

        # ===========================================
        # Events
        events = []

        # Bacteria replication
        # TODO - intracellular may need constraining by capacity
        for state in ALL_BACTERIA:
            events.append(Create(event_parameters[state + '_replication_rate'], network.nodes, state, [state]))

        # Bacteria change
        # TODO - other means of bacteria state change
        events.append(ChangeByOxygen(event_parameters['bacterium_change_oxygen_fast_to_slow'], network.lung_patches,
                                     BACTERIUM_FAST, BACTERIUM_SLOW, True))
        events.append(ChangeByOxygen(event_parameters['bacterium_change_oxygen_slow_to_fast'], network.lung_patches,
                                     BACTERIUM_SLOW, BACTERIUM_FAST, False))

        # Bacteria translocate
        for state in EXTRACELLULAR_BACTERIA:
            # TODO - assumes fast/slow doesn't affect translocation
            # Between Lung Patches
            events.append(LungTranslocateWeight(event_parameters["bacteria_translocate_lung"], network.lung_patches,
                                                state))
            # Lung to Lymph
            events.append(LymphTranslocateDrainage(event_parameters["bacteria_translocate_lymph"], network.lung_patches,
                                                state))
            # Lymph to Lung (blood)
            events.append(BloodTranslocatePerfusion(event_parameters["bacteria_translocate_blood"],
                                                    network.lung_patches, state))

        # Macrophage recruitment
        # In lung, standard
        events.append(RecruitmentByPerfusion(event_parameters["macrophage_recruitment_lung_standard"],
                                             network.lung_patches, MACROPHAGE_REGULAR))
        # In lung, by chemokine
        # TODO - assumes equal chemokine by M_A and M_I
        events.append(RecruitmentByPerfusion(event_parameters["macrophage_recruitment_lung_chemokine"],
                                             network.lung_patches, MACROPHAGE_REGULAR,
                                             [MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED]))
        # In lymph, standard
        events.append(Create(event_parameters['macrophage_recruitment_lymph_standard'], network.lymph_patches,
                             MACROPHAGE_REGULAR))
        # In lymph, by chemokine
        # TODO - assumes equal chemokine by M_A and M_I
        events.append(Create(event_parameters['macrophage_recruitment_lymph_chemokine'], network.lymph_patches,
                             MACROPHAGE_REGULAR))

        for state in ALL_MACROPHAGES:
            # Macrophage translocate to lymph
            events.append(LymphTranslocateDrainage(event_parameters[state + '_translocate_lymph'], network.lung_patches,
                                                   state))
            # Macrophage death (standard)
            events.append(Destroy(event_parameters[state + 'death_standard'], network.nodes, state))

        # Macrophage bursting
        # TODO - use Bacteria intracellular and capacity to determine
        events.append(Destroy(event_parameters['infected_macrophage_bursting'], network.nodes, MACROPHAGE_INFECTED,
                              [BACTERIUM_INTRACELLULAR]))

        # T Cell destroys macrophage
        events.append(Destroy(event_parameters['infected_macrophage_bursting'], network.nodes, MACROPHAGE_INFECTED,
                              [T_CELL_CYTOTOXIC_ACTIVATED]))

        # T Cell activates macrophage
        events.append(Change(event_parameters['regular_macrophage_activated_by_t_cell'], network.nodes,
                             MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [T_CELL_HELPER_ACTIVATED]))

        # Cytokine activates macrophage
        # TODO - cytokine modelling
        events.append(Change(event_parameters['regular_macrophage_activated_by_t_cell'], network.nodes,
                             MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [MACROPHAGE_INFECTED]))

        Dynamics.__init__(self, network, events)
