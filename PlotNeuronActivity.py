# following code was written using tutorials on https://www.nengo.ai/nengo/examples/basic/single-neuron.html and
# https://www.nengo.ai/nengo/examples/usage/tuning-curves.html
# and information retrieved from https://www.w3schools.com/python/matplotlib_pyplot.asp
import getopt
import sys

import matplotlib.pyplot as plt
import numpy as np
import nengo
from nengo.utils.matplotlib import rasterplot
from nengo.dists import Uniform
from nengo.utils.ensemble import tuning_curves


def create_model(size, random_tuning_curves):
    names = ["One Neuron", "Two Neurons", "N Neurons"]
    encoders = [[[1]], [[1], [-1]], [[1], [-1]]]
    if size >= len(names):
        index = len(names) - 1
    else:
        index = size - 1

    model = nengo.Network(label=names[index])
    with model:
        if random_tuning_curves:
            neurons = nengo.Ensemble(size, dimensions=1)
        else:
            neurons = nengo.Ensemble(size, dimensions=1, intercepts=Uniform(-0.5, -0.5), max_rates=Uniform(100, 100),
                                     encoders=encoders[index])

        cos = nengo.Node(lambda t: np.cos(8 * t))
        # Connect the input signal to the neuron
        nengo.Connection(cos, neurons)
        # The original input
        cos_probe_ = nengo.Probe(cos)
        # The raw spikes from the neuron
        spikes = nengo.Probe(neurons.neurons)
        # Spikes filtered by a 10ms post-synaptic filter
        filtered = nengo.Probe(neurons, synapse=0.01)

    return model, neurons, cos_probe_, spikes, filtered


def plot(model, neurons, cos_probe, spikes, filtered):
    # run the simulation for one second
    with nengo.Simulator(model) as sim:
        eval_points, activities = tuning_curves(neurons, sim)
        sim.run(1)
    # Plot tuning-curves
    plt.figure()
    plt.plot(eval_points, activities)
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
    plt.figure()
    rasterplot(sim.trange(), sim.data[spikes])
    plt.ylabel("Neuron")
    plt.xlabel("Time of Spike-Occurrence")
    plt.xlim(0, 1)
    plt.show()


def main():
    model, neurons, cos_probe, spikes, filtered = create_model(AMOUNT_OF_NEURONS, RANDOM_TUNING_CURVES)
    plot(model, neurons, cos_probe, spikes, filtered)


AMOUNT_OF_NEURONS = 0
RANDOM_TUNING_CURVES = True
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:", ["neurons="])
except getopt.GetoptError:
    print('argument: -n <number_of_neurons>')
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-n", "--neurons"):
        AMOUNT_OF_NEURONS = int(arg)
main()
