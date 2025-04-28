#
# Performs LTP protocol without EF and with different initial conductance.
#

# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import csv
from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils


duration = int(snakemake.params["duration"])
ltp_start = int(snakemake.params["ltp_start"])
ltp_duration = int(snakemake.params["ltp_duration"])
ltp_frequency = int(snakemake.params["ltp_frequency"])

print("Initializing neuron with random synapses")
seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)

n_synapses = int(snakemake.params["n_synapses"])
initial_conductance = float(snakemake.wildcards["conductance"])
initial_weight = float(snakemake.params["initial_weight"])

test_stimulus_1, test_stimulus_2 = [
    int(stimulus_time) for stimulus_time in snakemake.params["test_stim_times"]
]


def generate_ltp_spike_times():
    """Generate Poisson-distributed spike times."""
    spikes = []
    t = test_stimulus_1
    spikes.append(t)

    t = ltp_start
    while t < ltp_start + ltp_duration:
        spikes.append(t)
        isi = int(1000 / ltp_frequency)
        t += isi

    t = test_stimulus_2
    spikes.append(t)

    return spikes


# Define the stimulus
def ltp_stimulus():
    # Generate spike times
    spike_times = generate_ltp_spike_times()

    spike_vec = h.Vector(spike_times)
    stimulus = h.VecStim()
    stimulus.play(spike_vec)

    return stimulus


neuron = PlasticNeuron(
    n_synapses = n_synapses,
    seed = seed,
    initial_conductance = initial_conductance,
    initial_weight = initial_weight,
    generate_stimulus = ltp_stimulus
)

NeuronUtils.set_stimulus(
    duration = ltp_duration + 200,
    frequency1 = 1000,
    frequency2 = 1005,
    phase = 10,
    amplitude = 134,
    delay = ltp_start - 100
)

print("Starting simulation")
neuron.run(duration = duration)

# Save the data

# Save synapse location info
synapse_info = neuron.get_final_synapse_info()
synapse_info.to_csv(snakemake.output["synapse_info"])

# Save spike frequency
spike_frequency, spike_time = neuron.spike_frequency
spike_frequency = pd.DataFrame({
    "Frequency": spike_frequency,
    "Time": spike_time
})

spike_frequency.to_csv(snakemake.output["spike_frequency"])

# Save voltage
voltage = pd.DataFrame({
    "Voltage": neuron.voltage,
    "Time": neuron.time
})

voltage.to_csv(snakemake.output["voltage"])

# Save synaptic weights over time
synapse_weights = pd.DataFrame({
    "Time": neuron.time
})

for i, synapse in enumerate(neuron.synapses):
    synapse_weights[f"Synapse{i}"] = synapse.weights

synapse_weights.to_csv(snakemake.output["synapse_weights"])

# Save voltages at the synaptic locations

synapse_voltage = pd.DataFrame({
    "Time": neuron.time
})

for i, synapse in enumerate(neuron.synapses):
    synapse_voltage[f"Synapse{i}"] = synapse.voltage

synapse_voltage.to_csv(snakemake.output["synapse_voltage"])

# Save inputs to the synapse

synapse_stimuli = []

for i, synapse in enumerate(neuron.synapses):
    synapse_stimuli.append(synapse.stimuli)

synapse_stimuli = [list(row) for row in synapse_stimuli]
max_len = max(len(row) for row in synapse_stimuli)
padded_data = [row + [""] * (max_len - len(row)) for row in synapse_stimuli]

with open(snakemake.output["synapse_stimuli"], "w", newline = "") as f:
    writer = csv.writer(f)
    writer.writerows(padded_data)
