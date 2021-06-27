''' CHSH Strategies.'''

import numpy as np

def randomStrategy(sentBits: [int, int]) -> [int,int] : 
    ''' Randomly have you and your collaborator guess.'''
    
    # 'sentBits' contains the bit you and your collaborator received.
    if sentBits[0] == 0:
        yourResponse = np.random.randint(2)
    elif sentBits[0] == 1:
        yourResponse = np.random.randint(2) # Spelt out for clarity!
    
    # Now repeat for collaborator.
    if sentBits[1] == 0:
        collaboratorResponse = np.random.randint(2)
    elif sentBits[1] == 1:
        collaboratorResponse = np.random.randint(2)
    
    return (yourResponse,
            collaboratorResponse)


def fixedStrategy(sentBits: [int, int]) -> [int,int] : 
    ''' Always do the same action.'''
    
    # 'actions' contains the action of you and collaborator.
    if sentBits[0] == 0:
        yourResponse = 0
    elif sentBits[0] == 1:
        yourResponse = 0 # Spelt out for clarity!
    
    # Now repeat for collaborator.
    if sentBits[1] == 0:
        collaboratorResponse = 0
    elif sentBits[1] == 1:
        collaboratorResponse = 0
    
    return (yourResponse,
            collaboratorResponse)


def quantumStrategy(actions):
    ''' The quantum strategy.'''
    pass


