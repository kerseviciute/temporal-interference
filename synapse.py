from neuron import h
import numpy as np


class Synapse:
    # NOTE: the synaptic model used here cannot undergo LTD!

    def __init__(
            self,
            dendrite_loc,
            dendrite_idx,
            stimulus,
            delay: float = 0.0,
            initial_weight: float = 0.0,
            max_weight: float = 0.0
    ):
        self.ampa = h.STDPE2bis(dendrite_loc, sec = h.apical_dendrite[dendrite_idx])
        self.ampa.initial_weight = initial_weight
        self.nmda = h.nmdanet(dendrite_loc, sec = h.apical_dendrite[dendrite_idx])
        self.stimulus = stimulus

        self.connection_ampa = self.__connect(
            self.ampa, self.stimulus, delay = delay, max_weight = max_weight
        )
        self.connection_nmda = self.__connect(
            self.nmda, self.stimulus, delay = delay, max_weight = max_weight
        )

        self.__weights_0 = h.Vector().record(self.connection_ampa._ref_weight[0])
        self.__weights_1 = h.Vector().record(self.connection_ampa._ref_weight[1])
        self.__i = h.Vector().record(self.ampa._ref_i)
        self.__g = h.Vector().record(self.ampa._ref_g)
        self.__v = h.Vector().record(h.apical_dendrite[dendrite_idx](dendrite_loc)._ref_v)

    @staticmethod
    def __connect(synapse, stimulus, delay: float = 0.0, max_weight: float = 1.0):
        connection = h.NetCon(stimulus, synapse)
        connection.delay = delay
        connection.weight[0] = max_weight

        return connection

    @property
    def weights(self):
        # weights_0 correspond to the maximum conductance
        # weights_1 correspond to the actual conductance
        return np.array(self.__weights_1 / self.__weights_0)

    @property
    def current(self):
        return np.array(self.__i)

    @property
    def conductance(self):
        return np.array(self.__g)

    @property
    def voltage(self):
        return np.array(self.__v)
