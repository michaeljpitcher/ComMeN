#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN import *
from ComMeN import *
from ..PulmonaryTBCompartments import *
from ..PTBEvents import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PTBDynamics(Dynamics):

    def __init__(self, ventilations, perfusions, edge_joining, event_parameters):

        compartments = ALL_BACTERIA + ALL_MACROPHAGES + ALL_T_CELLS

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
            # Between Lung Patches
            events.append(LungTranslocateWeight(event_parameters[state + "_translocate_lung"], network.lung_patches,
                                                state))
            # Lung to Lymph
            events.append(LymphTranslocateDrainage(event_parameters[state + "_translocate_lymph"],
                                                   network.lung_patches, state))
            # Lymph to Lung (blood)
            events.append(BloodTranslocatePerfusion(event_parameters[state + "_translocate_blood"],
                                                    network.lung_patches, state))

        # Macrophage recruitment
        # In lung, standard
        events.append(RecruitmentByPerfusion(event_parameters["macrophage_recruitment_lung_standard"],
                                             network.lung_patches, MACROPHAGE_REGULAR))

        # In lymph, standard
        events.append(Create(event_parameters['macrophage_recruitment_lymph_standard'], network.lymph_patches,
                             MACROPHAGE_REGULAR))

        for influencer in [MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED]:
            # In lung
            events.append(RecruitmentByPerfusion(event_parameters["macrophage_recruitment_lung_" + influencer],
                                             network.lung_patches, MACROPHAGE_REGULAR, [influencer]))
            # In lymph
            events.append(Create(event_parameters['macrophage_recruitment_lymph_' + influencer], network.lymph_patches,
                             MACROPHAGE_REGULAR, [influencer]))

        for state in ALL_MACROPHAGES:
            # Macrophage translocate to lymph
            events.append(LymphTranslocateDrainage(event_parameters[state + '_translocate_lymph'], network.lung_patches,
                                                   state))
            # Macrophage death (standard)
            events.append(Destroy(event_parameters[state + '_death_standard'], network.nodes, state))

        # Macrophage bursting
        # TODO - use Bacteria intracellular and capacity to determine
        events.append(Destroy(event_parameters['infected_macrophage_bursting'], network.nodes, MACROPHAGE_INFECTED,
                              [BACTERIUM_INTRACELLULAR]))

        # TODO - one type of t-cell
        # T Cell destroys macrophage
        events.append(Destroy(event_parameters['infected_macrophage_bursting'], network.nodes, MACROPHAGE_INFECTED,
                              [T_CELL_ACTIVATED]))

        # T Cell activates macrophage
        events.append(Change(event_parameters['regular_macrophage_activated_by_t_cell'], network.nodes,
                             MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [T_CELL_ACTIVATED]))

        # Cytokine activates macrophage
        # TODO - cytokine modelling
        events.append(Change(event_parameters['regular_macrophage_activated_by_t_cell'], network.nodes,
                             MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, [MACROPHAGE_INFECTED]))

        # Phagocytosis
        for b in EXTRACELLULAR_BACTERIA:
            # Regular destroys bacteria
            events.append(Destroy(event_parameters[MACROPHAGE_REGULAR + '_destroys_' + b], network.nodes, b,
                                  [MACROPHAGE_REGULAR]))
            # Regular retains bacteria, becomes infected
            events.append(PhagocytosisInfect(event_parameters[MACROPHAGE_REGULAR + "_infected_by_" + b], network.nodes,
                                             MACROPHAGE_REGULAR, b))
            # Infected retains bacteria
            events.append(PhagocytosisInfect(event_parameters[MACROPHAGE_INFECTED + "_infected_by_" + b], network.nodes,
                                             MACROPHAGE_INFECTED, b))
            # Activated destroys bacteria
            events.append(Destroy(event_parameters[MACROPHAGE_ACTIVATED + '_destroys_' + b], network.nodes, b,
                                  [MACROPHAGE_ACTIVATED]))

        # Immature dendritic recruitment standard
        events.append(RecruitmentByPerfusion(event_parameters[DENDRITIC_IMMATURE + '_recruitment_lung_standard'],
                                             network.lung_patches, DENDRITIC_IMMATURE))
        # Immature dendritic recruitment by bacteria
        events.append(RecruitmentByPerfusion(event_parameters[DENDRITIC_IMMATURE + '_recruitment_lung_bacteria'],
                                             network.lung_patches, EXTRACELLULAR_BACTERIA))

        # Dendritic cell death
        for d in ALL_DENDRITIC_CELLS:
            events.append(Destroy(event_parameters[d + '_death_standard'], network.nodes, d))

        # Dendritic translocation
        events

        # T-cell recruitment
        # TODO - clarify the t-cell recruitment/priming process
        events.append(Create(event_parameters[T_CELL_NAIVE + '_recruitment_rate'], network.lymph_patches, T_CELL_NAIVE))

        # T-cell priming
        # TODO - clarify which cells prime (i.e. are antigen-presenting)
        events.append(Change(event_parameters[T_CELL_NAIVE + '_priming_rate'], network.nodes,
                             T_CELL_NAIVE, T_CELL_ACTIVATED, [MACROPHAGE_INFECTED]))

        # T-cell death
        for t in ALL_T_CELLS:
            events.append(Destroy(event_parameters[t + '_death_rate'], network.nodes, t))

        # T-cell translocate
        events.append(BloodTranslocatePerfusion(event_parameters[T_CELL_ACTIVATED + '_blood_translocation_rate'],
                                                    network.lymph_patches, T_CELL_ACTIVATED))
        # T-cell cloning
        # TODO - maybe only occurs at lymph patches?
        events.append(Create(event_parameters[T_CELL_ACTIVATED + '_cloning_rate'], network.nodes, T_CELL_ACTIVATED,
                             [T_CELL_ACTIVATED]))

        Dynamics.__init__(self, network, events)
