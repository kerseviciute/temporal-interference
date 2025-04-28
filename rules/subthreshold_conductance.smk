
rule subthreshold_conductance:
    input:
        seeds = "output/{project}/seeds.csv"
    output:
        subthreshold_conductance = "output/{project}/subthreshold_conductance/{idx}.txt",
        results = "output/{project}/subthreshold_conductance/{idx}_results.csv"
    params:
        n_synapses = 10,
        initial_weight = 0.1,

        min_conductance = 0.00005,
        max_conductance = 0.0001,
        epsilon = 0.0000005,
        min_dendritic_spikes = 0.1, # 10% of synapses must have dendritic spikes

        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance.py"

rule subthreshold_conductance_ltp_noTI:
    input:
        seeds = "output/{project}/seeds.csv",
        subthreshold_conductance = "output/{project}/subthreshold_conductance/{idx}.txt"
    output:
        synapse_info = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/synapse_info.csv",
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/ltp/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        n_synapses = 10,

        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance_ltp/no_ti.py"

rule subthreshold_conductance_ltp_TI:
    input:
        seeds = "output/{project}/seeds.csv",
        subthreshold_conductance = "output/{project}/subthreshold_conductance/{idx}.txt",
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        synapse_info = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_info.csv",
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
    params:
        phase = 10,
        n_synapses = 10,

        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance_ltp/ti.py"

rule subthreshold_conductance_random_poisson_noTI:
    input:
        seeds = "output/{project}/seeds.csv",
        subthreshold_conductance = "output/{project}/subthreshold_conductance/{idx}.txt"
    output:
        synapse_info = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/synapse_info.csv",
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        n_synapses = 10,
        duration = 10 * 1000 # ms, 10 seconds
    conda: "neuron"
    script: "../python/subthreshold_conductance_random_poisson/no_ti.py"

rule subthreshold_conductance_random_poisson_TI:
    input:
        seeds = "output/{project}/seeds.csv",
        subthreshold_conductance = "output/{project}/subthreshold_conductance/{idx}.txt",
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        synapse_info = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_info.csv",
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/random_poisson/{rate}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
    params:
        phase = 10,
        n_synapses = 10,
        duration = 10 * 1000 # ms, 10 seconds
    conda: "neuron"
    script: "../python/subthreshold_conductance_random_poisson/ti.py"
