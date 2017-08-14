#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


BACTERIUM_FAST = 'bacteria_fast'
BACTERIUM_SLOW = 'bacteria_slow'
BACTERIUM_INTRACELLULAR = 'bacteria_intracellular'
EXTRACELLULAR_BACTERIA = [BACTERIUM_FAST, BACTERIUM_SLOW]
ALL_BACTERIA = [BACTERIUM_FAST, BACTERIUM_SLOW, BACTERIUM_INTRACELLULAR]

MACROPHAGE_REGULAR = 'macrophage_regular'
MACROPHAGE_ACTIVATED = 'macrophage_activated'
MACROPHAGE_INFECTED = 'macrophage_infected'
ALL_MACROPHAGES = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED]

T_CELL_HELPER_NAIVE = 't_cell_helper_naive'
T_CELL_CYTOTOXIC_NAIVE = 't_cell_cytotoxic_naive'
T_CELL_HELPER_ACTIVATED = 't_cell_helper_activated'
T_CELL_CYTOTOXIC_ACTIVATED = 't_cell_cytotoxic_activated'
ALL_T_CELLS = [T_CELL_HELPER_NAIVE, T_CELL_CYTOTOXIC_NAIVE, T_CELL_HELPER_ACTIVATED, T_CELL_CYTOTOXIC_ACTIVATED]

# DENDRITIC_IMMATURE = 'dendritic_immature'
# DENDRITIC_MATURE = 'dendritic_mature'
# DENDRITIC_CELLS = [DENDRITIC_IMMATURE, DENDRITIC_MATURE]
