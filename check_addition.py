# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

from qiskit import QuantumCircuit

# Code check addition
A = [0,1,2]
B = [3,4,5]
R = [6,7,8] # measure output register
AUX = [9,10,11,12, 13, 14, 15, 16]
n = len(A) + len(B) + len(R) + len(AUX) +4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, [A, B], [[0,0,1],[0,1,1]])
add(circuit, A, B, R, AUX)
print("\nAddition Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)