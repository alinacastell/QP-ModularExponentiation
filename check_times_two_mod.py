from functions import times_two_mod, set_bits
from qiskit import QuantumCircuit
from utils import print_measures

n = 2  # number of bits
required_aux = 2*n + 12  # auxiliary qubits needed
total_qubits = 4*n + required_aux

# Code check addition modulo N
N = list(range(0, n))        # Modulus N
A = list(range(n, 2 * n))    # Input number A
R = list(range(2 * n, 3 * n))  # Result register R
aux = list(range(3 * n, total_qubits))  # Auxiliary qubits

# Create the circuit
circuit = QuantumCircuit(total_qubits,n)

# Initialize values (e.g., A = 3, N = 7)
set_bits(circuit, N, [0, 1])  # N = 7 (binary)
set_bits(circuit, A, [0, 0])  # A = 3 (binary)

# Test times_two_mod
times_two_mod(circuit, N, A, R, aux)
print("\nMultiplication by two Modulo N Circuit\n")
circuit.measure(A, [0,1])
print_measures(circuit)