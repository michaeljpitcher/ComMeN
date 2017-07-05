#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# imports

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class UpdateHandler:
    """
    Handles node updates - when a node updates, handler propagates that change by finding every event that happens
    at that node and updates their state variables. Prevents having to recalculate state variables for all events on
    every timestep.
    """
    def __init__(self, events):
        """
        Create a new event handler.
        :param events: List of all events
        """
        # Dependencies is a dictionary listing every event at a node
        self._node_dependencies = dict()

        for event in events:
            for node in event.state_variable_composition:
                # Attaches itself to the node (if no update handler already)
                if not node.update_handler:
                    node.update_handler = self
                # Add a record to the dictionary if one doesn't exist already
                if node not in self._node_dependencies:
                    self._node_dependencies[node] = []
                self._node_dependencies[node].append(event)

    def propagate_node_update(self, node):
        """
        Given a node, update the state variables of the events that occur at that node (as its subpopulation
        has been altered)
        :param node: The node whose subpopulation has been amended
        :return:
        """
        events = self._node_dependencies[node]
        for e in events:
            e.update_state_variable_from_node(node)
