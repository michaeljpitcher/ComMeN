#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from PTBComMeN.PTBDynamics import *
from PTBComMeN.PTBEvents import *
import ConfigParser

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


DEFAULT_EVENT_CONFIG_FILE = "PTBModel_Events.cfg"
DEFAULT_SEEDING_CONFIG_FILE = "PTBModel_Seeding.cfg"


def create_event_config_file(filename=DEFAULT_EVENT_CONFIG_FILE):
    config_event_file = open(filename, 'w')
    config_event = ConfigParser.ConfigParser(allow_no_value=True)
    for n in EVENT_CONFIG_SECTIONS:
        config_event.add_section(n)

    config_event.set(CELL_ATTRIBUTES, MACROPHAGE_CARRYING_CAPACITY, 0.0)
    config_event.set(CELL_ATTRIBUTES, DENDRITIC_CELL_CARRYING_CAPACITY, 0.0)
    config_event.set(CELL_ATTRIBUTES, INTRACELLULAR_BACTERIUM_MACROPHAGE_HILL_EXPONENT, 0.0)
    config_event.set(CELL_ATTRIBUTES, INTRACELLULAR_BACTERIUM_DENDRITIC_CELL_HILL_EXPONENT, 0.0)

    for o in EXTRACELLULAR_BACTERIA + [SIGMOID, HALF_SAT]:
        config_event.set(BacteriaChangeByOxygen.__name__, o, 0.0)

    for o in EXTRACELLULAR_BACTERIA:
        config_event.set(ExtracellularBacteriaReplication.__name__, o, 0.0)

    config_event.set(IntracellularBacteriaMacrophageReplication.__name__, RATE, 0.0)

    config_event.set(IntracellularBacteriaDendriticReplication.__name__, RATE, 0.0)

    for o in EXTRACELLULAR_BACTERIA:
        config_event.set(BacteriaTranslocateLung.__name__, o, 0.0)
        config_event.set(BacteriaTranslocateLymph.__name__, o, 0.0)
        config_event.set(BacteriaTranslocateBlood.__name__, o, 0.0)

    config_event.set(MacrophageActivation.__name__, RATE, 0.0)
    config_event.set(MacrophageActivation.__name__, HALF_SAT, 0.0)

    config_event.set(MacrophageDeactivation.__name__, RATE, 0.0)
    config_event.set(MacrophageDeactivation.__name__, HALF_SAT, 0.0)

    for o in ALL_MACROPHAGES:
        config_event.set(MacrophageDeathStandard.__name__, o, 0.0)

    config_event.set(InfectedMacrophageDeathByTCell.__name__, RATE, 0.0)
    config_event.set(InfectedMacrophageDeathByTCell.__name__, HALF_SAT, 0.0)

    config_event.set(InfectedMacrophageBursts.__name__, RATE, 0.0)

    for o in EXTRACELLULAR_BACTERIA:
        config_event.set(RegularMacrophageDestroysBacteria.__name__, o, 0.0)
        config_event.set(ActivatedMacrophageDestroysBacteria.__name__, o, 0.0)

    config_event.set(MacrophageBecomesInfected.__name__, RATE, 0.0)
    config_event.set(MacrophageBecomesInfected.__name__, HALF_SAT, 0.0)

    config_event.set(MacrophageRecruitmentLungStandard.__name__, RATE, 0.0)
    config_event.set(MacrophageRecruitmentLymphStandard.__name__, RATE, 0.0)

    for o in [MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED]:
        config_event.set(MacrophageRecruitmentLungEnhanced.__name__, o, 0.0)
        config_event.set(MacrophageRecruitmentLymphEnhanced.__name__, o, 0.0)

    config_event.set(InfectedMacrophageTranslocateLymph.__name__, RATE, 0.0)

    for o in ALL_T_CELLS:
        config_event.set(TCellDeath.__name__, o, 0.0)

    config_event.set(TCellRecruitmentStandard.__name__, RATE, 0.0)

    for o in [DENDRITIC_CELL_MATURE, MACROPHAGE_INFECTED]:
        config_event.set(TCellRecruitmentEnhanced.__name__, o, 0.0)
        config_event.set(TCellDifferentiationByAPC.__name__, o, 0.0)

    config_event.set(TCellTranslocationBlood.__name__, RATE, 0.0)

    config_event.set(DendriticCellRecruitmentLungStandard.__name__, RATE, 0.0)

    config_event.set(DendriticCellRecruitmentLungEnhancedByBacteria.__name__, RATE, 0.0)
    config_event.set(DendriticCellRecruitmentLungEnhancedByBacteria.__name__, HALF_SAT, 0.0)

    for o in ALL_DENDRITIC_CELLS:
        config_event.set(DendriticCellDeathStandard.__name__, o, 0.0)

    config_event.set(DendriticCellTranslocation.__name__, RATE, 0.0)

    # for o in [MACROPHAGE_INFECTED]:
    #     config_event.set(DendriticCellMaturationAntigen.__name__, o, 0.0)

    for o in EXTRACELLULAR_BACTERIA:
        config_event.set(DendriticCellMaturationBacteriaUptake.__name__, o, 0.0)

    # Write to file and close
    config_event.write(config_event_file)
    config_event_file.close()


def create_seeding_config_file(filename=DEFAULT_SEEDING_CONFIG_FILE):
    config_seeding_file = open(filename, 'w')
    config_seeding = ConfigParser.ConfigParser()
    for n in LUNG_BPS + [LYMPH]:
        config_seeding.add_section(n)
        for c in ALL_TB_COMPARTMENTS:
            config_seeding.set(n, c, 0)
    config_seeding.write(config_seeding_file)
    config_seeding_file.close()

if __name__ == '__main__':
    create_event_config_file()
    create_seeding_config_file()
