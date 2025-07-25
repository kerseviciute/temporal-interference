rule in_vivo_inputs:
    input:
        recording = ancient(expand(
            "CA3-INVIVO-STIM/l23-06-13.res.6-tt6clu{id}.txt",
            id = [2, 3, 5, 6, 7, 8, 10, 11, 13, 14]
        ))
    output:
        stimuli = "output/{project}/in_vivo_stimuli.csv"
    conda: "neuron"
    script: "../python/in_vivo/stimuli.py"
