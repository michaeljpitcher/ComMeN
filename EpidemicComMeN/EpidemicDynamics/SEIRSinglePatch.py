#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN import *
from ..EpidemicNetwork.SinglePatchNetwork import SinglePatchEpidemicNetwork
from ..Compartments import *
from ..EpidemicEvents.Infect import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SEIRSinglePatchDynamics(Dynamics):
    """
    SEIR (Susceptible-Exposed-Infectious-Recovered dynamics occurring across a single homogeneously mixed population.
    Members are born into S, contact between S and I turns S into E, E progresses to I, I recovers to R. Death occurs
    naturally at all compartments and increased death occurs due to disease at I.
    """

    def __init__(self, birth_rate, infection_rate, progression_rate, recovery_rate, death_rate, death_by_infection_rate,
                 seeding):
        """
        Create new SEIR single patch model
        :param birth_rate: rate at which members are born into S (population dependent)
        :param infection_rate: rate at which I members infect S (population density dependent) and turn S to E
        :param progression_rate: rate at which E members turn to I
        :param recovery_rate: rate at which I members turn to R
        :param death_rate: Rate at which all compartments die
        :param death_by_infection_rate: Rate at which I dies (extra to natural death)
        :param seeding: Initial seeding of patch
        """
        # Single patch network
        network = SinglePatchEpidemicNetwork(SEIR_compartments)
        # Create events
        events = []
        # Birth - into susceptible class
        events.append(Create(birth_rate, network.nodes, compartment_created=SUSCEPTIBLE,
                             influencing_compartments=SEIR_compartments))
        # Infection - Infectious change Susceptible to Exposed
        events.append(Infect(infection_rate, network.nodes, susceptible_compartment=SUSCEPTIBLE,
                             infected_compartment=EXPOSED, infectious_compartments=[INFECTIOUS],
                             population_density_dependent=True))
        # Progression - Exposed becomes Infectious
        events.append(Change(progression_rate, network.nodes, compartment_from=EXPOSED, compartment_to=INFECTIOUS))
        # Recover - Infectious changes to Recovered
        events.append(Change(recovery_rate, network.nodes, compartment_from=INFECTIOUS, compartment_to=RECOVERED))
        # Death (standard) - death event for every compartment
        for c in SEIR_compartments:
            events.append(Destroy(death_rate, network.nodes, compartment_destroyed=c))
        # Death (by disease) - increased mortality for disease
        events.append(Destroy(death_by_infection_rate, network.nodes, compartment_destroyed=INFECTIOUS))

        Dynamics.__init__(self, network, events, seeding)

    def _end_simulation(self):
        """
        End the simulation if the infection has been eliminated from the system
        :return: True if no exposed or infectious members, false otherwise
        """
        return self._network.nodes[0][EXPOSED] == 0 and self._network.nodes[0][INFECTIOUS] == 0
