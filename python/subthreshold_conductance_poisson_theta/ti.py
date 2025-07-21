#
# Uses subthreshold synaptic conductances and
# inputs the synapses with random Poisson stimuli trains.
#

# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import csv
import pandas as pd
import numpy as np
from neuron import h
from datetime import datetime
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils

initial_weight = float(snakemake.wildcards["initial_weight"])

# Read the initial conductance from the file
with open(snakemake.input["subthreshold_conductance"], "r") as file:
    initial_conductance = float(file.read())

synapse_info = pd.read_csv(snakemake.input["synapse_info"], index_col = 0)
synapse_info.InitialWeight = initial_weight
synapse_info.Conductance = initial_conductance

n_synapses = len(synapse_info)

# Seed will be used to generate the Poisson stimuli
seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)
np.random.seed(seed)
seeds = np.random.choice(range(10000), n_synapses, replace = False)
seed_counter = -1

rate = int(snakemake.params["rate"])
burst_duration = int(snakemake.params["burst_duration"])
rate_in_burst = int(snakemake.wildcards["rate_in_burst"])
rate_outside_burst = int(snakemake.params["rate_outside_burst"])

duration = int(snakemake.params["duration"])


def generate_poisson_theta_burst(
        frequency = 5,
        burst_duration = 50,
        duration = 1000,
        rate_in_burst = 100,
        rate_outside_burst = 1
):
    burst_times = np.arange(0, duration, 1000 / frequency)
    spike_times = []

    for t_burst in burst_times:
        # Generate Poisson spikes inside the burst window
        n_spikes = np.random.poisson(rate_in_burst * (burst_duration / 1000))
        spikes = t_burst + np.random.uniform(0, burst_duration, size = n_spikes)
        spike_times.extend(spikes)

        # Generate sparse spikes outside bursts
        outside_duration = (1000 / frequency) - burst_duration
        if outside_duration > 0:
            n_out = np.random.poisson(rate_outside_burst * (outside_duration / 1000))
            spikes_out = t_burst + burst_duration + np.random.uniform(0, outside_duration, size = n_out)
            spike_times.extend(spikes_out)

    spike_times = np.sort(np.array(spike_times))
    return spike_times


# Define the stimulus
def poisson_theta():
    global seed_counter
    seed_counter += 1

    np.random.seed(seeds[seed_counter])

    # Generate spike times
    spike_times = generate_poisson_theta_burst(
        frequency = rate,
        duration = duration,
        burst_duration = burst_duration,
        rate_in_burst = rate_in_burst,
        rate_outside_burst = rate_outside_burst
    )
    spike_vec = h.Vector(spike_times)

    stimulus = h.VecStim()
    stimulus.play(spike_vec)

    return stimulus


neuron = PlasticNeuron(
    synapse_info = synapse_info,
    generate_stimulus = poisson_theta
)
carrier = int(snakemake.wildcards["carrier"])
offset = int(snakemake.wildcards["offset"])
phase = int(snakemake.params["phase"])

ef_strength = float(snakemake.wildcards["ef_strength"])
subthreshold = pd.read_csv(snakemake.input["subthreshold_ef"])
amplitude = subthreshold.loc[subthreshold.Offset == offset, "Amplitude"].values[0]
amplitude *= ef_strength
amplitude = int(amplitude)

print("Theta bursts with TI")
print(f"carrier = {carrier} Hz")
print(f"offset = {offset} Hz")
print(f"amplitude = {amplitude} V/m ({int(ef_strength * 100)}% of original strength)")

NeuronUtils.set_stimulus(
    duration = duration,
    frequency1 = carrier,
    frequency2 = carrier + offset,
    phase = phase,
    amplitude = amplitude,
    delay = 0
)

print(f"Running simulation for {duration} ms")
print(f"Starting at: {datetime.now().strftime('%H:%M:%S')}")
neuron.run(duration)

# Save the data

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

# Drop duplicated synaptic weights for saving up the space
synapse_weights = synapse_weights.drop_duplicates(
    subset = [f"Synapse{i}" for i in range(0, 10)],
    keep = "first"
)

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
