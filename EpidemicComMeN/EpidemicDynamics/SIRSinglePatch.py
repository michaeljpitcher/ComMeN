#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN import *
from EpidemicComMeN.EpidemicCompartments import SUSCEPTIBLE, INFECTIOUS, RECOVERED, SIR_compartments
from ..EpidemicEvents.Infect import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SIRSinglePatchDynamics(Dynamics):
    """
    SIR (Susceptible-Infectious-Recovered dynamics occurring across a single homogeneously mixed population. Members
    are born into S, contact between S and I turns S into I, I recovers to R. Death occurs naturally at all compartments
    and increased death occurs due to disease at I.
    """

    def __init__(self, birth_rate, infection_rate, recovery_rate, death_rate, death_by_infection_rate,):
        """
        Create new SIR single patch model
        :param birth_rate: rate at which members are born into S (population dependent)
        :param infection_rate: rate at which I members infect S (population density dependent)
        :param recovery_rate: rate at which I member turn to R
        :param death_rate: Rate at which all compartments die
        :param death_by_infection_rate: Rate at which I dies (extra to natural death)
        """
        # Single patch network
        network = SinglePatchMetapopulation(SIR_compartments)
        # Create events
        events = []
        # Birth - into susceptible class
        events.append(Create(birth_rate, network.nodes, compartment_created=SUSCEPTIBLE,
                             influencing_compartments=SIR_compartments))
        # Infection - Infectious change Susceptible to Infectious
        events.append(Infect(infection_rate, network.nodes, susceptible_compartment=SUSCEPTIBLE,
                             infected_compartment=INFECTIOUS, infectious_compartments=[INFECTIOUS],
                             population_density_dependent=True))
        # Recover - Infectious changes to Recovered
        events.append(Change(recovery_rate, network.nodes, compartment_from=INFECTIOUS, compartment_to=RECOVERED))
        # Death (standard) - death event for every compartment
        for c in SIR_compartments:
            events.append(Destroy(death_rate, network.nodes, compartment_destroyed=c))
        # Death (by disease) - increased mortality for disease
        events.append(Destroy(death_by_infection_rate, network.nodes, compartment_destroyed=INFECTIOUS))

        Dynamics.__init__(self, network, events)

    def _end_simulation(self):
        """
        End the simulation if the infection has been eliminated from the system
        :return: True if no infectious members, false otherwise
        """
        return self._network.nodes[0][INFECTIOUS] == 0
