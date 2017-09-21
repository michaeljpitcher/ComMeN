#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network.Edge import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LymphEdge(Edge):

    def __init__(self, node_1, node_2, drainage):
        self.drainage = drainage
        Edge.__init__(self, node_1, node_2, directed=True)
