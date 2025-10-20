import numpy as np

rule subthreshold_ef_strength:
    output:
        subthreshold = "output/{project}/ef/{angle_phi}_{angle_psi}_{carrier}.csv"
    params:
        offset_range = np.concatenate([
            np.array([0]),
            np.array([0.5]),
            np.arange(1, 10, 1),
            np.arange(10, 50, 5),
            np.arange(50, 140, 10)
        ]),
        phase = 10,
        duration = 500,
        initial_amplitude = 1000,
        accuracy = 0.5
    conda: "neuron"
    script: "../python/subthreshold_ef_strength.py"

rule subthreshold_ef_beat:
    output:
        subthreshold = "output/{project}/variable-time-ef-intermediate/{angle_phi}_{angle_psi}_{carrier}_{beat}.csv"
    params:
        phase = 10,
        duration = 1000, # ms
        initial_amplitude = 2000,
        accuracy = 0.5
    conda: "neuron"
    script: "../python/subthreshold_ef_beat.py"

rule variable_time_subthreshold_ef:
    input:
        expand(
            "output/{{project}}/variable-time-ef-intermediate/{{angle_phi}}_{{angle_psi}}_{{carrier}}_{beat}.csv",
            beat = [0, 0.5] + list(range(1, 10, 1)) + list(range(10, 50, 5)) + list(range(50, 150, 10))
        )
    output:
        "output/{project}/variable-time-ef/{angle_phi}_{angle_psi}_{carrier}.csv"
    conda: "neuron"
    script: "../python/subthreshold_ef_merge.py"

