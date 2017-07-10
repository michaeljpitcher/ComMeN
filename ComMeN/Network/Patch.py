#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Patch:
    """
    The basic node of the ComMeN network. Contains a subpopulation of compartments, which interact via the
    events of the system.
    """
    def __init__(self, node_id, compartments):
        """ Create a new patch

        :param node_id: Unique identifier of patch
        :param compartments: list of compartments present in this patch
        """
        self.compartments = compartments
        self.node_id = node_id
        self._subpopulation = dict([(c, 0) for c in self.compartments])
        # Record of all nodes this patch neighbours (updated when an edge is added to a network)
        self.adjacent_edges = dict()
        self.update_handler = None

    def __getitem__(self, item):
        """
        Shortcut function to retrieve a patch subpopulation compartment via the get item function.
        e.g. use patch[compartment] to return count of compartment in subpopulation of patch instance
        :param item: Compartment of subpopulation
        :return:
        """
        return self._subpopulation[item]

    def __str__(self):
        return self.__class__.__name__ + ":" + str(self.node_id)

    def update(self, changes):
        """
        Change the value of the count of a compartment by an amount (new value cannot be negative)
        :param changes: Dictionary of changes; key=compartment, value=amount to update
        :return:
        """
        for compartment in changes:
            alteration = changes[compartment]
            new_value = self._subpopulation[compartment] + alteration
            assert new_value >= 0, "New value cannot be negative"
            self._subpopulation[compartment] = new_value
        # If an update handler has been assigned, process the consequences of updating this patch
        if self.update_handler:
            self.update_handler.propagate_node_update(self)

    def add_adjacent_edge(self, edge):
        """
        Add an edge to the list of adjacent edges
        :param edge:
        :return:
        """
        if edge.__class__ not in self.adjacent_edges:
            self.adjacent_edges[edge.__class__] = [edge]
        else:
            self.adjacent_edges[edge.__class__].append(edge)

    def total_population(self):
        """
        The total population at this node
        :return:
        """
        # Sum of counts in subpopulation for each compartment
        return sum(self._subpopulation.values())