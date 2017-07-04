#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN import *
from ..EpidemicNetwork.SinglePatchNetwork import SinglePatchEpidemicNetwork
from ..Compartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SIRSinglePatchDynamics(Dynamics):

    def __init__(self, birth_rate, infection_rate, recovery_rate, death_rate, death_by_infection_rate,
                 population_total, population_infected):
        network = SinglePatchEpidemicNetwork(SIR_compartments)

        # Events
        events = []
        # Birth - into susceptible class
        events.append(Create(birth_rate, network.nodes, compartment_created=SUSCEPTIBLE,
                             influencing_compartments=[SUSCEPTIBLE, INFECTIOUS, RECOVERED]))
        # Infection - Infectious change Susceptible to Infectious
        events.append(Change(infection_rate, network.nodes, compartment_from=SUSCEPTIBLE, compartment_to=INFECTIOUS,
                             influencing_compartments=INFECTIOUS))
        # Recover - Infectious changes to Recovered
        events.append(Change(recovery_rate, network.nodes, compartment_from=INFECTIOUS, compartment_to=RECOVERED))
        # Death (standard) - death event for every compartment
        for c in SIR_compartments:
            events.append(Destroy(death_rate, network.nodes, compartment_destroyed=c))
        # Death (by disease) - increased mortality for disease
        events.append(Destroy(death_by_infection_rate, network.nodes, compartment_destroyed=INFECTIOUS))

        Dynamics.__init__(self, network, events)

        # Seed the network
        network.nodes[0].update({SUSCEPTIBLE: population_total - population_infected})
        network.nodes[0].update({INFECTIOUS: population_infected})
