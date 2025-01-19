# Multiplication by a Power of Two Modulo N

from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

def times_two_power_mod(circuit, N, A, k, R, AUX):
    '''
    Multiplies number(A) by 2^k modulo number(N).
    '''
    for _ in range(k):
        times_two_mod(circuit, N, A, R, AUX)

# Code check multiplication by a power of two modulo N
n = 2 
required_aux = 11
total_qubits = 3*n + required_aux
# N = list(range(0, n))        # Modulus N
# A = list(range(n, 2 * n))    # Input number A
# R = list(range(2 * n, 3 * n))  # Result register R
# AUX = list(range(3 * n, total_qubits))  # Auxiliary qubits

N = [0,1]
A = [2,3]
R = [4,5]
AUX = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
k = 3
# Create the circuit
circuit = QuantumCircuit(total_qubits,n)

# Initialize values (e.g., A = 3, N = 7)
set_bits(circuit, N, [0,1])  # N = 7 (binary)
set_bits(circuit, A, [0,1])  # A = 3 (binary)

# Test times_two_mod
times_two_power_mod(circuit, N, A, k, R, AUX)
print("\nMultiplication by power of two Modulo N Circuit\n")
print("N = [0,1] // A = [0,1]\n")
circuit.measure([R[1],R[0]], [0,1])
print_measures(circuit)