#
# Performs LTP protocol without EF and with different initial conductance.
#

# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils


duration = int(snakemake.params["duration"])
ltp_start = int(snakemake.params["ltp_start"])
ltp_duration = int(snakemake.params["ltp_duration"])
ltp_frequency = int(snakemake.params["ltp_frequency"])

conductance_strength = float(snakemake.wildcards["conductance_strength"])

# Read the initial conductance from the file
with open(snakemake.input["subthreshold_conductance"], "r") as file:
    initial_conductance = float(file.read())
    initial_conductance *= conductance_strength

initial_weight = float(snakemake.params["initial_weight"])

synapse_info = pd.read_csv(snakemake.input["synapse_info"], index_col = 0)
synapse_info.InitialWeight = initial_weight
synapse_info.Conductance = initial_conductance

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
    synapse_info = synapse_info,
    generate_stimulus = ltp_stimulus
)

NeuronUtils.set_stimulus(duration = 0)

print(f"Starting simulation with conductance {format(initial_conductance * 1000, '.10f')} nS "
      f"({round(conductance_strength * 100)}% of initial conductance strength)")
neuron.run(duration = duration)

# Save the data

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

synapse_weights.to_csv(snakemake.output["weights"])
