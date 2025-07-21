#
# Performs no
#
rule carrier_amplitude:
    input:
        subthreshold_ef = expand("output/{{project}}/ef/{phi}_{psi}_{{carrier}}.csv", phi = 90, psi = 90)[0]
    output:
        voltage = "output/{project}/carrier_amplitude/{offset}/{another_carrier}_with_amplitude_of_{carrier}.csv"
    params:
        phase = 10,
        ef_strength = 0.9,
        duration = 5 * 1000 # ms, 5 s
    conda: "neuron"
    script: "../python/carrier_amplitude.py"
