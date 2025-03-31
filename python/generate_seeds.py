import numpy as np
import pandas as pd

initial_seed = int(snakemake.params["initial_seed"])
n_seeds = int(snakemake.params["n"])

np.random.seed(initial_seed)
seeds = np.random.randint(1, 999999, size = n_seeds)

seeds = pd.DataFrame({
    "Seed": seeds
})

seeds.to_csv(snakemake.output["seeds"])
