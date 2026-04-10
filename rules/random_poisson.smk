import numpy as np

rule random_poisson_noTI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt"
    output:
        spike_frequency = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/spike_frequency.csv",
        # voltage = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_weights.csv",
        # synapse_voltage = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_voltage.csv",
        # synapse_stimuli = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        duration = 10 * 1000 # ms, 10 seconds
    conda: "neuron"
    script: "../python/random_poisson/no_ti.py"

rule random_poisson_TI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        subthreshold_ef = expand("output/{{project}}/variable-time-ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        spike_frequency = "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
    params:
        phase = 10,
        duration = 10 * 1000 # ms, 10 seconds
    conda: "neuron"
    script: "../python/random_poisson/ti.py"

rule random_poisson_plot_weights:
    input:
        weights = expand(
            "output/{{project}}/{idx}/random_poisson/{{rate}}/{type}/synapse_weights.csv",
            idx = idxs,
            type = "noTI_0.1"
        ),
        weights_5 = expand(
            "output/{{project}}/{idx}/random_poisson/{{rate}}/{type}/synapse_weights.csv",
            idx = idxs,
            type = "1000_5_0.9_0.1"
        ),
        weights_130 = expand(
            "output/{{project}}/{idx}/random_poisson/{{rate}}/{type}/synapse_weights.csv",
            idx = idxs,
            type = "1000_130_0.9_0.1"
        ),
        weights_0 = expand(
            "output/{{project}}/{idx}/random_poisson/{{rate}}/{type}/synapse_weights.csv",
            idx = idxs,
            type = "1000_0_0.32_0.1"
        )
    output:
        weight_dynamics = "output/{project}/random_poisson/{rate}_weight_dynamics.png",
        summary = "output/{project}/random_poisson/{rate}_summary.png"
    conda: "neuron"
    script: "../python/random_poisson/plot_weights.py"

rule random_poisson_gif:
    input:
        summaries = expand(
            "output/{{project}}/random_poisson/{rate}_summary.png",
            rate = np.arange(1, 31)
        )
    output:
        gif = "output/{project}/random_poisson/summary.gif"
    conda: "neuron"
    script: "../python/random_poisson/summary_gif.py"
