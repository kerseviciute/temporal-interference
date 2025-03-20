import numpy as np

rule all:
    input:
        expand("output/ti/cns/simulation_{i}/simulation_5hz_vm.csv", i = np.arange(1, 41))

rule simulation:
    output:
        synapses = "output/ti/cns/simulation_{i}/synapses.csv",

        no_stim_vm = "output/ti/cns/simulation_{i}/simulation_none_vm.csv",
        no_stim_syn_weight = "output/ti/cns/simulation_{i}/simulation_none_synaptic_weights.csv",

        stim_5hz_vm = "output/ti/cns/simulation_{i}/simulation_5hz_vm.csv",
        stim_5hz_weight = "output/ti/cns/simulation_{i}/simulation_5hz_synaptic_weights.csv",

        stim_100hz_vm = "output/ti/cns/simulation_{i}/simulation_100hz_vm.csv",
        stim_100hz_weight = "output/ti/cns/simulation_{i}/simulation_100hz_synaptic_weights.csv",

        stim_ti_5hz_vm = "output/ti/cns/simulation_{i}/simulation_ti_5hz_vm.csv",
        stim_ti_5hz_weight = "output/ti/cns/simulation_{i}/simulation_ti_5hz_synaptic_weights.csv",

        stim_ti_100hz_vm = "output/ti/cns/simulation_{i}/simulation_ti_100hz_vm.csv",
        stim_ti_100hz_weight = "output/ti/cns/simulation_{i}/simulation_ti_100hz_synaptic_weights.csv"
    conda: "neuron"
    script: "cns_simulation.py"
