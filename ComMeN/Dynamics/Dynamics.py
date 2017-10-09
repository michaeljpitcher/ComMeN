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
    Dynamics handles the simulation of events over a metapopulation network.

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
        # Only interested in events that can actually occur
        events = [e for e in events if e.reaction_parameter > 0]
        # Create update handler. Doing so attaches handler to every node (that has an event attached)
        update_handler = UpdateHandler(events)
        self.network = network
        self._events = events
        self._time = 0.0
        self.compartments = []
        for node in self.network.nodes:
            self.compartments += node.compartments
        # Remove any duplicates
        self.compartments = list(set(self.compartments))

    def run(self, time_limit, seeding, run_id, timestep_for_data_record=1):
        """
        Run the simulation, performing events upon the network, until time limit is reached or no event can occur.
        :param time_limit: Maximum simulation time to run dynamics until - will terminate once this is exceeded
        :param seeding: Initial state of the network. Dict: key=node_id, value=updates as dict: key=compartment,
                        value=amount to start
        :param output_data: Should data be written to a CSV file
        :param run_id: Identifier for this simulation. Will be used for CSV filename if supplied
        :return:
        """
        print "ComMeN Simulation"

        # Seed the network with initial subpopulation counts
        self.network.seed(seeding)

        data = []
        self._record_data(data, 0)
        counter = timestep_for_data_record

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

            # Update time
            self._time += tau

            # Record data. Use the timestep interval to record - use while loop in case multiple intervals have been
            # passed
            while self._time > counter:
                self._record_data(data, counter)
                counter = counter + timestep_for_data_record
                self._timestep_print()

            for e in self._events:
                running_total += e.rate
                if running_total >= r2:
                    e.perform()
                    break



        # Write data
        csv_file = open(str(run_id) + '.csv', 'w')
        csv_writer = csv.DictWriter(csv_file, [TIMESTEP, NODE_ID] + self.compartments)
        csv_writer.writeheader()
        for row in data:
            csv_writer.writerow(row)

    def _end_simulation(self):
        """
        Function to determine if simulation should be ended. Can be overridden by sub-classes to end when a certain
        limit reached (e.g. if infection dies out)
        :return: Boolean - if true, simulation ends
        """
        return False

    def _record_data(self, data, counter):
        """
        Write the current state of the network nodes to a csv file. One row = one patch at the current time
        :param csv_writer: CSV writer object (DictWriter)
        """
        # Loop through all nodes
        for node in self.network.nodes:
            row = {TIMESTEP: counter, NODE_ID: node.node_id}
            for c in node.compartments:
                row[c] = node[c]
            data.append(row)
        return data

    def _timestep_print(self):
        """
        Output to the console every timestep
        """
        print "t = ", self._time
