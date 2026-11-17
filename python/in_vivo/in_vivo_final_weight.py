import os
import pandas as pd
import numpy as np


def read_n_to_last_line(filename, n = 1):
    """Returns the nth before last line of a file (n=1 gives last line)"""
    # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line


def get_final_weights(filename):
    last_line = read_n_to_last_line(filename, n = 1)
    last_line = last_line.split(",")
    synaptic_weights = [float(element) for element in last_line][2:]

    return synaptic_weights


weights_file = snakemake.input["weights"]
idx = snakemake.wildcards["idx"]

final_weights = get_final_weights(weights_file)
final_weights = pd.DataFrame({
    "ID": idx,
    "Synapse": np.arange(0, 10),
    "Weight": final_weights
})

final_weights.to_csv(snakemake.output["final_weights"], index = False)
