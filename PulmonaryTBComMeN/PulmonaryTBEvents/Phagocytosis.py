#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ComMeN.Events.Destroy import *
from ..PulmonaryTBCompartments import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Phagocytosis(Destroy):
    def __init__(self, reaction_parameter, nodes, phagocyte_compartment, bacterial_compartment):
        self._phagocyte_compartment = phagocyte_compartment
        Destroy.__init__(self, reaction_parameter, nodes, bacterial_compartment, [phagocyte_compartment])


class PhagocytosisInternalise(Phagocytosis):
    def __init__(self, reaction_parameter, nodes, phagocyte_compartment, bacterial_compartment,
                 phagocyte_infected_compartment=None):
        self._internalised_compartment = BACTERIUM_INTRACELLULAR
        self._phagocyte_infected_compartment = phagocyte_infected_compartment
        Phagocytosis.__init__(self, reaction_parameter, nodes, phagocyte_compartment, bacterial_compartment)

    def _update_node(self, node):
        changes = {self._compartment_destroyed: -1, self._internalised_compartment: 1}
        if self._phagocyte_infected_compartment:
            changes[self._phagocyte_compartment] = -1
            changes[self._phagocyte_infected_compartment] = 1
        node.update(changes)
