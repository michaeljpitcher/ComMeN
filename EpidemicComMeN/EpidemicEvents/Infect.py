#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events import Change

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Infect(Change):
    """
    Infection event. Member of an infectious class comes into contact with member of a susceptible class, causing the
    susceptible member to move into an infected class.
    N.B. Infectious and infected classes may be different (e.g. latency).
    """
    def __init__(self, reaction_parameter, nodes, susceptible_compartment, infected_compartment,
                 infectious_compartments, population_density_dependent=True):
        """
        Create a new infection event
        :param reaction_parameter: Rate at which event occurs
        :param nodes: Nodes where event occurs
        :param susceptible_compartment: The class the member to be infected comes from
        :param infected_compartment: The class the susceptible member will move into
        :param infectious_compartments: List of all infectious compartments who transmit disease for this event
        :param population_density_dependent: Does this event depend on the population density?
        """
        self._population_density_dependent = population_density_dependent
        Change.__init__(self, reaction_parameter, nodes, susceptible_compartment, infected_compartment,
                        infectious_compartments)

    def _calculate_state_variable_at_node(self, node):
        """
        Determine state variable from a node. Count of susceptible compartment * (sum of infectious compartments).
        Then divided by total population if contact is population density dependent.
        :param node: Node to calculate
        :return: State variable calculated from the node
        """
        # Defer to Change class to calculate susceptible compartment * (sum of infectious compartments)
        state_variable = Change._calculate_state_variable_at_node(self, node)
        if self._population_density_dependent:
            total_pop = node.total_population()
            # If the total population is zero, must be no chance (needed for initial setup of network)
            if not total_pop:
                return 0
            else:
                # Divide by the total population at node
                state_variable = state_variable / node.total_population()
        return state_variable
