#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Create import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class BacteriaReplicate(Create):
    """
    Bacterium replicates
    """
    def __init__(self, reaction_parameter, nodes, compartment):
        Create.__init__(self, reaction_parameter, nodes, compartment, [compartment])
