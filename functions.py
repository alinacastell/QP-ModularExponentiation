# Modular Exponentiation
# Implementation of functions ordered as instructed

# General imports
from utils import print_measures
from qiskit import QuantumCircuit
import numpy as np

# Initialization
def set_bits(circuit, A, X):
    '''
    Initialize bits of register A with binary string X.
    '''
    n = len(A)
    for i in range(len(X)):
        if X[i] == 1:
            # Apply X-gate
            circuit.x(A[i])
    # Measure input qubits and store into classical bits
    measured_qubits =[i for i in range(n)]
    classical_results =[i for i in range(n)]
    circuit.measure(measured_qubits, classical_results)
    return circuit

# Copy
def copy(circuit, A, B):
    '''
    Copy the binary string of A to the register B.
    '''
    for a, b in zip(A, B):
        # Apply CNOT gate
        circuit.cx(a, b)
    # Measure input qubits and store into classical bits
    measured_qubits =[i for i in range(n)]
    classical_results =[i for i in range(n)]
    circuit.measure(measured_qubits, classical_results)
    return circuit

# Full Adder
def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    '''
    Implement a full adder.
    '''
    # Compute result bit with CNOT gates
    circuit.cx(a,r)
    circuit.cx(b,r)
    circuit.cx(c_in,r)
    # Compute c_out bit with CNOT and Toffoli gates
    circuit.ccx(a, b, AUX)  # AUX = a AND b
    circuit.ccx(c_in, r, c_out)
    circuit.cx(AUX, c_out)
    # Reverse aux to |0⟩
    circuit.ccx(a, b, AUX)
    # Measure input qubits and store into classical bits
    measured_qubits =[i for i in range(n)]
    classical_results =[i for i in range(n)]
    circuit.measure(measured_qubits, classical_results)
    return circuit


# Code check initialization
A = [2,4,3,7,5]
X = "01011"
n = len(A)
circuit = QuantumCircuit(n,n)
set_bits(circuit, A, X)
print("Initialization Circuit\n")
print(circuit)
print_measures(circuit)

# Code check copy
A = [2,4,3]
B = [1,0,5]
n = len(A) + len(B)
circuit = QuantumCircuit(n,n)
copy(circuit, A, B)
print("Copy Circuit\n")
print(circuit)
print_measures(circuit)

# Code check full adder
n = 6
circuit = QuantumCircuit(n,n)
a = 0
b = 1
r = 2
c_in = 3
c_out = 4
AUX = 5
full_adder(circuit, a, b, r, c_in, c_out, AUX)
print("Full Adder Circuit\n")
print(circuit)
print_measures(circuit)