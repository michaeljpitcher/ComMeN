#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import csv
import numpy as np

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def aggregate_data(location, ids):
    node_data = {}
    compartments = None
    timesteps = []

    for run_id in ids:
        if location:
            filename = location + '/' + str(run_id) + '.csv'
        else:
            filename = str(run_id) + '.csv'
        csv_file = open(filename, 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if not compartments:
                compartments = sorted(list(csv_reader.fieldnames))
                compartments.remove('node_id')
                compartments.remove('timestep')
            if row['node_id'] not in node_data:
                node_data[row['node_id']] = {}
            if row['timestep'] not in node_data[row['node_id']]:
                node_data[row['node_id']][row['timestep']] = {}
            if row['timestep'] not in timesteps:
                timesteps.append(row['timestep'])
            for c in compartments:
                if c not in node_data[row['node_id']][row['timestep']]:
                    node_data[row['node_id']][row['timestep']][c] = []
                node_data[row['node_id']][row['timestep']][c].append(float(row[c]))

    aggregated_node_data = {}

    for n in node_data:
        aggregated_node_data[n] = {}
        for t in node_data[n]:
            aggregated_node_data[n][t] = {}
            for c in node_data[n][t]:
                aggregated_node_data[n][t][c] = np.mean(node_data[n][t][c])

    if location:
        output_csv = open(location + '/aggregated.csv', 'wb')
    else:
        output_csv = open('aggregated.csv', 'wb')
    fieldnames = ['timestep', 'node_id'] + compartments
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()

    for t in timesteps:
        for n in aggregated_node_data:
            row = {'timestep': t, 'node_id': n}
            for c in aggregated_node_data[n][t]:
                row[c] = aggregated_node_data[n][t][c]
            writer.writerow(row)

    # for n in aggregated_node_data:
    #     timesteps = sorted(aggregated_node_data[n].keys())
    #     for t in timesteps:
    #         row = {'timestep': t, 'node_id': n}
    #         for c in aggregated_node_data[n][t]:
    #             row[c] = aggregated_node_data[n][t][c]
    #         writer.writerow(row)
