# Measure and check correct function implementation

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit
import numpy as np

# Code check initialization
A = [0,1,2,3,4]
X = "01011"
n = len(A)
circuit = QuantumCircuit(n)
circuit.x(A[2])
set_bits(circuit, A, X)
print("\nInitialization Circuit\n")
print(circuit)

# Code check copy
A = [2,4,3]
B = [1,0,5]
n = len(A) + len(B)
circuit = QuantumCircuit(n,2)
circuit.x(A[0]) # Initialize qubits for testing
copy(circuit, A, B)
print("\nCopy Circuit\n")
print_measures(circuit, A[2], B[2])

# Code check full adder
a = 0
b = 1
c_in = 3
c_out = 4
r = 5
AUX = 6
n = AUX+1
circuit = QuantumCircuit(n,2)
full_adder(circuit, a, b, r, c_in, c_out, AUX)
print("\nFull Adder Circuit\n")
print_measures(circuit, r, c_out)

# Code check addition
A = [0,1,2]
B = [3,4,5]
R = [6,7,8]
AUX = [9,10,11,12]
n = len(A) + len(B) + len(R) + len(AUX)
circuit = QuantumCircuit(n,2)
circuit.x(B[2])
add(circuit, A, B, R, AUX)
print("\nAddition Circuit\n")
print_measures(circuit, R[0], AUX[0])

# Code check substraction
A = [0,1,2]
B = [3,4,5]
R = [6,7,8]
AUX = [9,10,11,12]
n = len(A) + len(B) + len(R) + len(AUX)
circuit = QuantumCircuit(n,2)
circuit.x(B[2])
substract(circuit, A, B, R, AUX)
print("\nSubtraction Circuit\n")
print_measures(circuit, R[0], AUX[0])

# Code check comparison
A = [0,1,2]
B = [3,4,5]
r = 6
AUX = [7,8,9]
n = len(A) + len(B) + len(AUX) + 1
circuit = QuantumCircuit(n,2)
circuit.x(A[0])
circuit.x(B[2])
greater_or_eq(circuit, A, B, r, AUX)
print("\nComparison Circuit\n")
print_measures(circuit, r, AUX[0])