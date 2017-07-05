#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SinglePatchEpidemicNetwork(MetapopulationNetwork):
    """
    An epidemic taking place across a single homogeneously mixed population (i.e. a one-patch network)
    """
    def __init__(self, compartments):
        """
        Create a new network
        :param compartments: Compartments to add to nodes
        """
        # Just one node, no edges
        nodes = [Patch(0, compartments)]
        MetapopulationNetwork.__init__(self, nodes, [])
