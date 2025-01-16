from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

# Initialization
def set_bits(circuit, A, X):
    '''
    Initialize bits of register A with binary string X.
    '''
    n = len(A)
    for i in range(len(X)):
        if X[i] == 1:
            # Apply X-gate
            circuit.x(A[i])

# Code check initialization
A = [0,1,2]
X = [1,1,0]
n = len(A)
circuit = QuantumCircuit(n,n)
set_bits(circuit, A, X)
print("\nInitialization Circuit\n")
circuit.barrier()
circuit.measure(A, [0,1,2])
print_measures(circuit)