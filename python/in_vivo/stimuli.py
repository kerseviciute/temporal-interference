import pandas as pd

stimuli = []

for i, file in enumerate(snakemake.input["recording"]):
    data = pd.read_csv(file, header = None)
    data.columns = [f"{i}"]
    data = data.sort_values(by = f"{i}")

    stimuli.append(data)

stimuli = pd.concat(stimuli, axis = 1)

stimuli.to_csv(snakemake.output["stimuli"])
