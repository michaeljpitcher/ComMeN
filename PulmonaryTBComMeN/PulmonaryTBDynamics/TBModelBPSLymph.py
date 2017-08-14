#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import ConfigParser as cp

from LungComMeN import *
from PulmonaryTBComMeN.PulmonaryTBCompartments import *


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

        # --------------------------------------------
        # COMPARTMENTS
        compartments = BACTERIA + MACROPHAGES + T_CELLS
        # Compartments which give off cytokine
        # TODO - assume one cytokine, given off equally by all compartments in this list
        cytokine_compartments = [MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED]
        # Compartments which are antigen-presenting cells (for T-cell priming)
        apcs = [MACROPHAGE_INFECTED]

        # --------------------------------------------
        # NETWORK
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
        event_parameters = {}

        for (parameter, value) in config.items('Event_parameters'):
            event_parameters[parameter] = float(value)

        # BACTERIA
        # Replication
        for state in [BACTERIUM_FAST, BACTERIUM_SLOW]:
            rate = event_parameters[state + '_replication_rate']
            # Create a new bacterium of state, based on current amount of bacteria of that state
            replication_event = Create(rate, network.nodes, state, [state])
            events.append(replication_event)
        # Intracellular replication
        # TODO - M&K04 - conservative growth based on capacity
        rate = event_parameters[BACTERIUM_INTRACELLULAR + '_replication_rate']
        # Create a new bacterium of state, based on current amount of bacteria of that state
        replication_event = Create(rate, network.nodes, BACTERIUM_INTRACELLULAR, [BACTERIUM_INTRACELLULAR])
        events.append(replication_event)

        # State change
        events.append(ChangeByOxygen(event_parameters['bacterium_change_by_oxygen_fast_to_slow'], network.lung_patches,
                                     BACTERIUM_FAST, BACTERIUM_SLOW, True))
        events.append(ChangeByOxygen(event_parameters['bacterium_change_by_oxygen_slow_to_fast'], network.lung_patches,
                                     BACTERIUM_SLOW, BACTERIUM_FAST, False))

        # Bacterium translocate

        # MACROPHAGE
        # Recruitment - standard, lung
        events.append(RecruitmentByPerfusion(event_parameters['macrophage_recruitment_lung_rate'], network.lung_patches,
                                             MACROPHAGE_REGULAR))
        # Recruitment - standard, lymph
        events.append(RecruitmentByPerfusion(event_parameters['macrophage_recruitment_lymph_rate'],
                                             network.lymph_patches, MACROPHAGE_REGULAR))


        Dynamics.__init__(self, network, events)
