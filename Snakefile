configfile: "config.yml"

rule all:
    input:
        expand("{project}/{figure}", project = config["project"], figure = config["figures"])

rule neuron_model:
    output:
        png = "{project}/neuron_model.png"
    conda: "neuron"
    script: "figures/neuron_model.py"
