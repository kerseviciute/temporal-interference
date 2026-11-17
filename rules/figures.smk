
rule figure1_ef_subthreshold_trace:
    input:
        subthreshold_ef = "output/{project}/ef/90_90_1000.csv"
    output:
        voltage = "output/{project}/figures/figure1/voltage_trace_1000_4Hz_{strength}.csv"
    params:
        duration = 1000, # ms
        carrier = 1000, # Hz
        offset = 4, # Hz
        phase = 10
    conda: "neuron"
    script: "../figures/figure1_voltage_trace.py"

rule figure2_subthreshold_conductance_trace:
    input:
        synapse_info = "output/{project}/{idx}/synapse_info.csv",
        subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt"
    output:
        voltage = "output/{project}/figures/figure2/{idx}_{conductance_strength}_voltage.csv",
        weights = "output/{project}/figures/figure2/{idx}_{conductance_strength}_weights.csv"
    params:
        initial_weight = 0.1,
        duration = 3000, # ms
        ltp_start = 1000, # ms
        ltp_duration = 1000, # ms
        ltp_frequency = 100, # Hz
        test_stim_times = [100, 2500] # ms
    conda: "neuron"
    script: "../figures/figure2_subthreshold_conductace_trace.py"

rule figure2_neuron_with_synapses:
    input:
        synapse_info = "output/{project}/{idx}/synapse_info.csv"
    output:
        png = "output/{project}/figures/figure2/{idx}_neuron_with_synapses.png"
    conda: "neuron"
    script: "../figures/figure2_neuron_with_synapses.py"

rule figure3_neuron_with_all_synapses:
    input:
        synapse_info = expand("output/{{project}}/{idx}/synapse_info.csv", idx = np.arange(0, 20))
    output:
        png = "output/{project}/figures/figure3/neuron_with_all_synapses.png"
    conda: "neuron"
    script: "../figures/figure3_neuron_with_all_synapses.py"
