#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network.Patch import Patch

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class LungPatch(Patch):
    def __init__(self, node_id, compartments):
        Patch.__init__(self, node_id, compartments)
        # TODO - spatial attributes