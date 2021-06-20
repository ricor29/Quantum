''' This module implements a simulation of a Qubit and the operations on it. '''

import constants
import numpy as np

class Qubit():
    ''' The operations and modelling of a qubit. '''

    def __init__(self):
        ''' All Qubit's will start in a |0> state. This function
            initialises this for the class.'''

        # Create the kubit with ket state 0.
        self.s = constants.getK0()


    def measure(self) -> bool:
        ''' Measures the qubit to find probability (NB THIS IS SIMULATED). '''

        # First determine the probability of the qubit by measuring it's state.
        # We are measuring against the <0| state.
        prob = np.abs(self.s[0]) **2

        # Now do the cheat simulation as we don't have a quantum computer.
        if np.random.random() < prob:
            return bool(1)
        else:
            return bool(0)


    def x(self):
        ''' Quantum Not operation. '''
        
        # Matrix multiply the not operator on the state.
        self.s = constants.getX() @ self.s


    def hadamard(self):
        ''' Apply hadamard operator. '''

        # Matrix multiply the Hadamard operator on the state.
        self.s = constants.getH() @ self.s


    def randGen(self):
        ''' Get a random number from the qubit.'''
        
        # Put a qubit into known state.
        self.s = constants.getK0()
        
        # Apply Hadamard operation to qubit to put into 50/50 state.
        self.hadamard()

        # Measure the qubit.
        measState = self.measure()

        # Put the qubit back to known state.
        self.reset()
        
        return measState


    def reset(self):
        ''' Put the qubit into a known |0> state.'''
    
        # Put the qubit back to known state.
        self.s = constants.getK0()


