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

neuron = PlasticNeuron(n_synapses = 0)

duration = int(snakemake.params["duration"])
carrier = int(snakemake.params["carrier"])
offset = int(snakemake.params["offset"])
phase = int(snakemake.params["phase"])

ef_strength = float(snakemake.wildcards["strength"])

subthreshold = pd.read_csv(snakemake.input["subthreshold_ef"])
amplitude = subthreshold.loc[subthreshold.Offset == offset, "Amplitude"].values[0]
amplitude *= ef_strength
amplitude = int(amplitude)

print("Generating voltage trace for: ")
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

print("Starting simulation")
neuron.run(duration = duration)

# Save voltage
voltage = pd.DataFrame({
    "Voltage": neuron.voltage,
    "Time": neuron.time
})

voltage.to_csv(snakemake.output["voltage"], index = False)
