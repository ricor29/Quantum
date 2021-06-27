''' Implementation of CHSH game. '''

from collections import Counter
from typing import Callable

import constants
import numpy as np
import quantumSimulator as qs
import strategies as strat

'''
The CHSH game is an interesting one as a Quantum solution can outperform
a non-quantum one due to entanglement. The rules for the game are:

1) A third party randomly sends one bit (0 or 1) to you and your cooperator. 
Each individual bit is randomly chosen. Let bit 'x' be the bit sent to you, and
bit 'y' be the bet sent to your cooperator.

2) While not being able to communicate with your cooperator you must both send
back a bit to the third party. Let bit 'xr' be your reply and 'yr' be your
cooperators reply. The goal is for you and your cooperator to satsify this condition

x && y = xr XOR yr

NB you cant talk to your cooperator but you can pre-agree a strategy.

'''

def game(strategy: Callable[[list],list]) -> bool :
    ''' One iteration of the CHSM game.'''

    # Let player 1's bit sent from third party be:
    x = np.random.randint(2)
    
    # Let player 2's bit sent from third party by:
    y = np.random.randint(2)
  
    # Have player 1 and 2 implement their pre-defined strategy.
    # Although same function call they don't know about each other's
    # result.
    actions = strategy([x,y])

    # Determine the result.
    if (x & y) == (actions[0] ^ actions[1]):
        return True
    else:
        return False


def main():
    ''' Setup the quantum strategy and run the game multiple times.'''
    
    # Call the classical fixed strategy 1000 times to get an expectation value.
    nRuns = 1000
    avg = sum([ int(game(strat.fixedStrategy)) for i in range(nRuns)])/nRuns
    print("With a fixed strategy of both going for 0: {}".format(avg))
    
    avg = sum([ int(game(strat.randomStrategy)) for i in range(nRuns)])/nRuns
    print("With a random strategy for both: {}".format(avg))
    
    # Call the quantum strategy 1000 times to get an expectation value.
    
    
    

if __name__ == "__main__":
    # Run the example.
    main()

