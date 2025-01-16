from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

# Initialization

# Code check initialization
A = [0,1,2]
X = [1,1,0]
n = len(A)
circuit = QuantumCircuit(n,n)
set_bits(circuit, A, X)
print("\nInitialization Circuit\n")
circuit.barrier()
circuit.measure(A, [0,1,2])
print_measures(circuit)