import matplotlib.pyplot as plt


class NeuronPlots:
    @staticmethod
    def plot_all_synapses(neuron):
        fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize = (10, 10))
        axs = axs.flatten()

        for synapse in neuron.synapses:
            axs[0].plot(neuron.time, synapse.weights)

        axs[0].set_ylim(-0.1, 1.1)
        axs[0].set_title("Synaptic weights")

        for synapse in neuron.synapses:
            axs[1].plot(neuron.time, synapse.current, linewidth = 0.5)

        axs[1].set_title("Synapse current")

        for synapse in neuron.synapses:
            axs[2].plot(neuron.time, synapse.conductance, linewidth = 0.5)

        axs[2].set_title("Synapse conductance")

        for synapse in neuron.synapses:
            axs[3].plot(neuron.time, synapse.voltage, linewidth = 0.5)

        axs[3].set_title("Synapse EPSP")
