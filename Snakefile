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
