import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ks_2samp
import itertools
from scipy.stats import gaussian_kde

colors = {
    "No TI": "tab:blue",
    "5 Hz": "tab:orange",
    "130 Hz": "tab:green",
    "0 Hz": "tab:red"
}

def expand_time(original, max_time = 10_000):
    original["Time"] = (original["Time"] / 0.025).round() * 0.025
    original = original.sort_values("Time")

    new_time = np.arange(0, max_time + 0.025, 0.025)

    expanded = pd.DataFrame({ "Time": new_time })
    expanded = pd.merge_asof(expanded, original, on = "Time", direction = "backward")

    return expanded

def read_frequency_weights():
    conditions = {
        "No TI": snakemake.input["weights"],
        "0 Hz": snakemake.input["weights_0"],
        "5 Hz": snakemake.input["weights_5"],
        "130 Hz": snakemake.input["weights_130"]
    }

    weights = {}
    average_weights = {}
    time = []
    for (condition, filename) in conditions.items():
        weights[condition] = []
        average_weights[condition] = []
        for file in conditions[condition]:
            synapse_weights = pd.read_csv(file, index_col = 0)
            synapse_weights = expand_time(synapse_weights)
            time = synapse_weights.Time.to_list()

            synapse_weights = np.array([ synapse_weights[f"Synapse{i}"] for i in range(0, 10) ])
            weights[condition].append(synapse_weights)

            synapse_weights = synapse_weights.mean(axis = 0)
            average_weights[condition].append(synapse_weights)

        weights[condition] = np.array(weights[condition])
        weights[condition] = weights[condition].reshape((weights[condition].shape[0] * weights[condition].shape[1], weights[condition].shape[2]))
        average_weights[condition] = np.array(average_weights[condition])

    return np.array(time) / 1000, weights, average_weights


time, weights, average_weights = read_frequency_weights()

fig, axs = plt.subplots(nrows = 1, ncols = 4, figsize = (16, 2), sharey = True)
axs = axs.flatten()

for i, condition in enumerate(average_weights.keys()):
    for synapse_weights in average_weights[condition]:
        # Each line corresponds to the average synaptic weight in each run
        axs[i].plot(
            time,
            synapse_weights,
            linewidth = 1,
            color = colors[condition],
            alpha = 0.25
        )

    # The line is the average of all synaptic weights from all synapses
    axs[i].plot(
        time,
        weights[condition].mean(axis = 0),
        linewidth = 2,
        color = colors[condition],
        alpha = 1
    )

    axs[i].set_ylim(-0.05, 1.05)
    axs[i].set_title(condition)

    axs[i].set_xlabel("Time, s")

axs[0].set_ylabel("Synaptic weight")

plt.savefig(snakemake.output["weight_dynamics"])


# Perform statistical testing (KS test) between all TI conditions and no TI

def p_to_star(p):
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "ns"

ks_result = []

# Perform statistical testing between all conditions
for (cond1, cond2) in itertools.combinations(weights.keys(), 2):
    res = ks_2samp(weights[cond1][:, -1], weights[cond2][:, -1])

    ks_result.append(pd.DataFrame({
        "Condition1": [cond1],
        "Condition2": [cond2],
        "Pvalue": [res.pvalue],
        "Statistic": [res.statistic * res.statistic_sign],
        "StatisticLocation": [res.statistic_location],
        "Star": [p_to_star(res.pvalue)]
    }))

# Concatenate all test results
ks_result = pd.concat(ks_result, ignore_index = True)


fig, axs = plt.subplots(nrows = 1, ncols = 2, figsize = (16, 4))
axs = axs.flatten()

################## Average of synaptic weights

for condition in weights.keys():
    average = np.array(weights[condition]).mean(axis = 0)
    error = weights[condition].std(axis = 0) / np.sqrt(weights[condition].shape[0])

    axs[0].plot(
        time,
        average,
        linewidth = 1,
        color = colors[condition],
        alpha = 1,
        label = condition
    )

    axs[0].fill_between(
        time, average - error, average + error,
        alpha = 0.25,
        color = colors[condition],
        edgecolor = None
    )

axs[0].grid(True, alpha = 0.25)
axs[0].set_xlabel("Time, s")
axs[0].set_ylim(-0.05, 0.65)
axs[0].set_ylabel("Synaptic weight")

################## Final synaptic weight distribution

for condition in weights.keys():
    final_weights = weights[condition][:, -1]

    sns.kdeplot(
        final_weights,
        bw_adjust = 1,
        ax = axs[1],
        clip = (0, 1),
        label = condition,
        fill = True,
        alpha = 0.025,
        linewidth = 0.75,
        color = colors[condition]
    )

    if condition == "No TI": continue

    test_result = ks_result[(ks_result.Condition1 == "No TI") & (ks_result.Condition2 == condition)]
    star = test_result.Star.to_list()[0]
    location = test_result.StatisticLocation.to_list()[0]

    kde = gaussian_kde(final_weights)
    where_y = kde(location)
    where_x = location

    axs[1].text(
        where_x, where_y,
        star,
        fontsize = 10,
        color = colors[condition],
        horizontalalignment = "center",
        verticalalignment = "bottom"
    )

axs[1].grid(True, alpha = 0.25)
axs[1].set_xticks(np.arange(0, 1 + 0.25, 0.25))
axs[1].set_ylim(0, 3)
axs[1].set_yticks(np.arange(0, 3, 1))
axs[1].set_xlabel("Synaptic weight")
sns.despine(ax = axs[1], top = True, right = True)

plt.title(f"{snakemake.wildcards['rate']} Hz")

plt.savefig(snakemake.output["summary"])
