# following code was written using a tutorial on https://www.nengo.ai/nengo/examples/basic/single-neuron.html
# and information retrieved from https://www.w3schools.com/python/matplotlib_pyplot.asp

import matplotlib.pyplot as plt
import numpy as np

import nengo
from nengo.utils.matplotlib import rasterplot

from nengo.dists import Uniform

model = nengo.Network(label="One Neuron")
with model:
    neurons = nengo.Ensemble(1, dimensions=1, intercepts=Uniform(-0.5, -0.5), max_rates=Uniform(100, 100), encoders=[[1]])
    cos = nengo.Node(lambda t: np.cos(8 * t))
    # Connect the input signal to the neuron
    nengo.Connection(cos, neurons)
    # The original input
    cos_probe = nengo.Probe(cos)
    # The raw spikes from the neuron
    spikes = nengo.Probe(neurons.neurons)
    # Spikes filtered by a 10ms post-synaptic filter
    filtered = nengo.Probe(neurons, synapse=0.01)

# run the simulation for one second
with nengo.Simulator(model) as sim:
    sim.run(1)

# Plot the decoded output of the ensemble
plt.figure()
plt.plot(sim.trange(), sim.data[filtered])
plt.plot(sim.trange(), sim.data[cos_probe])
plt.ylabel("Signal")
plt.xlabel("Time")
plt.xlim(0, 1)

# Plot the spiking output of the ensemble
plt.figure(figsize=(10, 8))
plt.subplot(221)
rasterplot(sim.trange(), sim.data[spikes])
plt.ylabel("Neuron")
plt.xlabel("Time of Spike-Occurrence")
plt.xlim(0, 1)
plt.show()
