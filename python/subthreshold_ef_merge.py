import pandas as pd

data = []

for file in snakemake.input["files"]:
    data.append(pd.read_csv(file))

data = pd.concat(data, ignore_index = True)
data.to_csv(snakemake.output["subthreshold_ef"], index = False)
