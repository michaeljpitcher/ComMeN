#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# imports

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

# Bronchopulmonary lung segments, grouped by lobe
APICAL_RIGHT = 'apical_right'
POSTERIOR_RIGHT = 'posterior_right'
ANTERIOR_RIGHT = 'anterior_right'
RIGHT_SUPERIOR = [APICAL_RIGHT, POSTERIOR_RIGHT, ANTERIOR_RIGHT]

LATERAL_RIGHT = 'lateral_right'
MEDIAL_RIGHT = 'medial_right'
RIGHT_MIDDLE = [LATERAL_RIGHT, MEDIAL_RIGHT]

SUPERIOR_RIGHT = 'superior_right'
MEDIAL_BASAL_RIGHT = 'medial_basal_right'
ANTERIOR_BASAL_RIGHT = 'anterior_basal_right'
LATERAL_BASAL_RIGHT = 'lateral_basal_right'
POSTERIOR_BASAL_RIGHT = 'posteior_basal_right'
RIGHT_INFERIOR = [SUPERIOR_RIGHT, MEDIAL_BASAL_RIGHT, ANTERIOR_BASAL_RIGHT, LATERAL_BASAL_RIGHT, POSTERIOR_BASAL_RIGHT]

RIGHT_BPS = RIGHT_SUPERIOR + RIGHT_MIDDLE + RIGHT_INFERIOR

INFERIOR_LINGULAR_LEFT = 'inferior_lingular_left'
SUPERIOR_LIGULAR_LEFT = 'superior_lingular_left'
LEFT_LINGULA = [INFERIOR_LINGULAR_LEFT, SUPERIOR_LIGULAR_LEFT]

APICOPOSTERIOR_LEFT = 'apicoposterior_left'
ANTERIOR_LEFT = 'anterior_left'
LEFT_SUPERIOR = [APICOPOSTERIOR_LEFT, ANTERIOR_LEFT] + LEFT_LINGULA

SUPERIOR_LEFT = 'superior_left'
ANTEROMEDIAL_LEFT = 'anteromedial_left'
POSTERIOR_BASAL_LEFT = 'posterior_basal_left'
LATERAL_BASAL_LEFT = 'lateral_basal_left'
LEFT_INFERIOR = [SUPERIOR_LEFT, ANTEROMEDIAL_LEFT, POSTERIOR_BASAL_LEFT, LATERAL_BASAL_LEFT]

LEFT_BPS = LEFT_SUPERIOR + LEFT_INFERIOR

ALL_BPS = RIGHT_BPS + LEFT_BPS

LOBES = [RIGHT_SUPERIOR, RIGHT_MIDDLE, RIGHT_INFERIOR, LEFT_SUPERIOR, LEFT_INFERIOR]

LYMPH = 'lymph'
