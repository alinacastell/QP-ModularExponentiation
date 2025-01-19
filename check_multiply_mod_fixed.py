# Multiplication Modulo N with a hard-coded factor

from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

def multiply_mod_fixed(circuit, N, X, B, AUX):
    '''
    Multiplies number(B) by a fixed number X modulo number(N),
    the result (X * B mod N) replaces the value in register B.
    That is, the circuit implements a unitary transformation that sends |number(B)⟩|0⟩ to |X* number(B) mod N⟩|0⟩
    '''
    n = len(B)
    required_aux = 2 * n + 6
    if len(AUX) < required_aux:
        raise ValueError(f"multiply_mod needs at least {required_aux} auxiliary qubits.")
    # Split auxiliary register
    temp = AUX[:n]
    add_mod_aux = AUX[n:]
    # Iterate over each bit of the fixed binary number X
    for k in range(len(X)):
        if X[k] == 1:
            # If the k-th bit of X is 1, multiply B by 2^k modulo N
            times_two_power_mod(circuit, N, B, k, temp, add_mod_aux)
            # Add the result to B modulo N
            add_mod(circuit, N, B, temp, B, add_mod_aux)

# Code check multiplication modulo N
n = 2 
required_aux = 12
total_qubits = 3*n + required_aux
N = [0,1]
B = [2,3]
AUX = [4,5,6,7,8, 9, 10, 11, 12, 13, 14,15,16]
X = [1,1]
n = len(B)
# Create the circuit
circuit = QuantumCircuit(total_qubits,n)
# Initialize values
set_bits(circuit, N, [1,1])
set_bits(circuit, B, [1,0])
# Test times_two_mod
multiply_mod_fixed(circuit, N, X, B, AUX)
print("\nMultiplication Modulo N Circuit\n")
circuit.measure([B[1],B[0]], [0,1])
print_measures(circuit)