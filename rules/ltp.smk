rule subthreshold_conductance_ltp_noTI:
    input:
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        synapse_info = "output/{project}/{idx}/synapse_info.csv"
    output:
        spike_frequency = "output/{project}/{idx}/ltp/noTI_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/ltp/noTI_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/ltp/noTI_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/ltp/noTI_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/ltp/noTI_{initial_weight}/synapse_stimuli.csv"
    params:
        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance_ltp/no_ti.py"

rule subthreshold_conductance_ltp_TI:
    input:
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        spike_frequency = "output/{project}/{idx}/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
        voltage = "output/{project}/{idx}/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
        synapse_weights = "output/{project}/{idx}/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
        synapse_voltage = "output/{project}/{idx}/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
        synapse_stimuli = "output/{project}/{idx}/ltp/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
    params:
        phase = 10,

        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../python/subthreshold_conductance_ltp/ti.py"
