from neuron import h
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from copy import deepcopy

h.load_file("main.hoc")

h.random_seed = int(snakemake.wildcards["i"])
h.load_file("ampa_nmda_ltp.hoc")


def set_stimulus(delay = 100, duration = 900, frequency1 = 1000, frequency2 = 1005, amplitude = 100, phase = 0):
    h.setstim(delay, duration, frequency1, frequency2, amplitude, phase)


class Simulation:
    def __init__(self,
                 frequency1,
                 frequency2,
                 amplitude,
                 delay = 0,
                 duration = 3000,
                 n_synapses = 10,
                 ltp_start = 1000,
                 ltp_end = 2000
                 ):
        self.frequency1 = frequency1
        self.frequency2 = frequency2
        self.amplitude = amplitude
        self.delay = delay
        self.duration = duration
        self.n_synapses = n_synapses
        self.ltp_start = ltp_start
        self.ltp_end = ltp_end

        self.is_ti = frequency1 != frequency2

        self.result = None
        self.synapse_weights = None

    def run_ltp_simulation(self):
        set_stimulus(
            delay = self.delay,
            duration = self.duration - self.delay,
            frequency1 = self.frequency1,
            frequency2 = self.frequency2,
            amplitude = self.amplitude,
            phase = 0
        )

        h.tstop = self.duration

        synapse_weights = []
        for i in range(self.n_synapses):
            syn_weight = h.Vector().record(h.connections_ampa[i]._ref_weight[1])
            synapse_weights.append(syn_weight)

        soma = h.Vector().record(h.soma[0](0.5)._ref_v)
        t = h.Vector().record(h._ref_t)

        h.run()

        self.result = pd.DataFrame({
            "Time": t,
            "Soma": soma,
            "Frequency1": self.frequency1,
            "Frequency2": self.frequency2,
            "Amplitude": self.amplitude
        })

        result_syn = []
        for syn in synapse_weights:
            result_syn.append(deepcopy(np.array(syn)))

        self.synapse_weights = np.vstack(result_syn)

    def plot_result(self):
        fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 3.5))

        axs[0].plot(self.result.Time, self.result.Soma, label = "Soma", lw = 0.5, color = "black")
        axs[0].set_ylabel(r"$V_m$, mV")
        axs[0].set_xlabel("Time, ms")
        axs[0].set_ylim(-110, 70)
        axs[0].axvspan(
            self.ltp_start, self.ltp_end, alpha = 0.1,
            color = "orange",
            label = "LTP induction",
        )

        if self.is_ti:
            axs[0].set_title(
                rf"TI $\Delta f = {abs(int(self.frequency1 - self.frequency2))}$ Hz" + "\n" + rf"$E_0 = {self.amplitude}$ V/m")
        else:
            axs[0].set_title(rf"$f = {int(self.frequency1)}$ Hz" + "\n" + rf"$E_0 = {self.amplitude}$ V/m")

        for synapse in self.synapse_weights:
            axs[1].plot(self.result.Time, synapse / 0.0002, linewidth = 0.5)

        if self.is_ti:
            axs[1].set_title(
                rf"TI $\Delta f = {abs(int(self.frequency1 - self.frequency2))}$ Hz" + "\n" + rf"$E_0 = {self.amplitude}$ V/m")
        else:
            axs[1].set_title(rf"$f = {int(self.frequency1)}$ Hz" + "\n" + rf"$E_0 = {self.amplitude}$ V/m")

        axs[1].set_ylim(-0.1, 1.1)

        axs[1].axvspan(
            self.ltp_start, self.ltp_end, alpha = 0.1,
            color = "orange",
            label = "LTP induction",
        )

        axs[1].set_xlabel("Time, ms")
        axs[1].set_ylabel("Synaptic strength")

        plt.tight_layout()

    def save(self, file_vm, file_syn):
        self.result.to_csv(file_vm)
        pd.DataFrame(self.synapse_weights.T).to_csv(file_syn)


print("Saving synapse locations")
synapse_dendrites = np.array(h.synapse_dendrites)
synapse_locations = np.array(h.synapse_locations)

synapses = pd.DataFrame({
    "Dendrite": synapse_dendrites,
    "Location": synapse_locations
})

synapses.to_csv(
    snakemake.output["synapses"]
)

### NO STIMULATION

simulation_nostim = Simulation(
    frequency1 = 0,
    frequency2 = 0,
    amplitude = 0
)

print("Running: no stimulation")

simulation_nostim.run_ltp_simulation()

print("Saving: no stimulation")

simulation_nostim.save(snakemake.output["no_stim_vm"], snakemake.output["no_stim_syn_weight"])

### 5 Hz STIMULATION

simulation_5hz = Simulation(
    frequency1 = 5,
    frequency2 = 5,
    amplitude = 25
)

print("Running: 5 Hz stimulation")

simulation_5hz.run_ltp_simulation()

print("Saving: 5 Hz stimulation")

simulation_5hz.save(snakemake.output["stim_5hz_vm"], snakemake.output["stim_5hz_weight"])

### 100 Hz STIMULATION

simulation_100hz = Simulation(
    frequency1 = 100,
    frequency2 = 100,
    amplitude = 50
)

print("Running: 100 Hz stimulation")

simulation_100hz.run_ltp_simulation()

print("Saving: 100 Hz stimulation")

simulation_100hz.save(snakemake.output["stim_100hz_vm"], snakemake.output["stim_100hz_weight"])

### 5 Hz TI STIMULATION

simulation_ti_5hz = Simulation(
    frequency1 = 1000,
    frequency2 = 1005,
    amplitude = 150
)

print("Running: TI 5 Hz stimulation")

simulation_ti_5hz.run_ltp_simulation()

print("Saving: TI 5 Hz stimulation")

simulation_ti_5hz.save(snakemake.output["stim_ti_5hz_vm"], snakemake.output["stim_ti_5hz_weight"])

### 100 Hz TI STIMULATION

simulation_ti_100hz = Simulation(
    frequency1 = 1000,
    frequency2 = 1100,
    amplitude = 180
)

print("Running: TI 100 Hz stimulation")

simulation_ti_100hz.run_ltp_simulation()

print("Saving: TI 100 Hz stimulation")

simulation_ti_100hz.save(snakemake.output["stim_ti_100hz_vm"], snakemake.output["stim_ti_100hz_weight"])

