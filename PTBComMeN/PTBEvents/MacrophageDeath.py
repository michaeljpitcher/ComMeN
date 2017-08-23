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


def get_macrophage_death_events(nodes, standard_death_rates, death_by_t_cell_rate, death_bursting_rate):
    events = []
    # Standard
    for m in ALL_MACROPHAGES:
        # TODO - what to do with intracell during natural death? Currently they die
        events.append(MacrophageDeath(standard_death_rates[m], nodes, m))
    # By T-cell
    events.append(MacrophageDeath(death_by_t_cell_rate, nodes, MACROPHAGE_INFECTED, [T_CELL_ACTIVATED]))
    # By bursting
    events.append(MacrophageDeath(death_bursting_rate, nodes, MACROPHAGE_INFECTED, [BACTERIUM_INTRACELLULAR], False))
    return events


class MacrophageDeath(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed, influencing_compartments=None,
                 destroy_bacteria=True):
        self._destroy_bacteria = destroy_bacteria
        Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed, influencing_compartments)

    def _update_node(self, node):
        changes = {self._compartment_destroyed: -1}
        if self._compartment_destroyed == MACROPHAGE_INFECTED:
            bacteria_inside = int(round(node[self._compartment_destroyed] * 1.0 / node[BACTERIUM_INTRACELLULAR]))
            changes[BACTERIUM_INTRACELLULAR] = -1 * bacteria_inside
            if not self._destroy_bacteria:
                changes[BACTERIUM_SLOW] = bacteria_inside
        node.update(changes)
