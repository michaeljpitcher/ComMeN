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
    def __init__(self, compartments):
        """ Create a new patch

        :param compartments: list of compartments present in this patch
        """
        self.subpopulation = dict([(c, 0) for c in compartments])
        # Record of all nodes this patch neighbours (updated when an edge is added to a network)
        self.neighbours = dict()
        self.update_handler = None

    def update(self, compartment, alteration):
        """
        Change the value of the count of a compartment by an amount (new value cannot be negative)
        :param compartment: Compartment to be amended
        :param alteration: Amount to change count value by
        :return:
        """
        new_value = self.subpopulation[compartment] + alteration
        assert new_value >= 0, "New value cannot be negative"
        self.subpopulation[compartment] = new_value
        # If an update handler has been assigned, process the consequences of updating this patch
        if self.update_handler:
            self.update_handler.propagate_node_update(self)
