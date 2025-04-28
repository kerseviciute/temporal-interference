
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
