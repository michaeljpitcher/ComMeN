#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBDynamics.PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageDeath(Destroy):
    def __init__(self, reaction_parameter, nodes, macrophage_compartment, influencing_compartments=None):
        Destroy.__init__(self, reaction_parameter, nodes, macrophage_compartment, influencing_compartments)

    def _update_node(self, node):
        changes = {self._compartment_destroyed: -1}
        if self._compartment_destroyed == MACROPHAGE_INFECTED:
            bacteria_to_distribute = int(round(float(node[BACTERIUM_INTRACELLULAR])/node[MACROPHAGE_INFECTED]))
            changes[BACTERIUM_INTRACELLULAR] = -1 * bacteria_to_distribute
            changes[BACTERIUM_SLOW] = bacteria_to_distribute
        node.update(changes)


class MacrophageDeathNatural(MacrophageDeath):
    def __init__(self, reaction_parameter, nodes, macrophage_compartment):
        MacrophageDeath.__init__(self, reaction_parameter, nodes, macrophage_compartment)


class MacrophageDeathInfection(MacrophageDeath):
    def __init__(self, reaction_parameter, nodes):
        MacrophageDeath.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, [BACTERIUM_INTRACELLULAR])
