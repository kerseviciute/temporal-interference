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
    def create_constant_freq_stimulus():
        frequency = 50
        noise = 0
        delay = 0

        stimulus = h.NetStim()
        stimulus.interval = int(1000 / frequency)
        stimulus.noise = noise
        stimulus.start = delay

        return stimulus

    @staticmethod
    def create_no_stimulus():
        return None

    @staticmethod
    def create_single_stimulus():
        stimulus = h.NetStim()
        stimulus.interval = 1000
        stimulus.noise = 0
        stimulus.start = 50
        stimulus.number = 1

        return stimulus

    @staticmethod
    def set_stimulus(delay = 100, duration = 900, frequency1 = 1000, frequency2 = 1005, amplitude = 100, phase = 0):
        h.setstim(delay, duration, frequency1, frequency2, amplitude, phase)

    @staticmethod
    def set_field(psi_deg = 90, phi_deg = 90):
        field_length = 100
        h.changefield(field_length, psi_deg, phi_deg)
