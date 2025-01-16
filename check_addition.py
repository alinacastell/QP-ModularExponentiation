# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

from qiskit import QuantumCircuit

def add(circuit, A, B, R, AUX):
    """
    Adds number(A) and number(B) and stores the result in R.
    """
    n = len(A)
    # Initialize carry-in to 0 for the first adder
    c_in = AUX[0]
    circuit.x(c_in)  # Ensure carry-in starts at |0>
    for i in range(n):
        a = A[i]
        b = B[i]
        r = R[i]
        c_out = AUX[i + 1]  # Use AUX[i+1] for the carry-out
        # Apply full adder
        full_adder(circuit, a, b, r, c_in, c_out, AUX[n+1:])
        circuit.barrier()
        # Reset auxiliary qubits
        set_bits(circuit, AUX, [0]*len(AUX))
        # Update carry-in for the next adder
        c_in = c_out


# Code check addition
A = [0,1,2]
B = [3,4,5]
R = [6,7,8] # measure output register
AUX = [9,10,11,12, 13, 14, 15, 16]
n = len(A) + len(B) + len(R) + len(AUX) +4
circuit = QuantumCircuit(n,len(R))
set_bits(circuit, [A, B], [[0,0,1],[0,1,1]])
add(circuit, A, B, R, AUX)
print("\nAddition Circuit\n")
circuit.barrier()
circuit.measure(R, [0,1,2])
print_measures(circuit)