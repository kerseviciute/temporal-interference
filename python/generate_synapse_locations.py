#
# Generates synapse locations
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

seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)
print(f"{seed_idx}: Initializing neuron with random synapses")

n_synapses = int(snakemake.params["n_synapses"])

neuron = PlasticNeuron(
    n_synapses = n_synapses,
    seed = seed,
    initial_conductance = 0,
    max_distance = 300
)

neuron.synapse_info.to_csv(snakemake.output["synapse_info"])
