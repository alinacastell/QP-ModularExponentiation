from functions import add_mod, set_bits
from qiskit import QuantumCircuit
from utils import print_measures

n = 2  # number of bits
required_aux = 2*n + 6  # auxiliary qubits needed
total_qubits = 4*n + required_aux

# Code check addition modulo N
N = list(range(0, n))        # Modulus N
A = list(range(n, 2*n))      # First number
B = list(range(2*n, 3*n))    # Second number
R = list(range(3*n, 4*n))    # Result
aux = list(range(4*n, total_qubits))  # Auxiliary qubits
circuit = QuantumCircuit(total_qubits, n)

# Initialize values (example: A=3, B=5, N=7)
set_bits(circuit, N, [0,1])  # N = 7
set_bits(circuit, A, [1,1])  # A = 3
set_bits(circuit, B, [1,0])  # Auxiliary qubits

add_mod(circuit, N, A, B, R, aux)
print("\nAddition Modulo N Circuit\n")
circuit.measure(A, [0,1])
print_measures(circuit)