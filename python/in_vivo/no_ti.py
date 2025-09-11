#
# Run simulation with no TI and in-vivo inputs.
#

# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd
import csv
import math
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

# Read in-vivo stimuli
stimuli = pd.read_csv(snakemake.input["in_vivo"])
stimulus_counter = -1

# Calculate the simulation duration based on the latest recorded CA3
# input, rounded to the nearest 0.5 minutes.
duration = stimuli.max().max()
duration_minutes = duration / 1000 / 60
duration_minutes = math.ceil(duration_minutes * 2) / 2
duration = int(duration_minutes * 60 * 1000)  # ms

# Define the stimulus
def in_vivo_stimulus():
    global stimulus_counter
    stimulus_counter += 1

    spike_times = stimuli[f"{stimulus_counter}"].dropna().tolist()

    spike_vec = h.Vector(spike_times)
    stimulus = h.VecStim()
    stimulus.play(spike_vec)

    return stimulus


neuron = PlasticNeuron(
    synapse_info = synapse_info,
    generate_stimulus = in_vivo_stimulus
)

NeuronUtils.set_stimulus(duration = 0)

print(f"Running simulation for {duration} ms")
print(f"Starting at: {datetime.now().strftime('%H:%M:%S')}")
neuron.run(duration)

print(f"Finished at: {datetime.now().strftime('%H:%M:%S')}")

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
