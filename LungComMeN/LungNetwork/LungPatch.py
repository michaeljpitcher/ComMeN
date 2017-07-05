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


class LungPatch(Patch):
    """
    A region of the human lung. Spatial attributes include ventilation (air reaching this region of the lung),
    perfusion (blood reaching this region of the lung) and oxygen tension (ventilation / perfusion - amount of oxygen
    remaining after gas exchange)
    """
    def __init__(self, node_id, compartments, ventilation, perfusion):
        """
        Create a new lung patch
        :param node_id: Unique ID of patch
        :param compartments: Compartments in patch subpopulation
        :param ventilation: Value reflecting amount of air reaching patch
        :param perfusion: Value reflecting amount of blood reaching patch
        """
        self._ventilation = ventilation
        self._perfusion = perfusion
        # TODO - oxygen tension may be minus not divide in this instance
        self._oxygen_tension = ventilation / float(perfusion)
        Patch.__init__(self, node_id, compartments)
