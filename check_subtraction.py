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
    #circuit.x(AUX[0])

# Code check 2-qubit subtraction
'''
A = [0,1]
B = [2,3]
AUX = [4,5,6,9,10,11]
R = [7,8]
n = len(A) + len(B) + len(R) + len(AUX)
circuit = QuantumCircuit(n, 3)
print("\nSubtraction Circuit\n")
print("A = [a0,a1] = [1,1] // B = [b0,b1] = [1,0]\n")
set_bits(circuit, R, [0,0,0])
set_bits(circuit, A, [1,1])
set_bits(circuit, B, [1,1])
subtract(circuit, A, B, R, AUX)
circuit.barrier()
circuit.measure([AUX[2],R[1],R[0]], [0,1,2])
print_measures(circuit)
'''
# Code check 3-qubit subtraction

A = [0,1,2]
B = [3,4,5]
R = [6,7,8]
AUX = [9,10,11,12, 13, 14,15]
n = len(A) + len(B) + len(R) + len(AUX) + 4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, A, [1,0,0])
set_bits(circuit, B,[1,1,0])
subtract(circuit, A, B, R, AUX)
print("\nSubtraction Circuit\n")
print("A = [a0,a1,a2] = [1,0,0] // B = [b0,b1,b2] = [1,1,0]\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)
