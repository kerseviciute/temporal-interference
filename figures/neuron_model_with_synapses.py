# Include path to neuron classes
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neuron import h
from abstract_neuron import AbstractNeuron
from plastic_neuron import PlasticNeuron
import plotly
import matplotlib
import plotly.graph_objects as go

neuron = PlasticNeuron(n_synapses = 10)

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

for synapse in neuron.synapses:
    dendrite = synapse.dendrite
    position = synapse.position

    i = int(h.apical_dendrite[dendrite].n3d() * position)
    x = h.apical_dendrite[dendrite].x3d(i)
    y = h.apical_dendrite[dendrite].y3d(i)
    z = h.apical_dendrite[dendrite].z3d(i)

    fig.add_trace(
        go.Scatter3d(
            x = [x],
            y = [y],
            z = [z],
            marker = dict(
                color = "red",
                size = 5
            )
        )
    )

fig.write_image(snakemake.output["png"], width = 1920, height = 1080, scale = 1)
