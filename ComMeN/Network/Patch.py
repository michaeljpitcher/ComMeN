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
        self.neighbours = dict()

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
