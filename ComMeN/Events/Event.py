#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import numpy.random as rand

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Event:
    """
    An event to be performed upon the metapopulation network, altering the subpopulation of a patch.

    Nomenclature adapted from ** D. T. Gillespie, "A general method for numerically simulating the stochastic time
    evolution of coupled chemical reactions," J. Comput. Phys., vol. 22, no. 4, pp. 403-434, 1976. **

    Reaction parameter - average probability to first order in unit time, that an event will occur accordingly in the
        next time interval unit time
    State variable - number of distinct reactant possible combinations for event, found to be present at time t.
    Rate - probability, to first order in unit time that an event will occur in the next time interval unit time
    """

    def __init__(self, reaction_parameter, nodes):
        """
        Create a new event
        :param reaction_parameter: Rate at which event occurs
        :param nodes: Nodes where event can occur
        """
        # Reaction rate of event
        self.rate = 0
        self.reaction_parameter = reaction_parameter

        #  Initialise the state variable, and the dictionary detailing its composition.
        self._state_variable = 0
        self.state_variable_composition = dict()
        # Write a record in the dictionary for every node where this event can happen, update with value from node.
        for n in nodes:
            self.state_variable_composition[n] = 0.0
            self.update_state_variable_from_node(n)

    def update_state_variable_from_node(self, node):
        """
        Given a node, update this events state variable and thus probability based on the current subpopulation of node
        :param node: Node to calculate state variable from
        """
        # Get new value
        value_after = self._calculate_state_variable_at_node(node)
        # Calculate change
        change = value_after - self.state_variable_composition[node]
        # No change, so quit
        if change == 0:
            # TODO - some means of update where we don't get this far if change will be zero (i.e. base updates on
            # compartments affected, not just nodes)
            return
        # Set new value
        self.state_variable_composition[node] = value_after
        # Alter the total state variable by the change of amount
        self._state_variable += change
        # Recalculate rate
        self.rate = self._state_variable * self.reaction_parameter

    def _calculate_state_variable_at_node(self, node):
        """
        Calculate the amount the given node contributes to the overall state variable. To be overriden in subclass, as
        specific to the event type.
        :param node: Node at which to calculate the contribution to event state variable
        :return: State variable from node
        """
        raise NotImplementedError()

    def perform(self):
        """
        Perform the event and update the network. Chooses a node probabilistically based on the contribution to the
        overall state variable, then updates it (and neighbours if needed)
        :return:
        """
        # Check their is some state variable composition
        if not self._state_variable:
            raise Exception("State variable for event is 0 - no instances where event can be performed")
        # Choose a node based on the contribution to total state variable
        r = rand.random() * self._state_variable
        running_total = 0
        # Loop through all nodes which contribute to this event, summing state variables. Once greater than r, choose
        # that node
        for node in self.state_variable_composition:
            running_total += self.state_variable_composition[node]
            if running_total >= r:
                # Update node, finish
                self._update_node(node)
                return

    def _update_node(self, node):
        """
        Update the subpopulation of the node. To be overriden in subclass, as specific to the event type.
        :param node: Node to be updated
        """
        raise NotImplementedError()
