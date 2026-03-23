#
# Determine subthreshold EF strength.
# No synapses present.
#

# Include path to neuron classes
import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils


def get_dt(carrier):
    if carrier == 9000: return 0.0025
    if carrier == 5000: return 0.0025
    if carrier == 2000: return 0.025
    if carrier == 1000: return 0.025
    if carrier == 0: return 0.025

    print(f"Undefined dt for carrier {carrier}")
    return None


def get_duration(beat, duration, min_oscillations = 10):
    oscillations_per_second = beat
    duration_seconds = duration / 1000

    n_oscillations = oscillations_per_second * duration_seconds

    if beat != 0 and n_oscillations < min_oscillations:
        return math.ceil(min_oscillations / oscillations_per_second * 1000 / 100) * 100
    else:
        return math.ceil(duration / 100) * 100


def find_ef_amplitude(carrier, target, dt, initial_amplitude = 1000, epsilon: float = 1, duration = 100, phase = 10):
    amplitude = initial_amplitude
    amplitude_step = amplitude / 2
    last_amplitude = initial_amplitude * 2
    last_ap = True

    adjusted_duration = get_duration(
        beat = target,
        duration = duration,
        min_oscillations = 10
    )

    while abs(last_amplitude - amplitude) > epsilon or last_ap:
        print(f"Testing {amplitude}")
        last_amplitude = amplitude

        NeuronUtils.set_stimulus(
            delay = 0,
            duration = adjusted_duration,
            frequency1 = carrier,
            frequency2 = carrier + target,
            amplitude = amplitude,
            phase = 0 if carrier == 0 else phase
        )
        neuron.run(
            duration = adjusted_duration,
            dt = dt
        )

        last_ap = len(neuron.spike_times) > 0

        if last_ap:
            amplitude -= amplitude_step
        else:
            amplitude += amplitude_step

        amplitude_step = amplitude_step / 2

    print(f"Sub-threshold amplitude for carrier {carrier} with target {target}: {last_amplitude}")
    return last_amplitude


phi = int(snakemake.wildcards["angle_phi"])
psi = int(snakemake.wildcards["angle_psi"])
carrier = int(snakemake.wildcards["carrier"])
offsets = list(map(float, snakemake.params["offset_range"]))
phase = int(snakemake.params["phase"])
duration = int(snakemake.params["duration"])
initial_amplitude = int(snakemake.params["initial_amplitude"])
epsilon = float(snakemake.params["accuracy"])

dt = get_dt(carrier)

# Make sure offset 0 and target 0 are not tested
if carrier == 0 and 0 in offsets:
    offsets.remove(0)

print("Creating neuron model")
neuron = PlasticNeuron(n_synapses = 0)

print(f"Setting the orientation of the electric field to psi = {psi} and phi = {phi}")
NeuronUtils.set_field(phi_deg = phi, psi_deg = psi)

print(f"Using dt = {dt}")

res = []
for offset in offsets:
    print(f"Starting carrier {carrier} with target {offset}")
    amplitude = find_ef_amplitude(
        carrier, offset,
        initial_amplitude = initial_amplitude,
        epsilon = epsilon,
        duration = duration,
        phase = phase,
        dt = dt
    )

    res.append(pd.DataFrame({
        "Offset": [offset],
        "Amplitude": [amplitude]
    }))

res = pd.concat(res, ignore_index = True)
res.to_csv(snakemake.output["subthreshold"], index = False)
