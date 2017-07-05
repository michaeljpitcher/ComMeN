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
    def __init__(self, reaction_parameter, nodes, susceptible_compartment, infected_compartment,
                 infectious_compartments, population_density_dependent=True):
        self._population_density_dependent = population_density_dependent
        Change.__init__(self, reaction_parameter, nodes, susceptible_compartment, infected_compartment,
                        infectious_compartments)

    def _calculate_state_variable_at_node(self, node):
        state_variable = Change._calculate_state_variable_at_node(self, node)
        if self._population_density_dependent:
            total_pop = node.total_population()
            if not total_pop:
                return 0
            else:
                state_variable = state_variable / node.total_population()
        return state_variable
