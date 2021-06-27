''' Implementation of BB84 Quantum Key Distribution Simulation. '''

from collections import Counter
import constants
import quantumSimulator as qs
import queue
import threading

'''
 The BB84 QKD algorithm has the following steps:
Alice is distributing the key to Bob.d

Define a holder for the key.

ALICES HARDWARE
- Get access to a Qubit.

- Generate a classical bit with a QRNG.
- Generate a basis with a QRNG.
- Prepare message using state and basis.

BOBS HARDWARE
- Get access to a Qubit.

- Generate a classical bit with a QRNG.
- Measure message basis.

ALICE AND BOB CHECK BASIS AGREES OVER CLASSICAL CHANNEL.
If yes append to key.

'''

def runAlice(quantumQueue: queue.Queue, 
             conventionalQueue: queue.Queue):
    ''' This controls Alice's behaviour for BB48'''

    # Create an empty key that we wish to fill up to 128 bits long.
    key = []
    nBits = 1024

    # Initialse the quantum computer with one qubit.
    quantDevice = qs.QuantumComputer(1)

    # Get a qubit from the device.
    qubit = quantDevice.getQubit()

    # Now build up the key. Note how many attempts given.
    nTries = 0
    while len(key) < nBits:

        # Get a random bit that will be an element of the key.
        bit = qubit.randGen()

        # Choose a random basis. This will help determine what we send.
        basis = qubit.randGen()

        # Create the qubit to send based on bit and basis.
        # If the key bit is 1 then we need to convert our qubit that we send
        # from default |0> state to |1>. 
        if bit == True:
            qubit.x()
        # If the basis is 1 then we measure on along 'x' axis so need to apply
        # Hadamard operation (instad of along 'z' axis which is |0> to |1> axis.
        if basis == True:
            qubit.hadamard()

        # Now send this qubit. Simulation will pass the object by reference.
        # This is deliberate (instead of using multiprocessing.Queue that would
        # make a copy). So if anybody tries to clone or measure it we would 
        # find out. 
        quantumQueue.put(qubit)

        # Check on the conventional authenticated channel if the basis agrees
        # with what was sent. Store the key if yes.
        bobBasis = conventionalQueue.get()
        
        if bobBasis == basis:
            key.append(bit)

        # Increment the counter.
        nTries += 1

    hexKey = hex(int("".join([str(int(bit)) for bit in key]) ,2 ))[2:] 
    print("The secret key that both parties now have is:\n{}".format(hexKey) )

    # Close the quantum queue down with poison pill.
    quantumQueue.put("COMPLETE")

    # Write the secret key to disk.
    f = open("SecretKey.txt", "w")
    f.write(hexKey)


def runBob(quantumQueue: queue.Queue, 
           conventionalQueue: queue.Queue):
    ''' This controls Bob's behaviour for BB48. It will terminate
        when a full key has been received.'''

    # Create a holder for Bobs secret key.
    key = []

    # Initialse the quantum computer with one qubit.
    quantDevice = qs.QuantumComputer(1)

    # Get a qubit that we will use for a rng to choose a basis to measure.
    basisQubit = quantDevice.getQubit()
    
    # Iterate while building the key.
    while True:

        # Choose the basis to measure qubit in randomly.
        basis = basisQubit.randGen()

        # Wait for a qubit on the quantum queue. NB this has been passed by 
        # reference as closer to real world (so must get sequencing right).
        qubit = quantumQueue.get()

        # Check if we have a complete key.
        if qubit == "COMPLETE":

            # Now return from thread as finished.
            return

        # Measure this on our basis. If the basis is 1 then use the X axis 
        # else use the Z axis (|0> to |1> axis).
        if basis == True:
            qubit.hadamard()
        potentialKeyBit = qubit.measure()

        # Now reset the qubit to |0> as not needed so Alice can re-use.
        qubit.reset()

        # Now send the over the conventional authenticated channel the basis used.
        # If it agrees with Alice then keep the key. NB that because both Alice and
        # Bob are randomly selecting the basis it won't always agree. This randomness
        # is used incase an eaves dropper is on the line and clones the qubit. Also
        # note this would normally be two way channel but just send back to Alice
        # here for ease.
        conventionalQueue.put(basis) # bool so passed by value.


def keyExchange():
    ''' Sets up the respective players in the key exchange.
        Alice will send the key to Bob. They will exchange the
        key over a quantum channel (simulated fibre optic). They
        will confirm the key by looking at the basis over a 
        conventional comms channel (authentication is just assumed).
    '''
    
    # Create a thread safe quantum channel queue.
    quantumChannel = queue.Queue()
    
    # Create a thread safe convential channel queue.
    conventionalChannel = queue.Queue()
    
    # Setup the Alice thread.
    aliceThread = threading.Thread(target=runAlice, args=(quantumChannel,
                                                          conventionalChannel,))
    aliceThread.start()
    
    # Setup the Bob thread.
    bobThread = threading.Thread(target=runBob,
                                 args=(quantumChannel,
                                       conventionalChannel,))
    bobThread.start()
    
    # Now wait for the algorithm to complete.
    aliceThread.join()
    bobThread.join()


def main():
    ''' Simple program that creates a thread for Bob and Alice to illustrate the BB84
    key exchange algorithm.'''
    
    # Undertake the key exchange. This also writes out the secret key to a text
    # file for illustration purposes. That key would normally be held secretly 
    # by Bob and Alice. The algorithm ensures that they can build this key separately
    # by just exchanging basis of which the qubits were prepared and measured.
    keyExchange()


if __name__ == "__main__":
    # Run the example.
    main()

