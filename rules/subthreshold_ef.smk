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
