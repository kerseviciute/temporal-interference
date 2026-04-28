rule post_stimulation_evaluation:
  input:
    subthreshold_conductance = "output/{project}/{idx}/subthreshold_conductance.txt",
    synapse_info = "output/{project}/{idx}/synapse_info.csv",
    synapse_weights = "output/{project}/{idx}/in-vivo/{stimulation}/synapse_weights.csv"
  output:
    voltage = "output/{project}/{idx}/post-stimulation/in-vivo/{stimulation}/somatic_voltage.csv"
  conda: "neuron"
  script: "../python/post-stimulation.py"
