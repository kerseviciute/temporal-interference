import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import polars as pl
from zipfile import ZipFile
mpl.rcParams["font.family"] = "Avenir"

print("Reading stimuli")
stimuli = pl.read_csv(snakemake.input["in_vivo"]).to_pandas()

synapse_idx = snakemake.wildcards["synapse_idx"]
synapse = f"Synapse{synapse_idx}"
print(f"Creating plot for synapse {synapse_idx}")

print("Reading No TI")

weights = pl.read_csv(snakemake.input["weights_no_ti"], columns = ["Time", synapse]).to_pandas()
time = weights.Time / 1000

synapse_voltage = pl.read_csv(snakemake.input["voltage_no_ti"], columns = ["Time", synapse]).to_pandas()

print("Reading 5 Hz TI")

weights_5 = pl.read_csv(snakemake.input["weights_ti_5"], columns = ["Time", synapse]).to_pandas()
time_5 = weights_5.Time / 1000

synapse_voltage_5 = pl.read_csv(snakemake.input["voltage_ti_5"], columns = ["Time", synapse]).to_pandas()

print("Reading 130 Hz TI")

weights_130 = pl.read_csv(snakemake.input["weights_ti_130"], columns = ["Time", synapse]).to_pandas()
time_130 = weights_130.Time / 1000

synapse_voltage_130 = pl.read_csv(snakemake.input["voltage_ti_130"], columns = ["Time", synapse]).to_pandas()

print("Reading 0 Hz TI")

weights_0 = pl.read_csv(snakemake.input["weights_ti_0"], columns = ["Time", synapse]).to_pandas()
time_0 = weights_0.Time / 1000

synapse_voltage_0 = pl.read_csv(snakemake.input["voltage_ti_0"], columns = ["Time", synapse]).to_pandas()

synapse_stimuli = (stimuli[f"{synapse_idx}"].dropna() / 1000).tolist()

synapse_weights_no_ti = weights[synapse]
synapse_weights_5 = weights_5[synapse]
synapse_weights_130 = weights_130[synapse]
synapse_weights_0 = weights_0[synapse]

voltage_no_ti = synapse_voltage[synapse]
voltage_130 = synapse_voltage[synapse]
voltage_5 = synapse_voltage_5[synapse]
voltage_0 = synapse_voltage_0[synapse]

fig, axs = plt.subplots(nrows = 6, ncols = 1, figsize = (12, 11), height_ratios = [0.1, 0.45, 0.45, 0.45, 0.45, 0.45], sharex = True)

### Synaptic input

ax = axs[0]

ax.eventplot(synapse_stimuli, lineoffsets = 0, linelengths = 0.75, colors = "black", linewidths = 0.5)
ax.set_yticks([])
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.grid(alpha = 0.25)

### Synaptic weights

ax = axs[1]

ax.plot(
    time,
    synapse_weights_no_ti,
    linewidth = 1,
    label = "No TI",
    color = "tab:blue"
)

ax.plot(
    time_5,
    synapse_weights_5,
    linewidth = 1,
    label = "5 Hz TI",
    color = "tab:orange"
)

ax.plot(
    time_130,
    synapse_weights_130,
    linewidth = 1,
    label = "130 Hz TI",
    color = "tab:green"
)

ax.plot(
    time_0,
    synapse_weights_0,
    linewidth = 1,
    label = "0 Hz TI",
    color = "tab:red"
)

ax.grid(alpha = 0.25)
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.set_ylim(-0.05, 1.05)
ax.set_ylabel("Synaptic weight")
ax.legend(
    loc = "center right",
    frameon = False,
    ncol = 1,
    bbox_to_anchor = (1.15, 0.5)
)

### Dendritic voltage

ax = axs[2]

ax.plot(
    synapse_voltage.Time / 1000,
    voltage_no_ti,
    linewidth = 0.5,
    color = "tab:blue"
)

ax.grid(alpha = 0.25)
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.set_ylim(-90, 50)
ax.set_yticks([-75, -50, -25, 0, 25])
ax.set_ylabel("Voltage, mV")

ax = axs[3]

ax.plot(
    synapse_voltage_5.Time / 1000,
    voltage_5,
    linewidth = 1,
    label = "5 Hz TI",
    color = "tab:orange"
)

ax.grid(alpha = 0.25)
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.set_ylim(-90, 50)
ax.set_yticks([-75, -50, -25, 0, 25])
ax.set_ylabel("Voltage, mV")

ax = axs[4]

ax.plot(
    synapse_voltage_130.Time / 1000,
    voltage_130,
    linewidth = 1,
    label = "130 Hz TI",
    color = "tab:green"
)

ax.grid(alpha = 0.25)
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.set_ylim(-90, 50)
ax.set_yticks([-75, -50, -25, 0, 25])
ax.set_ylabel("Voltage, mV")

ax = axs[5]

ax.plot(
    synapse_voltage_0.Time / 1000,
    voltage_0,
    linewidth = 1,
    label = "0 Hz TI",
    color = "tab:red"
)

ax.grid(alpha = 0.25)
ax.set_xlim(0, 630)
ax.set_xticks(np.arange(0, 630, 60))
ax.set_xlabel("Time, s")
ax.set_ylim(-90, 50)
ax.set_yticks([-75, -50, -25, 0, 25])
ax.set_ylabel("Voltage, mV")

axs[0].set_title(f"Synaptic configuration ID: {snakemake.wildcards['idx']}, Synapse {synapse_idx}")

plt.tight_layout()
plt.savefig(snakemake.output[f"png"], dpi = 500, bbox_inches = "tight")
