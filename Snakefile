import numpy as np

configfile: "config.yml"

rule all:
    input:
        expand("{project}/{figure}", project = config["project"], figure = config["figures"])

rule neuron_model:
    output:
        png = "{project}/neuron_model.png"
    conda: "neuron"
    script: "figures/neuron_model.py"

rule neuron_model_with_synapses:
    output:
        png = "{project}/neuron_model_with_synapses.png"
    conda: "neuron"
    script: "figures/neuron_model_with_synapses.py"

rule generate_seeds:
    output:
        seeds = "output/{project}/seeds.csv"
    params:
        initial_seed = 42,
        n = 50
    conda: "neuron"
    script: "python/generate_seeds.py"

rule subthreshold_ef_strength:
    output:
        subthreshold = "output/{project}/ef/{angle_phi}_{angle_psi}_{carrier}.csv"
    params:
        offset_range = np.concatenate([[0], [0.5], np.arange(1, 10, 1), np.arange(10, 50, 5), np.arange(50, 140, 10)]),
        phase = 10,
        duration = 500,
        initial_amplitude = 1000,
        accuracy = 0.5
    conda: "neuron"
    script: "python/subthreshold_ef_strength.py"

rule ltp:
    input:
        seeds = "output/{project}/seeds.csv",
        subthreshold = "output/{project}/ef/{phi}_{psi}_{carrier}.csv"
    output:
        synapse_info = "output/{project}/ltp/{idx}/{carrier}/{phi}_{psi}_{offset}/synapse_info.csv",
        spike_frequency = "output/{project}/ltp/{idx}/{carrier}/{phi}_{psi}_{offset}/spike_frequency.csv",
        voltage = "output/{project}/ltp/{idx}/{carrier}/{phi}_{psi}_{offset}/voltage.csv",
        synapse_weights = "output/{project}/ltp/{idx}/{carrier}/{phi}_{psi}_{offset}/synapse_weights.csv"
    params:
        n_synapses = 10,
        initial_conductance = 0.0001,
        duration = 2000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        ef_strength = 0.9, # fraction of subthreshold amplitude
    conda: "neuron"
    script: "python/ltp.py"

rule ltp_no_ef:
    input:
        seeds = "output/{project}/seeds.csv"
    output:
        synapse_info = "output/{project}/ltp/{idx}/{carrier}/synapse_info.csv",
        spike_frequency = "output/{project}/ltp/{idx}/{carrier}/spike_frequency.csv",
        voltage = "output/{project}/ltp/{idx}/{carrier}/voltage.csv",
        synapse_weights = "output/{project}/ltp/{idx}/{carrier}/synapse_weights.csv"
    params:
        n_synapses = 10,
        initial_conductance = 0.0001,
        duration = 2000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100 # Hz
    conda: "neuron"
    script: "python/ltp.py"
