#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ..LungNetwork.Lobe.LungLobes import *
from ..LungNetwork.BPS.BronchopulmonarySegments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


LOBE_POSITIONS_RIGHT = {SUPERIOR_RIGHT: (3, 10), MIDDLE_RIGHT: (2, 5), INFERIOR_RIGHT: (3.5, 1)}
LOBE_POSITIONS_ALL = {SUPERIOR_RIGHT: (3, 10),MIDDLE_RIGHT: (2, 5), INFERIOR_RIGHT: (3.5, 1), SUPERIOR_LEFT: (7, 10),
                      INFERIOR_LEFT: (7, 2)}

BPS_POSITIONS_ALL = {APICAL_RIGHT: (0, 10), POSTERIOR_RIGHT: (0, 8), ANTERIOR_RIGHT: (3, 10),
                     LATERAL_RIGHT: (0, 6), MEDIAL_RIGHT: (0, 4),
                     SUPERIOR_RIGHT: (0, 0), MEDIAL_BASAL_RIGHT: (0, 2), ANTERIOR_BASAL_RIGHT: (3, 0),
                     LATERAL_BASAL_RIGHT: (3, 2), POSTERIOR_BASAL_RIGHT: (1.5, 3),
                     INFERIOR_LINGULAR_LEFT: (7, 8), SUPERIOR_LIGULAR_LEFT: (7, 10),
                     APICOPOSTERIOR_LEFT: (10, 10), ANTERIOR_LEFT: (10, 8),
                     SUPERIOR_LEFT: (10, 0), ANTEROMEDIAL_LEFT: (7, 0), POSTERIOR_BASAL_LEFT: (10, 2),
                     LATERAL_BASAL_LEFT: (7, 2),
                     LYMPH: (5, 5)}