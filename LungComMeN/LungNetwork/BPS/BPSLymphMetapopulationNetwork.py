#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Network import *
from ..LungPatch import *
from ..LymphPatch import *
from ..LungEdge import *
from ..LymphEdge import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

from BronchopulmonarySegments import *


class BronchopulmonarySegmentLymphMetapopulationNetwork(MetapopulationNetwork):

    def __init__(self, compartments, ventilation, perfusion):

        nodes = {}
        for segment in ALL_BPS:
            nodes[segment] = LungPatch(segment, compartments, perfusion[segment], ventilation[segment])

        nodes[LYMPH] = LymphPatch(LYMPH, compartments)

        # Edges
        edges = []
        for lobe in LOBES:
            for index in range(len(lobe)-1):
                segment_patch = nodes[lobe[index]]
                for index2 in range(index+1, len(lobe)):
                    segment_patch2 = nodes[lobe[index2]]
                    edges.append(LungEdge(segment_patch, segment_patch2, False, 1))

        for segment in ALL_BPS:
            edges.append(LymphEdge(nodes[LYMPH], nodes[segment], False, 1))

        MetapopulationNetwork.__init__(self, nodes.values(), edges)