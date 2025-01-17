# Subtraction

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

def subtract(circuit, A, B, R, AUX):
    '''
    Subtracts number(A) and number(B).
    '''
    # Negate each bit of B
    for b in B:
        circuit.x(b)
    # Initialize carry-in bit to 1
    circuit.x(AUX[0])
    add(circuit, A, B, R, AUX)
    # Reset carry-in bit to 0
    circuit.x(AUX[0])

# Code check subtraction
A = [0,1,2]
B = [3,4,5]
R = [6,7,8]
AUX = [9,10,11,12, 13, 14,15,16]
n = len(A) + len(B) + len(R) + len(AUX) + 4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, [A, B], [[1,0,0],[1,1,0]])
subtract(circuit, A, B, R, AUX)
print("\nSubtraction Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)