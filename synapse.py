from neuron import h


class Synapse:
    def __init__(
            self,
            dendrite_loc,
            dendrite_idx,
            stimulus,
            delay: float = 0.0,
            initial_weight: float = 0.0,  # TODO: how to set initial weights of a netcon?
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

        # Interpretation: maximum conductance
        self.__weights_0 = h.Vector().record(self.connection_ampa._ref_weight[0])

        # Interpretation: actual conductance
        self.__weights_1 = h.Vector().record(self.connection_ampa._ref_weight[1])

        self.__weights_2 = h.Vector().record(self.connection_ampa._ref_weight[2])

    @staticmethod
    def __connect(synapse, stimulus, delay: float = 0.0, max_weight: float = 1.0):
        connection = h.NetCon(stimulus, synapse)
        connection.delay = delay
        connection.weight[0] = max_weight

        return connection

    @property
    def weights(self):
        return self.__weights_1 / self.__weights_0
