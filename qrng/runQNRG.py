''' Implementation of Quantum Random Number Generator Simulator. '''

import constants
import quantumSimulator as qs


# Repeat the experiment 10000 times and plot to show that we get a uniform distribution.
n0 = 0 # Create a note of how many observed in |0>.
n1 = 0 # Create a note of how many observed in |1>.
for i in range(10000):
    # Initialse the quantum computer with one qubit.
    quantDevice = qs.QuantumComputer(1)

    # Get a qubit from the device.
    qubit = quantDevice.getQubit()

    # Apply Hadamard operation to qubit.
    qubit.hadamard()

    # Measure the qubit.
    measState = qubit.measure()

    # Record simulation results to check measurement.
    if measState == True:
        n0 +=1
    else:
        n1 +=1

print("Number found in |0> state is {}, and number found in |1> state is {}".format(n0,n1))
print("Probability of state |0> is {}".format(n0/(n0+n1)))

