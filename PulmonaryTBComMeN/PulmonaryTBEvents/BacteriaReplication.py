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


class BacteriaReplication(Create):
    def __init__(self, reaction_parameter, nodes, compartment_created):
        Create.__init__(self, reaction_parameter, nodes, compartment_created,
                        influencing_compartments=[compartment_created])
