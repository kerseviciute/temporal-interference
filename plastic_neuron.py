import pandas as pd
from abstract_neuron import AbstractNeuron
from neuron import h
import random
from abc import ABC, abstractmethod
from neuron_utils import NeuronUtils
import numpy as np
from copy import deepcopy
from synapse import Synapse


class PlasticNeuron(AbstractNeuron, ABC):
    """
        Simple Neuron with AMPA and NMDA synapses.
    """

    def __init__(
            self,
            n_synapses = 10,
            # TODO: allow specifying a list of connection weights
            # TODO: allow specifying a list of initial connection weights
            connection_weight = 0.0002,
            initial_weight = 0.0001,
            min_distance = 100,
            max_distance = 300,
            seed = 42,
            synapse_info = None
    ):
        self.n_synapses = n_synapses
        self.connection_weight = connection_weight
        self.initial_weight = initial_weight
        self.min_distance = min_distance
        self.max_distance = max_distance

        self.synapses = []

        self.seed = seed

        self.synapse_info = synapse_info
        if self.synapse_info is not None:
            self.n_synapses = len(self.synapse_info)

        self.output = None

        super().__init__()

    def __generate_synapses(self):
        """
        Generates and inserts new synapses at random locations.

        :return: None
        """
        random.seed(self.seed)

        print(f"Inserting {self.n_synapses} synapses")

        n_apical_dendrites = NeuronUtils.count_section("apical_dendrite")

        synapse_info = []
        for synapse in range(self.n_synapses):
            dendrite_idx, dendrite_loc, distance = NeuronUtils.generate_synapse_location(
                n_apical_dendrites = n_apical_dendrites,
                max_distance = self.max_distance,
                min_distance = self.min_distance
            )

            delay = random.uniform(0, 100)

            self.__insert_synapse(dendrite_idx, dendrite_loc, delay)

            synapse_info.append(pd.DataFrame({
                "Dendrite": [dendrite_idx],
                "Location": [dendrite_loc],
                "Distance": [distance],
                "Delay": [delay]
            }))

        self.synapse_info = pd.concat(synapse_info, ignore_index = True)

    def __insert_synapse(self, dendrite_idx, dendrite_loc, delay):
        """
        Inserts a synapse at the specified location.

        :param dendrite_idx: dendrite id
        :param dendrite_loc: location along the dendrite
        :param delay: delay of stimulus
        :return: None
        """
        # TODO: create the stimulus elsewhere?
        stimulus = NeuronUtils.create_burst_stimulus()

        synapse = Synapse(
            dendrite_idx = dendrite_idx,
            dendrite_loc = dendrite_loc,
            stimulus = stimulus,
            delay = delay,
            max_weight = self.connection_weight,
            initial_weight = self.initial_weight
        )

        self.synapses.append(synapse)

    def __read_synapses(self):
        """
        Reads synapse information and inserts them.

        :return: None
        """
        print(f"Inserting {len(self.synapse_info)} synapses")

        for _, synapse in self.synapse_info.iterrows():
            dendrite_idx = int(synapse.Dendrite)
            dendrite_loc = synapse.Location
            delay = synapse.Delay

            self.__insert_synapse(dendrite_idx, dendrite_loc, delay)

    def initialize(self):
        if self.synapse_info is not None:
            print("Reading synapse information")
            self.__read_synapses()
        else:
            print("Generating synapse information")
            self.__generate_synapses()

    def run(self, duration = 100):
        # Setup experimental conditions
        NeuronUtils.set_stimulus(
            delay = 0,
            duration = 0,
            frequency1 = 0,
            frequency2 = 0,
            amplitude = 0,
            phase = 0
        )

        # Set up recording of all the variables of interest
        soma = h.Vector().record(h.soma[0](0.5)._ref_v)
        t = h.Vector().record(h._ref_t)

        # Run the experiment
        h.tstop = duration
        h.run()

        # Save the results
        # TODO: do it the same way as with the synapses?
        self.output = pd.DataFrame({
            "Time": t,
            "Soma": soma
        })
