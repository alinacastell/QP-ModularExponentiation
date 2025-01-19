# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

# Code check 2-qubit addition
'''
A = [0, 1]           # 3 qubits for first number
B = [2, 3]           # 3 qubits for second number
AUX1 = [4, 5, 6, 7, 8, 9, 10]  # 7 auxiliary qubits
R = [11, 12]        # 3 qubits for result
n = len(A) + len(B) + len(R) + len(AUX1)
circuit = QuantumCircuit(n, 2)
print("\nAddition Circuit\n")
set_bits(circuit, R, [0,0,0])
set_bits(circuit, A, [0,1])
set_bits(circuit, B, [1,1])
add(circuit, A, B, R, AUX1)
circuit.barrier()
circuit.measure([AUX1[2], R[0]], [0, 1])
print_measures(circuit)
'''

# Test circuit with corrected initialization and measurement
# Code check 3-qubit subtraction
A = [0,1,2]
B = [3,4,5]
R = [6,7,8]
AUX = [9,10,11,12, 13, 14,15]
n = len(A) + len(B) + len(R) + len(AUX)
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, A, [1,0,0])
set_bits(circuit, B,[1,1,0])
subtract(circuit, A, B, R, AUX)
print("\nSubtraction Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)