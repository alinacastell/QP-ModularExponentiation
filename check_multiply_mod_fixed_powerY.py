# Multiplication by X^Y modulo N

from functions import *
from qiskit import QuantumCircuit
from utils import *

def multiply_mod_fixed_power_Y(circuit,N,X,B,AUX,Y):
    '''
    Multiplies number(B) by the number(X^Y) modulo number(N).
    '''
    n = len(Y)  # Number of bits in Y
    for k in range(n):
        # If k-th bit of Y is 1, use it as a control
        # Apply multiply_mod_fixed_power_2_k for X^(2^k) modulo N
        multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k)
        for i in range(len(B)):
            circuit.cx(Y[k], B[i])


# Code check multiplication modulo N
n = 2 
required_aux = 12
total_qubits = 3*n + required_aux
N = [0,1]
B = [2,3]
AUX = [4,5,6,7,8, 9, 10, 11, 12, 13, 14,15,16]
X = [1,1]
Y = [1,0]
n = len(B)
# Create the circuit
circuit = QuantumCircuit(total_qubits,n)
# Initialize values
set_bits(circuit, N, [1,0])
set_bits(circuit, B, [1,1])
# Test times_two_mod
multiply_mod_fixed_power_Y(circuit, N, X, B, AUX, Y)
print("\nMultiplication Modulo N Circuit\n")
circuit.measure([B[1],B[0]], [0,1])
print_measures(circuit)