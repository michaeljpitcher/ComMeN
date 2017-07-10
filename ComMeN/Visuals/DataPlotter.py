#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv
import matplotlib.pyplot as plt

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def draw_single_population_graph(filename, compartments, show_total=False, title=None):
    csv_file = open(filename, 'r')
    csv_reader = csv.DictReader(csv_file)
    time = []
    data = {}
    for compartment in compartments:
        data[compartment] = []
    for row in csv_reader:
        time.append(float(row['timestep']))
        for compartment in compartments:
            data[compartment].append(float(row[compartment]))

    # Colours set to (sort of) mimic MATLAB
    fig, ax = plt.subplots()
    ax.set_color_cycle(['blue', 'orangered', 'goldenrod', 'purple', 'green', 'cyan'])

    for compartment in compartments:
        plt.plot(time, data[compartment])
    if show_total:
        total = []
        for n in range(0, len(time)):
            total.append(sum([data[compartment][n] for compartment in compartments]))
        plt.plot(time, total)
        plt.legend(compartments + ['total'])
    else:
        plt.legend(compartments)
    if title:
        plt.title(str(title))
    plt.show()
