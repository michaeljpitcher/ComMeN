#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN import *
from EpidemicComMeN.EpidemicDynamics.EpidemicCompartments import MATERNALLY_IMMUNE, SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED, MSEIR_compartments
from ..EpidemicEvents.Infect import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MSEIRSinglePatchDynamics(Dynamics):
    """
    MSEIR (Maternally Immune-Susceptible-Exposed-Infectious-Recovered dynamics occurring across a single homogeneously
    mixed population. Members are born into either S (from maternal S) or M (from maternal M,E,I or R), M changes to S
    as immunity wears off, contact between S and I turns S into E, E progresses to I, I recovers to R. Death occurs
    naturally at all compartments and increased death occurs due to disease at I.
    """

    def __init__(self, birth_rate, immunity_waning_rate, infection_rate, progression_rate, recovery_rate, death_rate,
                 death_by_infection_rate, seeding):
        """
        Create new MSEIR single patch model
        :param birth_rate: rate at which members are born into S (population dependent)
        :param immunity_waning_rate: rate at which M members transfer to S
        :param infection_rate: rate at which I members infect S (population density dependent) and turn S to E
        :param progression_rate: rate at which E members turn to I
        :param recovery_rate: rate at which I members turn to R
        :param death_rate: Rate at which all compartments die
        :param death_by_infection_rate: Rate at which I dies (extra to natural death)
        :param seeding: Initial seeding of patch
        """
        # Single patch network
        network = SinglePatchMetapopulation(MSEIR_compartments, seeding)
        # Create events
        events = []
        # Birth - into susceptible class
        events.append(Create(birth_rate, network.nodes, compartment_created=SUSCEPTIBLE,
                             influencing_compartments=[SUSCEPTIBLE]))
        # Birth - into maternally immune class
        events.append(Create(birth_rate, network.nodes, compartment_created=MATERNALLY_IMMUNE,
                             influencing_compartments=[MATERNALLY_IMMUNE,EXPOSED,INFECTIOUS,RECOVERED]))
        # Immunity waning - Maternally Immune become Susceptible
        events.append(Change(immunity_waning_rate, network.nodes, compartment_from=MATERNALLY_IMMUNE,
                             compartment_to=SUSCEPTIBLE))
        # Infection - Infectious change Susceptible to Exposed
        events.append(Infect(infection_rate, network.nodes, susceptible_compartment=SUSCEPTIBLE,
                             infected_compartment=EXPOSED, infectious_compartments=[INFECTIOUS],
                             population_density_dependent=True))
        # Progression - Exposed becomes Infectious
        events.append(Change(progression_rate, network.nodes, compartment_from=EXPOSED, compartment_to=INFECTIOUS))
        # Recover - Infectious changes to Recovered
        events.append(Change(recovery_rate, network.nodes, compartment_from=INFECTIOUS, compartment_to=RECOVERED))
        # Death (standard) - death event for every compartment
        for c in MSEIR_compartments:
            events.append(Destroy(death_rate, network.nodes, compartment_destroyed=c))
        # Death (by disease) - increased mortality for disease
        events.append(Destroy(death_by_infection_rate, network.nodes, compartment_destroyed=INFECTIOUS))

        Dynamics.__init__(self, network, events)

    def _end_simulation(self):
        """
        End the simulation if the infection has been eliminated from the system
        :return: True if no exposed or infectious members, false otherwise
        """
        return self._network.nodes[0][EXPOSED] == 0 and self._network.nodes[0][INFECTIOUS] == 0
