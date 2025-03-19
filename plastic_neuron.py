import pandas as pd
from abstract_neuron import AbstractNeuron
from neuron import h
import random
from abc import ABC, abstractmethod
from neuron_utils import NeuronUtils


class PlasticNeuron(Neuron, ABC):
    """
        Simple Neuron with AMPA and NMDA synapses.
    """

    def __init__(
            self,
            n_synapses = 10,
            # TODO: allow specifying a list of connection weights
            # TODO: allow specifying a list of initial connection weights
            connection_weight = 0.0002,
            min_distance = 100,
            max_distance = 300,
            seed = 42,
            synapse_info = None
    ):
        self.n_synapses = n_synapses
        self.connection_weight = connection_weight
        self.min_distance = min_distance
        self.max_distance = max_distance

        self.ampa = []
        self.connection_ampa = []

        self.nmda = []
        self.connection_nmda = []

        self.stimuli = []

        self.seed = seed

        self.synapse_info = synapse_info
        if self.synapse_info is not None:
            self.n_synapses = len(self.synapse_info)

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
        Inserts a synapse: generates the channel, stimulus, and connections.

        :param dendrite_idx: dendrite id
        :param dendrite_loc: location along the dendrite
        :param delay: delay of stimulus
        :return: None
        """
        ampa = h.STDPE2bis(dendrite_loc, sec = h.apical_dendrite[dendrite_idx])
        nmda = h.nmdanet(dendrite_loc, sec = h.apical_dendrite[dendrite_idx])

        stimulus = NeuronUtils.create_burst_stimulus()

        connection_ampa = NeuronUtils.connect(ampa, stimulus, delay = delay, max_weight = self.connection_weight)
        connection_nmda = NeuronUtils.connect(nmda, stimulus, delay = delay, max_weight = self.connection_weight)

        self.ampa.append(ampa)
        self.connection_ampa.append(connection_ampa)

        self.nmda.append(nmda)
        self.connection_nmda.append(connection_nmda)

        self.stimuli.append(stimulus)

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

    def run(self):
        pass
