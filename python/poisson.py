#
# Uses synaptic weights obtained during LTP protocol and
# inputs the synapses with random Poisson stimuli trains.
#

# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from neuron import h

from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils


synapse_info = pd.read_csv(snakemake.input["synapse_info"])
# Resetting the delay
synapse_info.Delay = 0

# Seed will be used to generate the Poisson stimuli
seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)
np.random.seed(seed)
seeds = np.random.choice(range(10000), len(synapse_info), replace = False)
seed_counter = -1

rate = int(snakemake.params["rate"])
duration = int(snakemake.params["duration"])


def generate_poisson_spike_times(rate, duration):
    """Generate Poisson-distributed spike times."""
    spikes = []
    t = np.random.exponential(1000 / rate)
    spikes.append(t)

    while t < duration:
        spikes.append(t)
        isi = np.random.exponential(1000 / rate)  # Exponential ISI
        t += isi

    return spikes


# Define the stimulus
def poisson_stimulus():
    global seed_counter
    seed_counter += 1

    np.random.seed(seeds[seed_counter])

    # Generate spike times
    spike_times = generate_poisson_spike_times(rate, duration)

    spike_vec = h.Vector(spike_times)
    stimulus = h.VecStim()
    stimulus.play(spike_vec)

    return stimulus


neuron = PlasticNeuron(
    synapse_info = synapse_info,
    generate_stimulus = poisson_stimulus
)

# Get the information about the stimulus used to generate the synaptic weights
carrier = int(snakemake.wildcards["carrier"])

# Will set up TI stimulation only if carrier is non-zero
if carrier != 0:
    offset = int(snakemake.wildcards["offset"])
    phi = int(snakemake.wildcards["phi"])
    psi = int(snakemake.wildcards["psi"])

    ef_strength = float(snakemake.params["ef_strength"])
    subthreshold = pd.read_csv(snakemake.input["subthreshold"])
    amplitude = subthreshold.loc[subthreshold.Offset == offset, "Amplitude"].values[0]
    amplitude *= ef_strength
    amplitude = int(amplitude)

    print("Poisson inputs with EF")
    print(f"carrier = {carrier} Hz")
    print(f"offset = {offset} Hz")
    print(f"amplitude = {amplitude} V/m ({int(ef_strength * 100)}% of original strength)")

    NeuronUtils.set_stimulus(
        duration = duration,
        frequency1 = carrier,
        frequency2 = carrier + offset,
        phase = 10,
        amplitude = amplitude,
        delay = 0
    )

    NeuronUtils.set_field(
        psi_deg = psi,
        phi_deg = phi
    )
else:
    NeuronUtils.set_stimulus(duration = 0, amplitude = 0)
    print("Poisson inputs without EF")

print(f"Running simulation for {duration} ms")
neuron.run(duration)

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

