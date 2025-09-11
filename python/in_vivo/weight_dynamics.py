import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["font.family"] = "Avenir"

weights = pd.read_csv(snakemake.input["no_ti"], index_col = 0)
time = weights.Time / 1000
weights.drop("Time", axis = 1, inplace = True)
mean_weights = weights.mean(axis = 1)

weights_5 = pd.read_csv(snakemake.input["ti_5"], index_col = 0)
time_5 = weights_5.Time / 1000
weights_5.drop("Time", axis = 1, inplace = True)
mean_weights_5 = weights_5.mean(axis = 1)

weights_130 = pd.read_csv(snakemake.input["ti_130"], index_col = 0)
time_130 = weights_130.Time / 1000
weights_130.drop("Time", axis = 1, inplace = True)
mean_weights_130 = weights_130.mean(axis = 1)

weights_0 = pd.read_csv(snakemake.input["ti_0"], index_col = 0)

time_0 = weights_0.Time / 1000
weights_0.drop("Time", axis = 1, inplace = True)
mean_weights_0 = weights_0.mean(axis = 1)


plt.figure(figsize = (8, 3))

plt.plot(
    time,
    mean_weights,
    linewidth = 1,
    label = "No TI",
    color = "tab:blue"
)

plt.plot(
    time_5,
    mean_weights_5,
    linewidth = 1,
    label = "5 Hz TI",
    color = "tab:orange"
)

plt.plot(
    time_130,
    mean_weights_130,
    linewidth = 1,
    label = "130 Hz TI",
    color = "tab:green"
)

plt.plot(
    time_0,
    mean_weights_0,
    linewidth = 1,
    label = "0 Hz TI",
    color = "tab:red"
)

plt.grid(alpha = 0.25)
plt.xlim(0, 630)
plt.xticks(np.arange(0, 630, 60))
plt.xlabel("Time, s")
plt.ylim(-0.05, 0.55)
plt.ylabel("Synaptic weight")
plt.legend(
    loc = "center right",
    frameon = False,
    ncol = 1,
    bbox_to_anchor = (1.2, 0.5)
)

plt.title(f"Synaptic configuration ID: {snakemake.wildcards['idx']}")

plt.savefig(snakemake.output["png"], dpi = 500, bbox_inches = "tight")
