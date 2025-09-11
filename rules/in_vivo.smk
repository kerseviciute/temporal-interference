# rule in_vivo_inputs:
#     input:
#         recording = ancient(expand(
#             "CA3-INVIVO-STIM/l23-06-13.res.6-tt6clu{id}.txt",
#             id = [2, 3, 5, 6, 7, 8, 10, 11, 13, 14]
#         ))
#     output:
#         stimuli = "output/{project}/in_vivo_stimuli.csv"
#     conda: "neuron"
#     script: "../python/in_vivo/stimuli.py"
#
# rule in_vivo_noTI:
#     input:
#         in_vivo = "output/{project}/in_vivo_stimuli.csv",
#         synapse_info = "output/{project}/{idx}/synapse_info.csv",
#         subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt"
#     output:
#         spike_frequency = "output/{project}/{idx}/in-vivo/noTI_{initial_weight}/spike_frequency.csv",
#         voltage = "output/{project}/{idx}/in-vivo/noTI_{initial_weight}/voltage.csv",
#         synapse_weights = "output/{project}/{idx}/in-vivo/noTI_{initial_weight}/synapse_weights.csv",
#         synapse_voltage = "output/{project}/{idx}/in-vivo/noTI_{initial_weight}/synapse_voltage.csv",
#         synapse_stimuli = "output/{project}/{idx}/in-vivo/noTI_{initial_weight}/synapse_stimuli.csv"
#     conda: "neuron"
#     script: "../python/in_vivo/no_ti.py"
#
# rule in_vivo_TI:
#     input:
#         in_vivo = "output/{project}/in_vivo_stimuli.csv",
#         synapse_info = "output/{project}/{idx}/synapse_info.csv",
#         subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
#         subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
#     output:
#         spike_frequency = "output/{project}/{idx}/in-vivo/{carrier}_{offset}_{ef_strength}_{initial_weight}/spike_frequency.csv",
#         voltage = "output/{project}/{idx}/in-vivo/{carrier}_{offset}_{ef_strength}_{initial_weight}/voltage.csv",
#         synapse_weights = "output/{project}/{idx}/in-vivo/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_weights.csv",
#         synapse_voltage = "output/{project}/{idx}/in-vivo/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_voltage.csv",
#         synapse_stimuli = "output/{project}/{idx}/in-vivo/{carrier}_{offset}_{ef_strength}_{initial_weight}/synapse_stimuli.csv"
#     params:
#         phase = 10
#     conda: "neuron"
#     script: "../python/in_vivo/ti.py"
#
# rule in_vivo_figure_weight_dynamics_1000:
#     input:
#         no_ti = "output/{project}/{idx}/in-vivo/noTI_0.1/synapse_weights.csv",
#         ti_5 = "output/{project}/{idx}/in-vivo/1000_5_0.9_0.1/synapse_weights.csv",
#         ti_130 = "output/{project}/{idx}/in-vivo/1000_130_0.9_0.1/synapse_weights.csv",
#         ti_0 = "output/{project}/{idx}/in-vivo/1000_0_0.32_0.1/synapse_weights.csv"
#     output:
#         png = "output/{project}/{idx}/in-vivo/weight_dynamics_1000.png"
#     conda: "neuron"
#     script: "../python/in_vivo/weight_dynamics.py"

rule in_vivo_figure_synapse_info_1000:
    input:
        in_vivo = "output/{project}/in_vivo_stimuli.csv",

        weights_no_ti = "output/{project}/{idx}/in-vivo/noTI_0.1/synapse_weights.csv",
        voltage_no_ti = "output/{project}/{idx}/in-vivo/noTI_0.1/synapse_voltage.csv.gz",

        weights_ti_5 = "output/{project}/{idx}/in-vivo/1000_5_0.9_0.1/synapse_weights.csv",
        voltage_ti_5 = "output/{project}/{idx}/in-vivo/1000_5_0.9_0.1/synapse_voltage.csv.gz",

        weights_ti_130 = "output/{project}/{idx}/in-vivo/1000_130_0.9_0.1/synapse_weights.csv",
        voltage_ti_130 = "output/{project}/{idx}/in-vivo/1000_130_0.9_0.1/synapse_voltage.csv.gz",

        weights_ti_0 = "output/{project}/{idx}/in-vivo/1000_0_0.32_0.1/synapse_weights.csv",
        voltage_ti_0 = "output/{project}/{idx}/in-vivo/1000_0_0.32_0.1/synapse_voltage.csv.gz"
    output:
        png = "output/{project}/{idx}/in-vivo/synapse_{synapse_idx}_info.png"
    conda: "neuron"
    script: "../python/in_vivo/synapse_plot.py"

rule in_vivo_force_compress:
    input:
        voltage_no_ti = "output/{project}/{idx}/in-vivo/noTI_0.1/synapse_voltage.csv.gz",
        voltage_ti_5 = "output/{project}/{idx}/in-vivo/1000_5_0.9_0.1/synapse_voltage.csv.gz",
        voltage_ti_130 = "output/{project}/{idx}/in-vivo/1000_130_0.9_0.1/synapse_voltage.csv.gz",
        voltage_ti_0 = "output/{project}/{idx}/in-vivo/1000_0_0.32_0.1/synapse_voltage.csv.gz"
    output:
        touch("output/{project}/{idx}/in-vivo/compress_voltage.done")

rule in_vivo_compress:
    input:
        csv = "output/{project}/{idx}/in-vivo/{type}/{filetype}.csv"
    output:
        zip = "output/{project}/{idx}/in-vivo/{type}/{filetype}.csv.gz"
    conda: "neuron"
    shell:
        """
            gzip -v {input.csv}
        """

rule in_vivo_mean_weight:
    input:
        weights = expand(
            "output/{{project}}/{idx}/in-vivo/{{type}}/synapse_weights.csv",
            idx = idxs
        )
    output:
        mean_weight = "output/{project}/in-vivo/{type}/mean_synapse_weights.csv"
    conda: "neuron"
    script: "../python/in_vivo/in_vivo_average.py"

rule in_vivo_final_weight:
    input:
        weights = "output/{project}/{idx}/in-vivo/{type}/synapse_weights.csv"
    output:
        final_weights = "output/{project}/{idx}/in-vivo/{type}/final_synapse_weights.csv"
    conda: "neuron"
    script: "../python/in_vivo/in_vivo_final_weight.py"
