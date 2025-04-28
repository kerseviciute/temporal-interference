import numpy as np

configfile: "config.yml"

include: "rules/subthreshold_conductance.smk"

rule all:
    input:
        expand(
            "output/{project}/subthreshold_conductance/{idx}.txt",
            project = config["project"],
            idx = np.arange(0, 20)
        )

rule generate_seeds:
    output:
        seeds = "output/{project}/seeds.csv"
    params:
        initial_seed = 42,
        n = 50
    conda: "neuron"
    script: "python/generate_seeds.py"
