import csv
import numpy as np
from datetime import datetime

files = snakemake.input["weights"]
output = snakemake.output["mean_weight"]

print("Creating CSV readers")
fps = [open(file, "r") for file in files]
readers = [csv.reader(fp, delimiter = ",") for fp in fps]

# 10 synapses per file
n_synapses = len(readers) * 10

print(f"Number of synapses: {n_synapses}")

# Read and ignore the headers
for reader in readers:
    header = next(reader)

print("Ignored header row")

line_counter = 0

print(f"Starting at: {datetime.now().strftime('%H:%M:%S')}")

with open(str(output), "w") as fout:
    writer = csv.writer(fout)
    writer.writerow(["Time", "Mean"])

    # Calculate the sum for each line
    for reader_rows in zip(*readers):
        line_counter += 1

        if line_counter % 100_000 == 0:
            print(f"Line {line_counter} at {datetime.now().strftime('%H:%M:%S')}")

        line_sum = 0
        for values in reader_rows:
            line_sum += np.sum([float(val) for val in values[2:]])

        mean = line_sum / n_synapses
        time = float(values[1])

        writer.writerow([f"{time:.3f}", f"{mean:.10f}"])

# Close connections
for fp in fps:
    fp.close()
