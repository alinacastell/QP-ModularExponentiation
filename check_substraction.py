# Full Adder

from functions import subtract, set_bits
from utils import print_measures
from qiskit import QuantumCircuit

# Code check full adder
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