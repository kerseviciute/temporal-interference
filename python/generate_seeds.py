import numpy as np
import pandas as pd

initial_seed = int(snakemake.params["initial_seed"])
n_seeds = int(snakemake.params["n"])

np.random.seed(initial_seed)
seeds = np.random.randint(1, 999999, size = n_seeds)

# Replace the third one
# (results in a synaptic configuration that is too sensitive when
# estimating subthreshold conductance)
seeds = np.delete(seeds, 3)
seeds = np.append(seeds, np.random.randint(1, 999999, size = 1))

seeds = pd.DataFrame({
    "Seed": seeds
})

seeds.to_csv(snakemake.output["seeds"])
