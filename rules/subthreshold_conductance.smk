
rule subthreshold_conductance:
    input:
        synaptic_configuration = "output/{project}/{idx}/synapse_info.csv"
    output:
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        results = "output/{project}/{idx}/subthreshold_conductance_results.csv"
    params:
        initial_weight = 0.1,

        min_conductance = 0.00005,
        max_conductance = 0.0001,
        epsilon = 0.000005,
        min_dendritic_spikes = 0.1, # 10% of synapses must have dendritic spikes

        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance.py"

rule subthreshold_conductance_theta_poisson_noTI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt"
    output:
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/noTI_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/noTI_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/noTI_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        n_synapses = 10,

        rate = 5, # Hz, poisson rate (theta frequency → 5 Hz = one burst every 200 ms)
        burst_duration = 40, # burst window in ms (typical is 30–50 ms)
        rate_outside_burst = 0, # firing frequency outside bursting interval (no spikes between bursts)

        duration = 30 * 1000 # ms, 30 seconds
    conda: "neuron"
    script: "../python/subthreshold_conductance_poisson_theta/no_ti.py"

rule subthreshold_conductance_theta_poisson_TI:
    input:
        seeds = "output/{project}/seeds.csv",
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        spike_frequency = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/subthreshold_conductance/theta_poisson/{rate_in_burst}/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
    params:
        phase = 10,

        n_synapses = 10,

        rate = 5, # Hz, poisson rate (theta frequency → 5 Hz = one burst every 200 ms)
        burst_duration = 40, # burst window in ms (typical is 30–50 ms)
        rate_outside_burst = 0, # firing frequency outside bursting interval (no spikes between bursts)

        duration = 30 * 1000 # ms, 30 seconds
    conda: "neuron"
    script: "../python/subthreshold_conductance_poisson_theta/ti.py"
