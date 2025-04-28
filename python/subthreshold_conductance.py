# Include path to neuron classes
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils

duration = int(snakemake.params["duration"])
ltp_start = int(snakemake.params["ltp_start"])
ltp_duration = int(snakemake.params["ltp_duration"])
ltp_frequency = int(snakemake.params["ltp_frequency"])

seeds = pd.read_csv(snakemake.input["seeds"])
seed_idx = int(snakemake.wildcards["idx"])
seed = int(seeds.iloc[seed_idx].Seed)
print(f"{seed_idx}: Initializing neuron with random synapses")

n_synapses = int(snakemake.params["n_synapses"])
initial_weight = float(snakemake.params["initial_weight"])
min_conductance = float(snakemake.params["min_conductance"])
max_conductance = float(snakemake.params["max_conductance"])
epsilon = float(snakemake.params["epsilon"])
min_dendritic_spikes = float(snakemake.params["min_dendritic_spikes"])

test_stimulus_1, test_stimulus_2 = [
    int(stimulus_time) for stimulus_time in snakemake.params["test_stim_times"]
]

time_before = 50
time_after = 100


def find_conductance(
        min_conductance = 0.00005,
        max_conductance = 0.00015,
        epsilon: float = 0.00001,
        min_dendritic_spikes = 0.2
):
    global duration
    global ltp_start, ltp_duration
    global test_stimulus_1, test_stimulus_2
    global time_before, time_after

    # Turn off the stimulation
    NeuronUtils.set_stimulus(duration = 0)

    # Start with the average conductance value
    conductance = (min_conductance + max_conductance) / 2
    step = (max_conductance - min_conductance) / 2

    good_behavior = False
    last_conductance = conductance

    results = []

    while step * 2 > epsilon or not good_behavior:
        print(f"Testing conductance: {format(conductance, '.8f')}")
        last_conductance = conductance

        neuron.set_initial_conductance(conductance)
        neuron.run(duration = duration)

        spike_before = np.any(
            neuron.voltage[np.logical_and(neuron.time > test_stimulus_1 - time_before, neuron.time < test_stimulus_1 + time_after)] > -20
        )
        spike_after = np.any(
            neuron.voltage[np.logical_and(neuron.time > test_stimulus_2 - time_before, neuron.time < test_stimulus_2 + time_after)] > -20
        )

        ltp_time = np.logical_and(neuron.time > ltp_start, neuron.time < ltp_start + ltp_duration)
        spike_during = np.any(
            neuron.voltage[ltp_time] > -20
        )
        dendritic_spikes = np.mean([ np.any(synapse.voltage[ ltp_time ] > -20) for synapse in neuron.synapses ])

        print(f"Spike before: {spike_before} (False)")
        print(f"Spike after: {spike_after} (False)")
        print(f"Spike during: {spike_during} (True)")
        print(f"Percentage of dendritic spikes: {round(dendritic_spikes * 100)}%")

        good_behavior = not spike_before and not spike_after and dendritic_spikes >= min_dendritic_spikes

        results.append(pd.DataFrame({
            "Conductance": [conductance],
            "SpikeBefore": [spike_before],
            "SpikeAfter": [spike_after],
            "SpikeDuring": [spike_during],
            "DendriticSpikes": [dendritic_spikes],
            "Correct": [good_behavior],
            "Step": [step]
        }))

        if spike_before or spike_after:
            conductance -= step
        if dendritic_spikes < min_dendritic_spikes:
            conductance += step

        print(f"Correct behavior: {good_behavior} (True)")
        print()

        if good_behavior:
            print("Correct behavior achieved")
            break

        step = step / 2

    results = pd.concat(results, ignore_index = True)

    print(f"Final conductance: {format(last_conductance, '.8f')}")
    return last_conductance, results


def generate_ltp_spike_times():
    """Generate Poisson-distributed spike times."""
    spikes = []
    t = test_stimulus_1
    spikes.append(t)

    t = ltp_start
    while t < ltp_start + ltp_duration:
        spikes.append(t)
        isi = int(1000 / ltp_frequency)
        t += isi

    t = test_stimulus_2
    spikes.append(t)

    return spikes


# Define the stimulus
def ltp_stimulus():
    # Generate spike times
    spike_times = generate_ltp_spike_times()

    spike_vec = h.Vector(spike_times)
    stimulus = h.VecStim()
    stimulus.play(spike_vec)

    return stimulus


neuron = PlasticNeuron(
    n_synapses = n_synapses,
    seed = seed,
    initial_conductance = 0,
    initial_weight = initial_weight,
    generate_stimulus = ltp_stimulus
)

conductance, results = find_conductance(
    min_conductance = min_conductance,
    max_conductance = max_conductance,
    epsilon = epsilon
)

with open(snakemake.output["subthreshold_conductance"], "w") as f:
    f.write(str(conductance))

results.to_csv(snakemake.output["results"], index = False)
