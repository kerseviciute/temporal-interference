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

### Setup neuron synapses

with open(snakemake.input["subthreshold_conductance"], "r") as file:
  initial_conductance = float(file.read())

weight = pd.read_csv(snakemake.input["synapse_weights"], index_col = 0).iloc[-1, 1:].values

synapse_info = pd.read_csv(snakemake.input["synapse_info"], index_col = 0)
synapse_info.Conductance = initial_conductance
synapse_info.InitialWeight = weight

### Define stimuli

def test_spike(test_stimulus_1 = 200):
  """Generate Poisson-distributed spike times."""
  spikes = []
  t = test_stimulus_1
  spikes.append(t)

  return spikes

def stimulus():
  # Generate spike times
  spike_times = test_spike()

  spike_vec = h.Vector(spike_times)
  stimulus = h.VecStim()
  stimulus.play(spike_vec)

  return stimulus

### Define neuron

neuron = PlasticNeuron(
  synapse_info = synapse_info,
  generate_stimulus = stimulus
)

NeuronUtils.set_stimulus(duration = 0)

### Run simulation

neuron.run(duration = 1000)

### Save voltage at the soma

voltage = pd.DataFrame({
    "Voltage": neuron.voltage,
    "Time": neuron.time
})

voltage.to_csv(snakemake.output["voltage"])
