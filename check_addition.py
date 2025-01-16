# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

def add(circuit, A, B, R, AUX):
    '''
    Adds number(A) and number(B).
    '''
    n = len(A)
    # Initialize carry-in to 0 for the first adder
    c_in = AUX[0]
    # Comput cascade of full-adders
    for i in range(n):
        c_out = AUX[i + 1]
        full_adder(circuit, A[i], B[i], R[i], c_in, c_out, AUX[n+1:])
        c_in = c_out # Update carry-in
    # Ensure all auxiliary qubits are reset to |0> after computation (optional)
    for aux in AUX:
        circuit.reset(aux)

# Code check addition
A = [0,1,2]
B = [3,4,5]
R = [6,7,8] # measure output register
AUX = [9,10,11,12, 13, 14,15,16]
n = len(A) + len(B) + len(R) + len(AUX) +4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, [A, B], [[1,0,0],[1,1,0]])
add(circuit, A, B, R, AUX)
print("\nAddition Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)