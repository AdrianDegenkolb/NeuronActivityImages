# Readme
This script simulates an ensemble of spiking-neurons for 1 second and plots the ensemble's neurons' tuning-curves, spike behavior and filtered output.
The amount of Neurons is set by the argument -n or --neurons. 
If the variable RANDOM_TUNING_CURVES == false, the neurons' tuning-curves are symmetrical to x = 0 (spike-behavior is inverted). This only works for ensembles of 2 Neurons. The neurons' tuning-curves will be initialized randomly if RANDOM_TUNING_CURVES == True. 

