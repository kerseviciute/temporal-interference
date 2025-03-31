#
# Performs LTP protocol with specified EF.
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


def generate_ltp_stimulus():
    stimulus = h.NetStim()
    stimulus.interval = int(1000 / ltp_frequency)
    stimulus.number = int(ltp_duration / stimulus.interval) + 1
    stimulus.noise = 0
    stimulus.start = 0

    return stimulus


# TODO: make sure this works with no stimulation as well!

duration = int(snakemake.params["duration"])
ltp_duration = int(snakemake.params["ltp_duration"])
ltp_frequency = int(snakemake.params["ltp_frequency"])

print("Initializing neuron with random synapses")
seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)
n_synapses = int(snakemake.params["n_synapses"])
initial_conductance = float(snakemake.params["initial_conductance"])

neuron = PlasticNeuron(
    n_synapses = n_synapses,
    seed = seed,
    initial_conductance = initial_conductance,
    generate_stimulus = generate_ltp_stimulus,
    generate_delay = lambda: int((duration - ltp_duration) / 2),
)

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

    print("Performing LTP protocol with EF")
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
    print("Performing LTP protocol without EF")

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
