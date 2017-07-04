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
    def __init__(self, compartments):
        nodes = [Patch(1, compartments)]
        MetapopulationNetwork.__init__(self, nodes, [])
