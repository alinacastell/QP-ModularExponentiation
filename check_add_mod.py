from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

# Addition Modulo N
def add_mod(circuit, N, A, B, R, aux):
    '''
    Adds number(A) to number(B) modulo number(N).
    '''
    # Add A and B, store result temporarily in aux[:len(R)]
    n = len(A)
    required_aux = 2 * n + 6
    if len(aux) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")
    # Split auxiliary register
    temp = aux[:n]
    comp_bit = aux[n]
    carry_bits = aux[n + 1:2 * n + 2]
    adder_aux = aux[2 * n + 2:2 * n + 6]
    # Add A and B into temp
    add(circuit, A, B, temp, carry_bits + adder_aux)
    # Compare temp with N
    greater_or_eq(circuit, temp, N, comp_bit, carry_bits)
    # Controlled subtraction of N from temp
    subtract(circuit, temp, N, R, carry_bits + adder_aux)
    # If no subtraction, copy temp into R
    for i in range(len(temp)):
        circuit.cx(comp_bit, temp[i])
        circuit.cx(temp[i], R[i])
        circuit.cx(comp_bit, temp[i])

n = 2  # number of bits
required_aux = 2*n + 6  # auxiliary qubits needed
total_qubits = 4*n + required_aux

# Code check addition modulo N
N = list(range(0, n))
A = list(range(n, 2*n))
B = list(range(2*n, 3*n))
R = list(range(3*n, 4*n))
aux = list(range(4*n, total_qubits))
circuit = QuantumCircuit(total_qubits, 3)

# Initialize values (example: A=3, B=5, N=7)
set_bits(circuit, N, [1,0])  # N = 7
set_bits(circuit, A, [1,0])  # A = 3
set_bits(circuit, B, [1,1])  # Auxiliary qubits

add_mod(circuit, N, A, B, R, aux)
print("\nAddition Modulo N Circuit\n")
circuit.measure([aux[5],R[1],R[0]], [0,1,2])
print_measures(circuit)