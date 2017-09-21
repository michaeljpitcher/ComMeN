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

MACROPHAGE_DEATH_OPTIONS = ALL_MACROPHAGES
INFECTED_MACROPHAGE_DEATH_OPTIONS = [T_CELL_ACTIVATED, BACTERIUM_INTRACELLULAR]


def get_macrophage_death_events(nodes, standard_rates, infected_mac_rates):
    events = []
    # Standard
    for m in ALL_MACROPHAGES:
        # TODO - assumes natural death of infected macrophage kills all internal bacteria
        events.append(MacrophageDeath(standard_rates[m], nodes, m))
    # By T-cell
    events.append(InfectedMacrophageDeathExternal(infected_mac_rates[T_CELL_ACTIVATED], nodes, T_CELL_ACTIVATED))
    # By bursting
    events.append(InfectedMacrophageDeathExternal(infected_mac_rates[BACTERIUM_INTRACELLULAR], nodes,
                                                  BACTERIUM_INTRACELLULAR, False))
    return events


class MacrophageDeath(Destroy):
    def __init__(self, reaction_parameter, nodes, compartment_destroyed, influencing_compartment=None,
                 destroy_bacteria=True):
        self._destroy_bacteria = destroy_bacteria
        if influencing_compartment:
            Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed, [influencing_compartment])
        else:
            Destroy.__init__(self, reaction_parameter, nodes, compartment_destroyed)

    def _update_node(self, node):
        changes = {self._compartment_destroyed: -1}
        if self._compartment_destroyed == MACROPHAGE_INFECTED:
            bacteria_inside = int(round(float(node[BACTERIUM_INTRACELLULAR]) / node[self._compartment_destroyed]))
            changes[BACTERIUM_INTRACELLULAR] = -1 * bacteria_inside
            if not self._destroy_bacteria:
                changes[BACTERIUM_SLOW] = bacteria_inside
        node.update(changes)


class InfectedMacrophageDeathExternal(MacrophageDeath):
    def __init__(self, reaction_parameter, nodes, influencing_compartment, destroy_bacteria=True):
        MacrophageDeath.__init__(self, reaction_parameter, nodes, MACROPHAGE_INFECTED, influencing_compartment,
                                 destroy_bacteria)
