import numpy as np

configfile: "config.yml"

include: "rules/subthreshold_ef.smk"
include: "rules/subthreshold_conductance.smk"

rule all:
    input:
        ### Estimate subthreshold conductance
        expand(
            "output/{project}/subthreshold_conductance/{idx}.txt",
            project = config["project"],
            idx = np.arange(0, 20)
        ),

        ### LTP protocol with subthreshold conductance
        expand(
            "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_info.csv",
            project = config["project"],
            idx = np.arange(0, 20),
            carrier = 1000,
            offset = [0, 5, 130],
            ef_strength = [0.9, 1],
            initial_weight = 0.1
        ),
        expand(
            "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/synapse_info.csv",
            project = config["project"],
            idx = np.arange(0, 20),
            initial_weight = 0.1
        )

rule generate_seeds:
    output:
        seeds = "output/{project}/seeds.csv"
    params:
        initial_seed = 42,
        n = 50
    conda: "neuron"
    script: "python/generate_seeds.py"
