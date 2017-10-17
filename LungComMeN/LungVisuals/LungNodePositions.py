#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from LungComMeN.LungNetwork.BronchopulmonarySegments import *


__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


BPS_POSITIONS_ALL = {RIGHT_APICAL: (0, 10), RIGHT_POSTERIOR: (0, 8), RIGHT_ANTERIOR: (3, 10),
                     RIGHT_LATERAL: (0, 6), RIGHT_MEDIAL: (0, 4),
                     RIGHT_SUPERIOR: (0, 0), RIGHT_MEDIAL_BASAL: (0, 2), RIGHT_ANTERIOR_BASAL: (3, 0),
                     RIGHT_LATERAL_BASAL: (3, 2), RIGHT_POSTERIOR_BASAL: (1.5, 3),
                     LEFT_INFERIOR_LINGULAR: (7, 8), LEFT_SUPERIOR_LIGULAR: (7, 10),
                     LEFT_APICOPOSTERIOR: (10, 10), LEFT_ANTERIOR: (10, 8),
                     LEFT_SUPERIOR: (10, 0), LEFT_ANTEROMEDIAL: (7, 0), LEFT_POSTERIOR_BASAL: (10, 2),
                     LEFT_LATERAL_BASAL: (7, 2),
                     LYMPH: (5, 5)}