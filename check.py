# Measure and check correct function implementation

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit
from qiskit.visualization import plot_distribution
import numpy as np

# Code check initialization
A = [0,1,2]
X = [1,1,0]
n = len(A)
circuit = QuantumCircuit(n,n)
set_bits(circuit, A, X)
print("\nInitialization Circuit\n")
circuit.barrier()
circuit.measure(A, [0,1,2])
print(circuit)
print_measures(circuit)

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
print(circuit)
print_measures(circuit)


# Code check full adder
a = 0
b = 1
c_in = 2
c_out = 3
r = 4
AUX = [5,6,7,8]
n = len(AUX)+5
circuit = QuantumCircuit(n,2)
set_bits(circuit, [a,b], [1,0])
full_adder(circuit, a, b, r, c_in, c_out, AUX)
print("\nFull Adder Circuit\n")
circuit.barrier()
circuit.measure([c_out,r], [0,1])
print(circuit)
print_measures(circuit)

# Code check addition
A = [0,1,2]
B = [3,4,5]
R = [6,7,8] # measure output register
AUX = [9,10,11,12, 13, 14,15,16]
n = len(A) + len(B) + len(R) + len(AUX) +4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, [A, B], [[1,0,0],[1,1,0]])
add(circuit, A, B, R, AUX)
print("\nAddition Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)

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

# Code check comparison
A = [0,1]
B = [2,3]
r = 4
AUX = [5,6,7,8]
n = len(A) + len(B) + len(AUX) + 1
circuit = QuantumCircuit(n,2)
set_bits(circuit, A, [1,1])
set_bits(circuit, B, [1,1])
greater_or_eq(circuit, A, B, r, AUX)
print("\nComparison Circuit\n")
circuit.barrier()
circuit.measure(r,0)
print_measures(circuit)

# Code check addition modulo N
A = [0, 1]  # Qubits for register A
B = [2, 3]  # Qubits for register B
R = [4, 5]  # Qubits for result register
N = [6, 7]
aux = [8, 9, 10, 11, 12, 13, 14]  # Auxiliary qubits
n = 15
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(B[1])
circuit.x(N[1])
add_mod(circuit, N, A, B, R, aux)
print("\nAddition Modulo N Circuit\n")
print(circuit)

# Code check multiplication by two modulo N
A = [0, 1]  # Qubits for register A
N = [2, 3]  # Qubits for register B
R = [4, 5]  # Qubits for result register
aux = [6, 7, 8, 9, 10, 11, 12]  # Auxiliary qubits
n = 13
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(N[1])
times_two_mod(circuit, N, A, R, aux)
print("\Multiplication by two Modulo N Circuit\n")
print(circuit)

# Code check multiplication by power of two modulo N
A = [0, 1]  # Qubits for register A
N = [2, 3]  # Qubits for register B
R = [4, 5]  # Qubits for result register
aux = [6, 7, 8, 9, 10, 11, 12]  # Auxiliary qubits
k = 2
n = 13
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(N[1])
times_two_mod(circuit, N, A, R, aux)
print("\Multiplication by power of two Modulo N Circuit\n")
print(circuit)

# Code check multiplication by power of two modulo N
A = [0, 1]  # Qubits for register A
N = [2, 3]  # Qubits for register B
R = [4, 5]  # Qubits for result register
AUX = [6, 7, 8, 9, 10, 11, 12]  # Auxiliary qubits
k = 2
n = 13
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(N[1])
times_two_power_mod(circuit, N, A, k, R, AUX)
print("\Multiplication by power of two Modulo N Circuit\n")
print(circuit)

# Code check multiplication modulo N
A = [0, 1]  # Qubits for register A
B = [2, 3]  # Qubits for register B
R = [4, 5]  # Qubits for result register
N = [6, 7]
AUX = [8, 9, 10, 11, 12, 13, 14]  # Auxiliary qubits
n = 15
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(N[1])
multiply_mod(circuit, N, A, B, R, AUX)
print("\Multiplication Modulo N Circuit\n")
print(circuit)

# Code check multiplication modulo N with a hard-coded factor
X = '01000'
B = [2, 3]  # Qubits for register B
N = [6, 7]
AUX = [8, 9, 10, 11, 12, 13, 14]  # Auxiliary qubits
n = 15
circuit = QuantumCircuit(n)
circuit.x(A[0])
circuit.x(A[1])
circuit.x(N[1])
multiply_mod_fixed(circuit, N, X, B, AUX)
print("\Multiplication Modulo N with hard-coded factorCircuit\n")
print(circuit)