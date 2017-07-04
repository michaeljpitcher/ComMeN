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
    def __init__(self, reaction_parameter, nodes, compartment_translocating, edge_class=None,
                 rate_increases_with_edges=True):
        """
        New translocate event. If rate_increases_with_edges, then the rate of the event increases the more edges there
        are at node. If false, then rate is only dependent on their being one edge.
        :param reaction_parameter: Reaction parameter of event
        :param nodes: Nodes where creation occurs
        :param compartment_translocating: The compartment of the member translocating
        :param edge_class: Class of edge which this event occurs along
        :param rate_increases_with_edges: Does the rate increase the more viable edges there are at node?
        """
        self._compartment_translocating = compartment_translocating
        self._rate_increases_with_edges = rate_increases_with_edges
        self._edge_class = edge_class
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
        # If rate increases with edges, state variable is * by number of viable edges, else it is state variable * 1 if
        # any edge exists, and * 0 if no edge exists
        if self._rate_increases_with_edges:
            return state_variable * len(viable_edges)
        else:
            return state_variable * (len(viable_edges) >= 1)

    def _viable_edges(self, node):
        """
        Return the neighbours which are acceptable for this event. If class has been specified, then will restrict to
        only edges matching that class (if edge is directed, will not appear in node's adjacent edges)
        :param node:
        :return: Acceptable edges for this event object
        """
        # TODO - can this be stored in the event so it's not computed every time?
        if self._edge_class:
            if self._edge_class in node.adjacent_edges.keys():
                edges_correct_class = node.adjacent_edges[self._edge_class]
            else:
                return []
        else:
            edges_correct_class = [j for i in node.adjacent_edges.values() for j in i]

        viable_edges = []
        for e in edges_correct_class:
            if (e.directed and e.nodes[0] == node) or not e.directed:
                viable_edges.append(e)
        return viable_edges

    def _update_node(self, node):
        """
        Update the node by removing a member from one compartment and adding a member into another compartment
        :param node: Node to update
        """
        # Get all acceptable edges
        viable_edges = self._viable_edges(node)
        chosen_edge = self._pick_edge(viable_edges)
        node.update({self._compartment_translocating: -1})
        neighbour = chosen_edge[node]
        neighbour.update({self._compartment_translocating: 1})

    def _pick_edge(self, edges):
        """
        Choose an edge. Default is to pick an edge at random, can be overridden in subclasses to look at specific
        attributes of the edges
        :param edges: List of viable edge objects
        :return: Chosen edge
        """
        return rand.choice(edges)
