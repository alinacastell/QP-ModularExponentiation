# Copy

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

def copy(circuit, A, B):
    '''
    Copy the binary string of A to the register B.
    '''
    for a, b in zip(A, B):
        # Apply CNOT gate
        circuit.cx(a, b)

# Code check copy
A = [0,1,2]
B = [3,4,5]
n = len(A) + len(B)
circuit = QuantumCircuit(n,3)
set_bits(circuit, A, [1,1,0])
set_bits(circuit, B, [0,0,0])
copy(circuit, A, B)
print("\nCopy Circuit\n")
circuit.barrier()
circuit.measure(B, [0,1,2])
print_measures(circuit)