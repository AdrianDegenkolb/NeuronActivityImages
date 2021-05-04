# following code was written using tutorials on https://www.nengo.ai/nengo/examples/basic/single-neuron.html and
# https://www.nengo.ai/nengo/examples/usage/tuning-curves.html
# and information retrieved from https://www.w3schools.com/python/matplotlib_pyplot.asp

import matplotlib.pyplot as plt
import numpy as np
import nengo
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform
from nengo.utils.ensemble import tuning_curves

model = nengo.Network(label="Two Neuron")
with model:
    neurons = nengo.Ensemble(2, dimensions=1, intercepts=Uniform(-0.5, -0.5), max_rates=Uniform(100, 100), encoders=[[1], [-1]])
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
    eval_points, activities = tuning_curves(neurons, sim)
    sim.run(1)

plt.figure()
plt.plot(eval_points, activities)
# We could have alternatively shortened this to
# plt.plot(*tuning_curves(ens_1d, sim))
plt.ylabel("Firing rate (Hz)")
plt.xlabel("Input scalar, x")

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
