import numpy as np
import pandas as pd
from abstract_neuron import AbstractNeuron
from neuron import h
import random
from neuron_utils import NeuronUtils
from synapse_ca3 import SynapseCA3
# from synapse_basket import SynapseBasket
from copy import deepcopy


class PlasticNeuron(AbstractNeuron):
    """
        Simple Neuron with AMPA and NMDA synapses.
    """

    def __init__(
            self,
            n_synapses = 10,
            # TODO: allow specifying a list of connection weights (maximal allowed conductances)
            # TODO: allow specifying a list of initial connection weights
            initial_conductance = 0.00005,
            initial_weight: float = 0,
            min_distance = 100,  # 50?
            max_distance = 350,  # 350
            max_diameter = 1,  # avoid placing the synapses on the apical trunk

            ap_threshold = -20,

            seed = 42,

            synapse_info = None,

            generate_stimulus = NeuronUtils.create_constant_freq_stimulus,
            generate_delay = lambda: 0,

            # # Parameters for inhibitory basket cells
            # basket_n_synapses = 0,
            # basket_fraction = None,
            # basket_conductance: float = 0.0,
            # basket_min_distance = 0,
            # basket_max_distance = 100,
            # basket_generate_delay = lambda: 5,
            # basket_generate_stimulus = NeuronUtils.create_constant_freq_stimulus
    ):
        """
        NOTE: initialization order is important.

        :param n_synapses: number of synapses

        :param initial_conductance: initial synapse conductance. The maximum conductance is
                                    double the initial conductance when fully potentiated

        :param initial_weight: initial synapse weight, specified as the degree of potentiation
                               in the interval [0, 1]

        :param min_distance: minimum synapse distance from the soma

        :param max_distance: maximum synapse distance from the soma

        :param seed: seed for random initializations

        :param synapse_info: a data frame with synapse information. If not provided, synapses
                             will be generated randomly. If provided, other parameters (n_synapses,
                             initial_conductance, initial_weight, min_distance, max_distance) are ignored

        :param generate_stimulus: a function used to generate stimuli for the synapses

        :param generate_delay: a function used to generate the delay of synaptic inputs
        """

        self.n_synapses = n_synapses
        self.initial_conductance = initial_conductance
        self.initial_weight = initial_weight
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.max_diameter = max_diameter

        self.synapses = []

        self.seed = seed

        self.synapse_info = synapse_info
        if self.synapse_info is not None:
            self.n_synapses = len(self.synapse_info)

        self.generate_stimulus = generate_stimulus
        self.stimulus = None

        self.generate_delay = generate_delay

        # Inhibitory basket cell definitions
        # self.basket_n_synapses = basket_n_synapses
        #
        # if basket_fraction is None:
        #     basket_fraction = dict({
        #         "Soma": 1 / 3,
        #         "Apical": 1 / 3,
        #         "Basal": 1 / 3
        #     })
        #
        # self.basket_fraction = basket_fraction
        # self.basket_conductance = basket_conductance
        # self.basket_min_distance = basket_min_distance
        # self.basket_max_distance = basket_max_distance
        # self.basket_generate_delay = basket_generate_delay
        # self.basket_generate_stimulus = basket_generate_stimulus
        #
        # self.basket_synapse_info = pd.DataFrame()
        # self.basket_synapses = []

        super().__init__()

        self.__v = h.Vector().record(h.soma[0](0.5)._ref_v)
        self.__t = h.Vector().record(h._ref_t)

        # Record spike times
        self.__spike_times = h.Vector()
        ap_connection = h.NetCon(h.soma[0](0.5)._ref_v, None, sec = h.soma[0])
        ap_connection.threshold = ap_threshold
        ap_connection.record(self.__spike_times)

        self.__input_stimulus = h.Vector().record(h.soma[0](0.5).xtrau._ref_er)

    def get_synapse_info(self):
        return self.synapse_info

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
            dendrite_idx, dendrite_loc, distance, diameter = NeuronUtils.generate_synapse_location_apical(
                n_apical_dendrites = n_apical_dendrites,
                max_distance = self.max_distance,
                min_distance = self.min_distance,
                max_diameter = self.max_diameter
            )

            delay = self.generate_delay()

            self.__insert_synapse(
                dendrite_idx = dendrite_idx,
                dendrite_loc = dendrite_loc,
                delay = delay,
                initial_conductance = self.initial_conductance,
                initial_weight = self.initial_weight
            )

            synapse_info.append(pd.DataFrame({
                "Dendrite": [dendrite_idx],
                "Location": [dendrite_loc],
                "Distance": [distance],
                "Diameter": [diameter],
                "Delay": [delay],
                "Conductance": [self.initial_conductance],
                "InitialWeight": [self.initial_weight]
            }))

        if self.n_synapses > 0:
            self.synapse_info = pd.concat(synapse_info, ignore_index = True)

    def __insert_synapse(
            self,
            dendrite_idx,
            dendrite_loc,
            delay,
            initial_conductance,
            initial_weight
    ):
        """
        Inserts a synapse at the specified location.

        :param dendrite_idx: dendrite id
        :param dendrite_loc: location along the dendrite
        :param delay: delay of stimulus
        :return: None
        """

        stimulus = self.generate_stimulus()

        synapse = SynapseCA3(
            dendrite_idx = dendrite_idx,
            dendrite_loc = dendrite_loc,
            stimulus = stimulus,
            delay = delay,
            initial_conductance = initial_conductance,
            initial_weight = initial_weight
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
            initial_conductance = synapse.Conductance
            initial_weight = synapse.InitialWeight

            self.__insert_synapse(
                dendrite_idx = dendrite_idx,
                dendrite_loc = dendrite_loc,
                delay = delay,
                initial_conductance = initial_conductance,
                initial_weight = initial_weight
            )

    def initialize(self):
        if self.synapse_info is not None:
            print("Reading synapse information")
            self.__read_synapses()
            # TODO: save and read basket cell information
        else:
            print("Generating synapse information")
            self.__generate_synapses()
            # self.__generate_basket_synapse()

    def get_final_synapse_info(self):
        synapse_info = deepcopy(self.synapse_info)

        final_weights = [ synapse.weights[-1] for synapse in self.synapses ]
        synapse_info.InitialWeight = final_weights

        return synapse_info

    def set_initial_conductance(self, conductance):
        for synapse in self.synapses:
            synapse.set_initial_conductance(conductance)

        self.synapse_info.Conductance = conductance

    @property
    def voltage(self):
        return np.array(self.__v)

    @property
    def time(self):
        return np.array(self.__t)

    @property
    def spike_times(self):
        if len(self.__spike_times) > 0:
            return np.array(self.__spike_times)
        else:
            return np.array([])

    @property
    def spike_frequency(self):
        if len(self.spike_times) > 1:
            isi = np.diff(self.spike_times)
            instantaneous_freq = 1000 / isi
            spike_time = self.spike_times[1:]
        else:
            instantaneous_freq = []
            spike_time = []

        return instantaneous_freq, spike_time

    @property
    def input_stimulus(self):
        return np.array(self.__input_stimulus)

    # def __determine_basket_compartment(self):
    #     probability = random.uniform(0, 1)
    #     soma, apical = self.basket_fraction["Soma"], self.basket_fraction["Apical"]
    #     if probability < soma: return "Soma"
    #     if probability < soma + apical: return "Apical"
    #     return "Basal"
    #
    # def __generate_basket_synapse(self):
    #     """
    #     Generates and inserts new inhibitory basket synapses at random locations.
    #
    #     :return: None
    #     """
    #     random.seed(self.seed)
    #
    #     print(f"Inserting {self.basket_n_synapses} inhibitory basket synapses")
    #
    #     synapse_info = []
    #     for synapse in range(self.basket_n_synapses):
    #         compartment_type = self.__determine_basket_compartment()
    #         print(f"Inserting basket cell in compartment: {compartment_type}")
    #
    #         compartment, idx, location, distance = NeuronUtils.generate_synapse_location(
    #             compartment_type = compartment_type,
    #             max_distance = self.basket_max_distance,
    #             min_distance = self.basket_min_distance
    #         )
    #
    #         delay = self.basket_generate_delay()
    #
    #         self.__insert_basket_synapses(
    #             compartment = compartment,
    #             location = location,
    #             delay = delay,
    #             conductance = self.basket_conductance
    #         )
    #
    #         synapse_info.append(pd.DataFrame({
    #             "Compartment": [compartment_type],
    #             "CompartmentID": [idx],
    #             "Location": [location],
    #             "Distance": [distance],
    #             "Delay": [delay],
    #             "Conductance": [self.basket_conductance]
    #         }))
    #
    #     if self.basket_n_synapses > 0:
    #         self.basket_synapse_info = pd.concat(synapse_info, ignore_index = True)
    #
    # def __insert_basket_synapses(
    #         self,
    #         compartment,
    #         location,
    #         delay,
    #         conductance
    # ):
    #     stimulus = self.basket_generate_stimulus()
    #
    #     synapse = SynapseBasket(
    #         compartment = compartment,
    #         location = location,
    #         stimulus = stimulus,
    #         delay = delay,
    #         conductance = conductance
    #     )
    #
    #     self.basket_synapses.append(synapse)
