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

SUSCEPTIBLE = 'susceptible'
EXPOSED = 'exposed'
INFECTIOUS = 'infectious'
RECOVERED = 'recovered'

SIR_compartments = [SUSCEPTIBLE, INFECTIOUS, RECOVERED]
SIS_compartments = [SUSCEPTIBLE, INFECTIOUS]
SEIR_compartments = [SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED]