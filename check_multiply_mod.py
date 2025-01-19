# Multiplication Modulo N

from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

def multiply_mod(circuit, N, A, B, R, AUX):
    '''
    Multiplies number(A) with number(B) modulo number(N).
    '''
    n = len(A)
    required_aux = 2 * n + 6
    if len(AUX) < required_aux:
        raise ValueError(f"multiply_mod needs at least {required_aux} auxiliary qubits.")
    # Compute partial sums for k = 0 to len(B) - 1
    for k in range(len(B)):
        # Split auxiliary register
        temp = AUX[:n]
        add_mod_aux = AUX[n:]
        # Controlled multiplication by 2^k mod N
        times_two_power_mod(circuit, N, A, k, temp, add_mod_aux)
        # Controlled addition of temp to the result R modulo N
        for i in range(len(R)):
            circuit.cx(B[k], temp[i])
        add_mod(circuit, N, R, temp, R, add_mod_aux)

# Code check multiplication modulo N
n = 2 
required_aux = 15
total_qubits = 3*n + required_aux
N = [0,1]
A = [2,3]
B = [4,5]
R = [6,7]
AUX = [8, 9, 10, 11, 12, 13, 14, 15, 16,17,18,19,20]
n = len(R)
# Create the circuit
circuit = QuantumCircuit(total_qubits,n)
# Initialize values
set_bits(circuit, N, [1,1])
set_bits(circuit, A, [1,0])
set_bits(circuit, B, [1,0])
# Test times_two_mod
multiply_mod(circuit, N, A, B, R, AUX)
print("\nMultiplication Modulo N Circuit\n")
circuit.measure([R[1],R[0]], [0,1])
print_measures(circuit)