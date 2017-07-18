#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network.Patch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LymphPatch(Patch):
    """
    Patch representing a region of the human lymphatic system
    """
    def __init__(self, node_id, compartments):
        """
        Create a new lymph patch
        :param node_id: Unique ID of patch
        :param compartments: Compartments in patch subpopulation
        """
        Patch.__init__(self, node_id, compartments)

    def __str__(self):
        return str(self.node_id)