''' This module implements a basic quantum simulator. '''

import qubit

class QuantumComputer():
    ''' A simulation for a quantum computer. This class keeps a record
        of the qubits that have been created and invokes operations on 
        qubits. '''


    def __init__(self, nQubits: int):
        ''' Initialises the quantum computer. '''
        
        # Create an empty list of qubits that are allocated.
        self.qubits = [qubit.Qubit() for q in range(nQubits)]


    def getQubit(self) -> qubit.Qubit:
        ''' Returns a qubit if available. '''

        if self.qubits:
            return self.qubits.pop()
            
        else:
            raise RuntimeError('No Qubits available - allocate a qubit on the quantum computer.')

