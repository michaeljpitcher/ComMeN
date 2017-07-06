#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network import *
from LungComMeN.LungNetwork.LungPatch import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


APICAL_RIGHT = 'apical_right'
POSTERIOR_RIGHT = 'posterior_right'
ANTERIOR_RIGHT = 'anterior_right'
LATERAL_RIGHT = 'lateral_right'
MEDIAL_RIGHT = 'medial_right'
SUPERIOR_RIGHT = 'superior_right'
MEDIAL_BASAL_RIGHT = 'medial_basal_right'
ANTERIOR_BASAL_RIGHT = 'anterior_basal_right'
LATERAL_BASAL_RIGHT = 'lateral_basal_right'
POSTERIOR_BASAL_RIGHT = 'posteior_basal_right'

RIGHT_BPS = [APICAL_RIGHT, POSTERIOR_RIGHT, ANTERIOR_RIGHT, LATERAL_RIGHT, MEDIAL_RIGHT, SUPERIOR_RIGHT,
             MEDIAL_BASAL_RIGHT, ANTERIOR_BASAL_RIGHT, LATERAL_BASAL_RIGHT, POSTERIOR_BASAL_RIGHT]

APICOPOSTERIOR_LEFT = 'apicoposterior_left'
ANTERIOR_LEFT = 'anterior_left'
INFERIOR_LINGULAR_LEFT = 'inferior_lingular_left'
SUPERIOR_LIGULAR_LEFT = 'superior_lingular_left'
SUPERIOR_LEFT = 'superior_left'
ANTEROMEDIAL_LEFT = 'anteromedial_left'
POSTERIOR_BASAL_LEFT = 'posterior_basal_left'
LATERAL_BASAL_LEFT = 'lateral_basal_left'

LEFT_BPS = [APICOPOSTERIOR_LEFT, ANTERIOR_LEFT, INFERIOR_LINGULAR_LEFT, SUPERIOR_LIGULAR_LEFT, SUPERIOR_LEFT,
            ANTEROMEDIAL_LEFT, POSTERIOR_BASAL_LEFT, LATERAL_BASAL_LEFT]


class BronchopulmonarySegmentMetapopulationNetwork(MetapopulationNetwork):

    def __init__(self, segments, ventilation, perfusion, connections, compartments, seeding):

        nodes = {}
        for segment in segments:
            assert segment in RIGHT_BPS or segment in LEFT_BPS, "Invalid bronchopulmonary segment: {0}".format(segment)
            nodes[segment] = LungPatch(segment, compartments, perfusion[segment], ventilation[segment])

        edges = []
        for (segment1, segment2) in connections:
            patch1 = nodes[segment1]
            patch2 = nodes[segment2]
            edges.append(Edge(patch1, patch2))

        MetapopulationNetwork.__init__(self, nodes.values(), edges, seeding)