# Include path to neuron classes
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
import plotly
import matplotlib

neuron = PlasticNeuron(n_synapses = 0)

neuron_sections = h.SectionList([
    sec for sec in h.allsec() if "sElec" not in str(sec) and "sField" not in str(sec)
])

ps = h.PlotShape(neuron_sections, False)
ps.show(1)

fig = ps.plot(plotly, cmap = matplotlib.colormaps["inferno"])

fig.update_layout(
    scene = dict(
        xaxis_title = "",
        yaxis_title = "",
        zaxis_title = "",
        xaxis = dict(showbackground = False, showticklabels = False),
        yaxis = dict(showbackground = False, showticklabels = False),
        zaxis = dict(showbackground = False, showticklabels = False),
        camera = dict(
            eye = dict(x = 2, y = 0, z = 1)
        )
    )
)

fig.write_image(snakemake.output["png"], width = 1920, height = 1080, scale = 1)
