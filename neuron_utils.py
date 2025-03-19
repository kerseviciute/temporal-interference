from neuron import h
import random


class NeuronUtils:
    @staticmethod
    def count_section(section_name):
        return sum([ section_name in section.name() for section in h.allsec() ])

    @staticmethod
    def generate_synapse_location(n_apical_dendrites, max_distance, min_distance):
        """
        Generates a random synapse location within the allowed distance bounds.

        :param n_apical_dendrites: number of apical dendrites
        :param max_distance: maximum distance to soma
        :param min_distance: minimum distance to soma
        :return: dendrite id, position along the dendrite, and distance to the soma
        """

        distance_to_soma = max_distance + 1
        dendrite_idx = -1
        loc_pos = -1.0

        while distance_to_soma > max_distance or distance_to_soma < min_distance:
            dendrite_idx = random.randint(0, n_apical_dendrites - 1)
            loc_pos = random.uniform(0, 1)
            dendrite = h.apical_dendrite[dendrite_idx]

            distance_to_soma = h.distance(dendrite(loc_pos))

        return dendrite_idx, loc_pos, distance_to_soma

    @staticmethod
    def create_burst_stimulus():
        stimulus = h.BurstStim3()
        stimulus.interval = 25
        stimulus.noise = 0
        stimulus.burstlen = 100
        stimulus.burstint = 250 - stimulus.burstlen

        return stimulus

    @staticmethod
    def connect(synapse, stimulus, delay: float = 0.0, initial_weight: float = 0.0, max_weight: float = 1.0):
        connection = h.NetCon(stimulus, synapse)
        connection.delay = delay
        connection.weight[0] = max_weight
        connection.weight[1] = initial_weight

        return connection
