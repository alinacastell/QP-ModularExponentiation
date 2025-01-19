# Multiplication by X^2^k modulo N

from functions import *
from qiskit import QuantumCircuit
from utils import print_measures

def multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k):
    '''
    Multiplies number(B) by the number(X^2^k) modulo number(N).
    '''
    # Convert binary numbers X and N to integers
    X_dec = int("".join(map(str, X)), 2)
    modulo = int("".join(map(str, N)), 2)
    # Compute W = X^(2^k) mod N in Python
    W_dec = X_dec
    for _ in range(k):
        W_dec = (W_dec ** 2) % modulo
    # Convert W to binary as a list of integers of length X
    W_bin = list(map(int, bin(W_dec)[2:].zfill(len(X))))
    # Call multiply_mod_fixed to implement the circuit
    multiply_mod_fixed(circuit, N, W_bin, B, AUX)

# Code check multiplication modulo N
n = 2 
required_aux = 12
total_qubits = 3*n + required_aux
N = [0,1]
B = [2,3]
AUX = [4,5,6,7,8, 9, 10, 11, 12, 13, 14,15,16]
X = [1,1]
k = 2
n = len(B)
# Create the circuit
circuit = QuantumCircuit(total_qubits,n)
# Initialize values
set_bits(circuit, N, [1,1])
set_bits(circuit, B, [1,1])
# Test times_two_mod
multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k)
print("\nMultiplication Modulo N Circuit\n")
circuit.measure([B[1],B[0]], [0,1])
print_measures(circuit)

# 3*3^2^2 % 3 = 