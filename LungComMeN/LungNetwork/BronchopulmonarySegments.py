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
RIGHT_APICAL = 'right_apical'
RIGHT_POSTERIOR = 'right_posterior'
RIGHT_ANTERIOR = 'right_anterior'
RIGHT_SUPERIOR_LOBE = [RIGHT_APICAL, RIGHT_POSTERIOR, RIGHT_ANTERIOR]

RIGHT_LATERAL = 'right_lateral'
RIGHT_MEDIAL = 'right_medial'
RIGHT_MIDDLE_LOBE = [RIGHT_LATERAL, RIGHT_MEDIAL]

RIGHT_SUPERIOR = 'right_superior'
RIGHT_MEDIAL_BASAL = 'right_medial_basal'
RIGHT_ANTERIOR_BASAL = 'right_anterior_basal'
RIGHT_LATERAL_BASAL = 'right_lateral_basal'
RIGHT_POSTERIOR_BASAL = 'right_posterior_basal'
RIGHT_INFERIOR_LOBE = [RIGHT_SUPERIOR, RIGHT_MEDIAL_BASAL, RIGHT_ANTERIOR_BASAL, RIGHT_LATERAL_BASAL, RIGHT_POSTERIOR_BASAL]

RIGHT_LUNG = RIGHT_SUPERIOR_LOBE + RIGHT_MIDDLE_LOBE + RIGHT_INFERIOR_LOBE

LEFT_INFERIOR_LINGULAR = 'left_inferior_lingular'
LEFT_SUPERIOR_LIGULAR = 'left_superior_lingular'
LEFT_LINGULA = [LEFT_INFERIOR_LINGULAR, LEFT_SUPERIOR_LIGULAR]

LEFT_APICOPOSTERIOR = 'left_apicoposterior'
LEFT_ANTERIOR = 'left_anterior'
LEFT_SUPERIOR_LOBE = [LEFT_APICOPOSTERIOR, LEFT_ANTERIOR] + LEFT_LINGULA

LEFT_SUPERIOR = 'left_superior'
LEFT_ANTEROMEDIAL = 'left_anteromedial'
LEFT_POSTERIOR_BASAL = 'left_posterior_basal'
LEFT_LATERAL_BASAL = 'left_lateral_basal'
LEFT_INFERIOR_LOBE = [LEFT_SUPERIOR, LEFT_ANTEROMEDIAL, LEFT_POSTERIOR_BASAL, LEFT_LATERAL_BASAL]

LEFT_LUNG = LEFT_SUPERIOR_LOBE + LEFT_INFERIOR_LOBE

LUNG_BPS = RIGHT_LUNG + LEFT_LUNG

LOBES = [RIGHT_SUPERIOR_LOBE, RIGHT_MIDDLE_LOBE, RIGHT_INFERIOR_LOBE, LEFT_SUPERIOR_LOBE, LEFT_INFERIOR_LOBE]

LYMPH = 'lymph'
