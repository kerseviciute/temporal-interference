rule random_poisson_noTI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt"
    output:
        spike_frequency = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        duration = 10 * 1000 # ms, 10 seconds
    conda: "neuron"
    script: "../python/random_poisson/no_ti.py"

rule random_poisson_TI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
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
