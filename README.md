# Readme
This script creates an ensemble of neurons. The amount of Neurons is dependent on the value of AMOUNT_OF_NEURONS. 
The Neurons in this ensemble have random tuning-curves if RANDOM_TUNING_CURVES == True. If RANDOM_TUNING_CURVES == false,
the tuning-curves are symmetrical to x = 0 (spike-behavior is inverted).
The created ensemble then is simulated for 1 second and plots of the ensemble's neurons' tuning-curves, spike behavior and filtered output are created.
