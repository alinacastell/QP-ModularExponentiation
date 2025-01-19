from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

# Multiplication by Two Modulo N
def times_two_mod(circuit, N, A, R, AUX):
    '''
    Doubles number(A) modulo number(N).
    '''
    n = len(A)
    required_aux = 2 * n + 6
    if len(AUX) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")
    # Split auxiliary register
    temp = AUX[:n]
    add_mod_aux = AUX[n:]
    # Copy A to R
    copy(circuit, A, R)
    # Add A to R modulo N (R = A + A mod N)
    add_mod(circuit, N, A, temp, R, add_mod_aux)

n = 2  # number of bits
required_aux = 11
total_qubits = 3*n + required_aux

# Code check addition modulo N
N = list(range(0, n))
A = list(range(n, 2 * n))
R = list(range(2 * n, 3 * n))
aux = list(range(3 * n, total_qubits))

# Create the circuit
circuit = QuantumCircuit(total_qubits,n)

# Initialize values (e.g., A = 3, N = 7)
set_bits(circuit, N, [1,1])  # N = 7 (binary)
set_bits(circuit, A, [0,1])  # A = 3 (binary)

# Test times_two_mod
times_two_mod(circuit, N, A, R, aux)
print("\nMultiplication by two Modulo N Circuit\n")
print("N = [1,1] // A = [0,1]\n")
circuit.measure([R[1],R[0]], [0,1])
print_measures(circuit)