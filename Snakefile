import numpy as np

idxs = np.arange(0, 20)
initial_weight = 0.1

configfile: "config.yml"

include: "rules/subthreshold_ef.smk"
include: "rules/subthreshold_conductance.smk"

include: "rules/in_vivo.smk"
include: "rules/random_poisson.smk"
include: "rules/ltp.smk"

include: "rules/figures.smk"

rule all:
  input:
    ##### Random Poisson at 5 Hz
    ### 5 Hz + 1000 Hz carrier, at varying strengths
    expand(
      "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{beat}_{ef_strength}_{initial_weight}/synapse_weights.csv",
      project = config["project"],
      idx = idxs,
      rate = 5, # Poisson frequency
      carrier = 1000,
      beat = 5, # Stimulation frequency
      ef_strength = [0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
      initial_weight = initial_weight
    ),

    ### 5 Hz + 9000 Hz carrier, at varying strengths
    expand(
      "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{beat}_{ef_strength}_{initial_weight}/synapse_weights.csv",
      project = config["project"],
      idx = idxs,
      rate = 5, # Poisson frequency
      carrier = 9000,
      beat = 5, # Stimulation frequency
      ef_strength = [0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
      initial_weight = initial_weight
    ),

    ### 130 Hz + 1000 Hz carrier, at varying strengths
    expand(
      "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{beat}_{ef_strength}_{initial_weight}/synapse_weights.csv",
      project = config["project"],
      idx = idxs,
      rate = 5, # Poisson frequency
      carrier = 1000,
      beat = 130, # Stimulation frequency
      ef_strength = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
      initial_weight = initial_weight
    ),

    ### 1000 Hz pure carrier
    # expand(
    #   "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{beat}_{ef_strength}_{initial_weight}/synapse_weights.csv",
    #   project = config["project"],
    #   idx = idxs,
    #   rate = 5, # Poisson frequency 
    #   carrier = 1000,
    #   beat = 0, # Stimulation frequency
    #   ef_strength = [0.29, 0.32],
    #   initial_weight = initial_weight
    # ),

    ### No TI
    expand(
      "output/{project}/{idx}/random_poisson/{rate}/noTI_{initial_weight}/synapse_voltage.csv",
      project = config["project"],
      idx = idxs,
      rate = 5, # Poisson frequency
      initial_weight = initial_weight
    ),

    ##### Random Poisson inputs at various frequencies
    expand(
      "output/{project}/{idx}/random_poisson/{rate}/{carrier}_{beat}_{ef_strength}_{initial_weight}/synapse_weights.csv",
      project = config["project"],
      idx = idxs,
      rate = np.arange(1, 16, 1), # Poisson frequency TODO: increase to 30 Hz
      carrier = 1000,
      beat = 5, # Stimulation frequency
      ef_strength = [0.6],
      initial_weight = initial_weight
    )

rule generate_seeds:
  output:
    seeds = "output/{project}/seeds.csv"
  params:
    initial_seed = 42,
    n = 50
  conda: "neuron"
  script: "python/generate_seeds.py"

rule generate_synapse_locations:
  input:
    seeds = "output/{project}/seeds.csv"
  output:
    synapse_info = "output/{project}/{idx}/synapse_info.csv"
  params:
    n_synapses = 10
  conda: "neuron"
  script: "python/generate_synapse_locations.py"
