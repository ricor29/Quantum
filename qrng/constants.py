''' Define constants that will be used such as |0> state and Hadamard operators. '''

import numpy as np

def defineConst() -> dict:

    # |0>
    K0 = np.array([ [1], [0]], dtype=complex)
    
    # |1>
    K1 = np.array([ [0], [1]], dtype=complex)
    
    # Hadamard operator (to convert state |0> to |+>).
    H = np.array([ [1,1],
                   [1,-1]], dtype=complex) / np.sqrt(2)

    return {'K0':K0, 'K1':K1, 'H':H}

_CONST = defineConst()

def getK0() -> np.array:

    return _CONST['K0'].copy()


def getK1() -> np.array:

    return _CONST['K1'].copy()


def getH() -> np.array:

    return _CONST['H'].copy()
