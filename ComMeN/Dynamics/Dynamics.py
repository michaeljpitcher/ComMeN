#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from UpdateHandler import UpdateHandler
from numpy import random as rand
import math
import csv
import time

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = ""
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

TIMESTEP = 'timestep'
NODE_ID = 'node_id'


class Dynamics:
    """
    Dynamics handles the simulation of events over a network.

    Simulations are run using the run function, which performs events using Gillespie algorithm, adapted from:
    D. T. Gillespie, "A general method for numerically simulating the stochastic time evolution of coupled chemical
    reactions," J. Comput. Phys., vol. 22, no. 4, pp. 403-434, 1976. **

    Each event calculates its rate, based on the assigned reaction parameter and the current state of the subpopulations
    of nodes in the network. Using these rates, a timestep interval is calculated and an event is probabilistically
    chosen. The event is performed and the network is updated. This continues until a time limit is reached or there are
    no events that can occur.
    """

    def __init__(self, network, events):
        """
        Create a new set of dynamics.
        :param network: The network upon which the events occur
        :param events: The events acting on the network
        """
        # Create update handler. Doing so attaches handler to every node (that has an event attached)
        update_handler = UpdateHandler(events)
        self._network = network
        self._events = events
        self._time = 0.0
        self._compartments = []
        for node in self._network.nodes:
            self._compartments += node.compartments
        # Remove any duplicates
        self._compartments = list(set(self._compartments))

    def run(self, time_limit, output_data=False, run_id=None):
        """
        Run the simulation, performing events upon the network, until time limit is reached or no event can occur.
        :param time_limit: Maximum simulation time to run dynamics until - will terminate once this is exceeded
        :param output_data: Should data be written to a CSV file
        :param run_id: Identifier for this simulation. Will be used for CSV filename if supplied
        :return:
        """
        print "ComMeN Simulation"
        csv_writer = None

        if output_data:
            if run_id:
                filename = str(run_id) + '.csv'
            else:
                current_time = [str(time.localtime()[n])+'_' for n in range(5)]
                current_time.append(str(time.localtime()[5]))
                filename = ''.join(current_time) + '.csv'
            csv_file = open(filename, 'w')

            csv_writer = csv.DictWriter(csv_file, [TIMESTEP, NODE_ID] + self._compartments)
            csv_writer.writeheader()
            print "Data output to:", filename

            self._record_data(csv_writer)

        self._timestep_print()

        # Run until time limit reached
        while self._time < time_limit:
            if self._end_simulation():
                print "Termination point reached - ending simulation"
                return
            # Calculate the total rate
            total_rate = sum([e.rate for e in self._events])
            # If rate is zero for all, end simulation
            if total_rate == 0:
                print "No possibility of any event occurring - ending simulation"
                return
            # Calculate the timestep tau based on the total rates
            r1 = rand.random()
            tau = (1.0 / total_rate) * math.log(1.0 / r1)
            # Choose which event has occurred
            r2 = rand.random() * total_rate
            running_total = 0.0
            for e in self._events:
                running_total += e.rate
                if running_total >= r2:
                    e.perform()
                    break
            # Update time
            self._time += tau
            if output_data:
                self._record_data(csv_writer)
            self._timestep_print()

    def _end_simulation(self):
        """
        Function to determine if simulation should be ended. Can be overridden by sub-classes to end when a certain
        limit reached (e.g. if infection dies out)
        :return: Boolean - if true, simulation ends
        """
        return False

    def _record_data(self, csv_writer):
        """
        Write the current state of the network nodes to a csv file. One row = one patch at the current time
        :param csv_writer: CSV writer object (DictWriter)
        :return:
        """
        # Loop through all nodes
        for node in self._network.nodes:
            row = {TIMESTEP: self._time, NODE_ID: node.node_id}
            for c in node.compartments:
                row[c] = node[c]
            csv_writer.writerow(row)

    def _timestep_print(self):
        """
        Output to the console every timestep
        :return:
        """
        print "t = ", self._time
