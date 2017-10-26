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


BACTERIUM_EXTRACELLULAR_FAST = 'bacteria_extracellular_fast'
BACTERIUM_EXTRACELLULAR_SLOW = 'bacteria_extracellular_slow'
BACTERIUM_INTRACELLULAR_MACROPHAGE = 'bacteria_intracellular_macrophage'
BACTERIUM_INTRACELLULAR_DENDRITIC = 'bacteria_intracellular_dendritic_cell'
EXTRACELLULAR_BACTERIA = [BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW]
ALL_BACTERIA = [BACTERIUM_EXTRACELLULAR_FAST, BACTERIUM_EXTRACELLULAR_SLOW, BACTERIUM_INTRACELLULAR_MACROPHAGE, BACTERIUM_INTRACELLULAR_DENDRITIC]

MACROPHAGE_REGULAR = 'macrophage_regular'
MACROPHAGE_ACTIVATED = 'macrophage_activated'
MACROPHAGE_INFECTED = 'macrophage_infected'
ALL_MACROPHAGES = [MACROPHAGE_REGULAR, MACROPHAGE_ACTIVATED, MACROPHAGE_INFECTED]

DENDRITIC_CELL_IMMATURE = 'dendritic_cell_immature'
DENDRITIC_CELL_MATURE = 'dendritic_cell_mature'
ALL_DENDRITIC_CELLS = [DENDRITIC_CELL_IMMATURE, DENDRITIC_CELL_MATURE]

T_CELL_NAIVE = 't_cell_naive'
T_CELL_ACTIVATED = 't_cell_activated'
ALL_T_CELLS = [T_CELL_NAIVE, T_CELL_ACTIVATED]

ALL_TB_COMPARTMENTS = ALL_BACTERIA + ALL_MACROPHAGES + ALL_DENDRITIC_CELLS + ALL_T_CELLS
