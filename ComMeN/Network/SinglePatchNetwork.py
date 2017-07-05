#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from MetapopulationNetwork import MetapopulationNetwork
from Patch import Patch

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class SinglePatchMetapopulation(MetapopulationNetwork):
    """
    An epidemic taking place across a single homogeneously mixed population (i.e. a one-patch network)
    """
    def __init__(self, compartments, seeding=None):
        """
        Create a new network
        :param compartments: Compartments to add to node
        :param seeding: Seeding for the node
        """
        # Just one node, no edges
        nodes = [Patch(0, compartments)]
        if seeding:
            node_seeding = {0: seeding}
        else:
            node_seeding = None
        MetapopulationNetwork.__init__(self, nodes, seeding=node_seeding)
