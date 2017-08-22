#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import Event
import numpy.random as rand

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Translocate(Event):
    """
    Translocate event - a member of one compartment moves from one node to another
    """
    def __init__(self, reaction_parameter, nodes, compartment_translocating, edge_class,
                 rate_increases_with_edges=True, influencing_compartments=None):
        """
        New translocate event. If rate_increases_with_edges, then the rate of the event increases the more edges there
        are at node. If false, then rate is only dependent on their being one edge.
        :param reaction_parameter: Reaction parameter of event
        :param nodes: Nodes where translocation occurs
        :param compartment_translocating: The compartment of the member translocating
        :param edge_class: Class of edge which this event occurs along
        :param rate_increases_with_edges: Does the rate increase the more viable edges there are at node?
        :param influencing_compartments: External compartments which cause translocation
        """
        self._compartment_translocating = compartment_translocating
        self._rate_increases_with_edges = rate_increases_with_edges
        self._edge_class = edge_class
        self._influencing_compartments = influencing_compartments
        Event.__init__(self, reaction_parameter, nodes)

    def _calculate_state_variable_at_node(self, node):
        """
        The amount this node provides to the state variable. Calculated as amount of viable edges (if necessary) *
        count of translocating compartment
        :param node: Node to calculate
        :return:
        """
        # Get all acceptable edges
        viable_edges = self._viable_edges(node)
        # State variable depends on count of compartment
        state_variable = node[self._compartment_translocating]
        if state_variable == 0:
            return state_variable
        # If rate increases with edges, state variable is * by number of viable edges, else it is state variable * 1 if
        # any edge exists, and * 0 if no edge exists
        if self._rate_increases_with_edges:
            state_variable = state_variable * len(viable_edges)
        else:
            state_variable = state_variable * (len(viable_edges) >= 1)

        if self._influencing_compartments:
            state_variable = state_variable * sum([node[compartment] for compartment in self._influencing_compartments])

        return state_variable

    def _viable_edges(self, node):
        """
        Return the neighbours which are acceptable for this event. If class has been specified, then will restrict to
        only edges matching that class (if edge is directed, will not appear in node's adjacent edges)
        :param node:
        :return: Acceptable edges for this event object
        """
        # TODO - can this be stored in the event so it's not computed every time?
        if self._edge_class in node.adjacent_edges.keys():
            viable_edges = []
            for e in node.adjacent_edges[self._edge_class]:
                if (e.directed and e.nodes[0] == node) or not e.directed:
                    viable_edges.append(e)
            return viable_edges
        else:
            return []

    def _update_node(self, node):
        """
        Update the node by removing a member from one compartment and adding a member into another compartment
        :param node: Node to update
        """
        # Get all acceptable edges
        viable_edges = self._viable_edges(node)
        # Choose an edge
        chosen_edge = self._pick_edge(viable_edges)
        # Remove member from the node
        node.update({self._compartment_translocating: -1})
        # Get neighbour from edge
        neighbour = chosen_edge[node]
        # Add member to the neighbour
        neighbour.update({self._compartment_translocating: 1})

    def _pick_edge(self, edges):
        """
        Choose an edge. Default is to pick an edge at random, can be overridden in subclasses to look at specific
        attributes of the edges
        :param edges: List of viable edge objects
        :return: Chosen edge
        """
        return rand.choice(edges)
