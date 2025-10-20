#
# Determine subthreshold EF strength for the specified beat frequency and
# field orientation.
#
# No synapses present.
#

# Include path to neuron classes
import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd

from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
from neuron_utils import NeuronUtils


def get_dt(carrier):
    """
    Determines the optimal time step depending on the carrier frequency.
    :param carrier: Carrier frequency.
    :return: Optimal time step.
    """
    if carrier == 9000: return 0.0025
    if carrier == 5000: return 0.0025
    if carrier == 2000: return 0.025
    if carrier == 1000: return 0.025
    if carrier == 0: return 0.025

    print(f"Undefined dt for carrier {carrier}")
    return None


def get_duration(beat, duration, min_oscillations = 10):
    """
    Determines the optimal stimulation duration depending on the beat frequency
    and minimum required number of oscillations.
    :param beat: Beat frequency.
    :param duration: Minimum stimulation duration (ms).
    :param min_oscillations: Minimum number of beat frequency oscillations.
    :return: Optimal stimulation duration (ms).
    """
    oscillations_per_second = beat
    duration_seconds = duration / 1000

    n_oscillations = oscillations_per_second * duration_seconds

    if beat != 0 and n_oscillations < min_oscillations:
        return math.ceil(min_oscillations / oscillations_per_second * 1000 / 100) * 100
    else:
        return math.ceil(duration / 100) * 100


# Get snakemake parameters
phi = int(snakemake.wildcards["angle_phi"])
psi = int(snakemake.wildcards["angle_psi"])
carrier = int(snakemake.wildcards["carrier"])
beat = int(snakemake.wildcards["beat"])

phase = int(snakemake.params["phase"])
duration = int(snakemake.params["duration"])
initial_amplitude = int(snakemake.params["initial_amplitude"])
epsilon = float(snakemake.params["accuracy"])

dt = get_dt(carrier)

duration = get_duration(
    beat = beat,
    duration = duration,
    min_oscillations = 10
)

print("Creating neuron model")
neuron = PlasticNeuron(n_synapses = 0)

print(f"Estimating the subthreshold EF strength for carrier frequency {carrier} Hz with beat frequency {beat} Hz")

print(f"Using dt = {dt} ms")
print(f"Stimulation duration = {duration} ms")

print(f"Setting the orientation of the electric field to psi = {psi}° and phi = {phi}°")
NeuronUtils.set_field(phi_deg = phi, psi_deg = psi)

amplitude = initial_amplitude
amplitude_step = amplitude / 2
last_amplitude = initial_amplitude * 2
last_ap = True

while abs(last_amplitude - amplitude) > epsilon or last_ap:
    print(f"Testing {amplitude}")
    last_amplitude = amplitude

    NeuronUtils.set_stimulus(
        delay = 0,
        duration = duration,
        frequency1 = carrier,
        frequency2 = carrier + beat,
        amplitude = amplitude,
        phase = 0 if carrier == 0 else phase
    )

    neuron.run(
        duration = duration,
        dt = dt
    )

    last_ap = len(neuron.spike_times) > 0

    if last_ap:
        amplitude -= amplitude_step
    else:
        amplitude += amplitude_step

    amplitude_step = amplitude_step / 2

print(f"Estimated subthreshold EF strength for carrier frequency {carrier} Hz with "
      f"beat frequency {beat} Hz: {round(last_amplitude, 2)}.")

result = pd.DataFrame({
    "Psi": [psi],
    "Phi": [phi],
    "Carrier": [carrier],
    "Beat": [beat],
    "SubthresholdAmplitude": [amplitude],
    "SubthresholdAmplitudeStep": [amplitude_step],
    "LastAP": [last_ap]
})

result.to_csv(snakemake.output["subthreshold"], index = False)
