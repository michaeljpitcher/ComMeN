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


from BronchopulmonarySegments import *


class BronchopulmonarySegmentMetapopulationNetwork(MetapopulationNetwork):

    def __init__(self, segments, ventilation, perfusion, connections, compartments):

        nodes = {}
        for segment in segments:
            assert segment in RIGHT_BPS or segment in LEFT_BPS, "Invalid bronchopulmonary segment: {0}".format(segment)
            nodes[segment] = LungPatch(segment, compartments, perfusion[segment], ventilation[segment])

        edges = []
        for (segment1, segment2) in connections:
            patch1 = nodes[segment1]
            patch2 = nodes[segment2]
            edges.append(Edge(patch1, patch2))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)