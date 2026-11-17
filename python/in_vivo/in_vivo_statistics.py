import csv
import numpy as np
from datetime import datetime

files = snakemake.input["weights"]
output = snakemake.output["statistics"]

print("Creating CSV readers")
fps = [open(file, "r") for file in files]
readers = [csv.reader(fp, delimiter = ",") for fp in fps]

# 10 synapses per file
n_synapses_file = 10
n_synapses = len(readers) * n_synapses_file

print(f"Number of synapses: {n_synapses}")

# Read and ignore the headers
for reader in readers:
    header = next(reader)

print("Ignored header row")

line_counter = 0
line_synapses = np.zeros(n_synapses)
sqrt_len = np.sqrt(n_synapses)

n_total_lines = 25200001

print(f"{snakemake.wildcards['type']} Starting at: {datetime.now().strftime('%H:%M:%S')}")

with open(str(output), "w") as fout:
    writer = csv.writer(fout)
    writer.writerow(["Time", "Mean", "SD", "SEM"])

    # Calculate the sum for each line
    for reader_rows in zip(*readers):
        line_counter += 1

        if line_counter % 100_000 == 0:
            print(f"{snakemake.wildcards['type']} {round(line_counter / n_total_lines, 3)}% done at {datetime.now().strftime('%H:%M:%S')}")

        for i, values in enumerate(reader_rows):
            line_synapses[(i * n_synapses_file):((i + 1) * n_synapses_file)] = [float(val) for val in values[2:]]

        time = float(values[1])
        mean = np.mean(line_synapses)
        sd = np.std(line_synapses)
        sem = sd / sqrt_len

        writer.writerow([f"{time:.3f}", f"{mean:.10f}", f"{sd:.10f}", f"{sem:.10f}"])

print(f"{snakemake.wildcards['type']} Ending at: {datetime.now().strftime('%H:%M:%S')}")

# Close connections
for fp in fps:
    fp.close()
