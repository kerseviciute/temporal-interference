from neuron import h
import numpy as np


class SynapseBasket:
    def __init__(
            self,
            compartment,
            location,
            stimulus = None,
            delay: float = 0.0,
            conductance: float = 0.001
    ):
        self.compartment = compartment
        self.location = location

        self.gaba_a = h.Exp2Syn(compartment(location))
        self.gaba_a.tau1 = 0.5 # ms
        self.gaba_a.tau2 = 5.0 # ms
        self.gaba_a.e = -75 # mV

        self.stimulus = stimulus
        self.delay = delay
        self.conductance = conductance

        self.connection = self.__connect()

        self.__i = h.Vector().record(self.gaba_a._ref_i)
        self.__v = h.Vector().record(compartment(location)._ref_v)

        self.__stim_times = h.Vector()
        self.connection.record(self.__stim_times)

    def __connect(self):
        connection = h.NetCon(self.stimulus, self.gaba_a)
        connection.delay = self.delay
        connection.weight[0] = self.conductance

        return connection

    @property
    def current(self):
        return np.array(self.__i)

    @property
    def voltage(self):
        return np.arange(self.__v)

    @property
    def stimuli(self):
        if len(self.__stim_times) > 0:
            return np.array(self.__stim_times) + self.delay
        else:
            return np.array([])
