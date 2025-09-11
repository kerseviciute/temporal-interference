import numpy as np

idxs = np.arange(0, 20)

configfile: "config.yml"

include: "rules/subthreshold_ef.smk"
include: "rules/subthreshold_conductance.smk"

include: "rules/in_vivo.smk"

include: "rules/figures.smk"

rule all:
    input:
        expand(
            "output/{project}/{idx}/synapse_info.csv",
            project = config["project"],
            idx = idxs
        ),

        expand(
            "output/{project}/in_vivo_stimuli.csv",
            project = config["project"]
        ),

        expand(
            "output/{project}/{idx}/in-vivo/weight_dynamics_1000.png",
            project = config["project"],
            idx = idxs
        ),

        expand(
            "output/{project}/{idx}/in-vivo/{type}/final_synapse_weights.csv",
            project = config["project"],
            idx = idxs,
            type = ["noTI_0.1", "1000_5_0.9_0.1", "1000_130_0.9_0.1", "1000_0_0.32_0.1"]
        ),

        expand(
            "output/{project}/{idx}/in-vivo/compress_voltage.done",
            project = config["project"],
            idx = idxs
        ),

        # expand(
        #     "output/{project}/carrier_amplitude/{offset}/{another_carrier}_with_amplitude_of_{carrier}.csv",
        #     project = config["project"],
        #     offset = 5,
        #     carrier = [1000, 2000, 5000, 9000],
        #     another_carrier = [1000, 2000, 5000, 9000]
        # ),

        ### Estimate subthreshold conductance
        # expand(
        #     "output/{project}/{idx}/subthreshold_conductance.txt",
        #     project = config["project"],
        #     idx = idxs
        # ),

        # # Figure stuff
        # expand(
        #     "output/{project}/figures/figure1/voltage_trace_1000_4Hz_{strength}.csv",
        #     project = config["project"],
        #     strength = [0.9, 1, 1.1]
        # ),
        # expand(
        #     "output/{project}/figures/figure2/{idx}_{conductance_strength}_voltage.csv",
        #     project = config["project"],
        #     idx = [0, 1, 2, 5, 6, 7],
        #     conductance_strength = [0.9, 1, 1.1]
        # ),
        # expand(
        #     "output/{project}/figures/figure2/{idx}_neuron_with_synapses.png",
        #     project = config["project"],
        #     idx = [0, 1, 2, 5, 6, 7]
        # ),
        # expand(
        #     "output/{project}/figures/figure3/neuron_with_all_synapses.png",
        #     project = config["project"]
        # ),
        #
        # ### LTP protocol
        # expand(
        #     "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/voltage.csv",
        #     project = config["project"],
        #     idx = idxs,
        #     initial_weight = 0.1
        # ),
        # expand(
        #     "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        #     project = config["project"],
        #     idx = idxs,
        #     carrier = [1000],
        #     offset = [5, 130],
        #     ef_strength = 0.9,
        #     initial_weight = 0.1
        # ),
        # expand(
        #     "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        #     project = config["project"],
        #     idx = idxs,
        #     carrier = [1000],
        #     offset = [0],
        #     ef_strength = [0.32], # This is the equivalent of 90% subthreshold amplitude for 130 Hz beat frequency
        #     initial_weight = 0.1
        # ),
        #
        expand(
            "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/voltage.csv",
            project = config["project"],
            idx = idxs,
            rate = np.arange(1, 31),
            initial_weight = 0.1
        ),
        expand(
            "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
            project = config["project"],
            idx = idxs,
            rate = np.arange(1, 31),
            carrier = [1000],
            offset = [5, 130],
            ef_strength = [0.9],
            initial_weight = 0.1
        ),
        expand(
            "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
            project = config["project"],
            idx = idxs,
            rate = np.arange(1, 31),
            carrier = [1000],
            offset = [0],
            ef_strength = [0.32],
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

rule generate_synapse_locations:
    input:
        seeds = "output/{project}/seeds.csv"
    output:
        synapse_info = "output/{project}/{idx}/synapse_info.csv"
    params:
        n_synapses = 10
    conda: "neuron"
    script: "python/generate_synapse_locations.py"
