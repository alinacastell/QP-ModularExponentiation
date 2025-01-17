# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

# Full Adder
def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    '''
    Implement a full adder.
    '''
    # r = a xor b xor c_in
    circuit.cx(a,r)
    circuit.cx(b,r)
    circuit.cx(c_in,r)
    # AUX[0] = a AND b
    circuit.ccx(a, b, AUX[0])
    # AUX[1] = a xor b
    circuit.cx(a,AUX[1])
    circuit.cx(b,AUX[1])
    # AUX[2] = c_in AND (a xor b)
    circuit.ccx(c_in,AUX[1],AUX[2])
    # NOT AUX[0] and NOT AUX[2]
    circuit.x(AUX[0])
    circuit.x(AUX[2])
    # AUX[3] = AUX[0] OR AUX[2]
    circuit.ccx(AUX[0], AUX[2], c_out)
    circuit.x(c_out)

# Addition
def add(circuit, A, B, R, AUX1, AUX2):
    '''
    Adds number(A) and number(B).
    '''
    n = len(A)
    # Initialize carry-in to 0 for the first adder
    c_in = AUX1[0]
    # Comput cascade of full-adders
    for i in range(n):
        c_out = AUX1[i + 1]
        full_adder(circuit, A[i], B[i], R[i], c_in, c_out, AUX2)
        c_in = AUX1[i+1] # Update carry-in

        #circuit.measure([c_out,R[0],R[1]], [0, 1,2])
        print(circuit)
    
    # Ensure all auxiliary qubits are reset to |0> after computation (optional)
    #for aux in AUX2:
    #    circuit.x(aux)

# Code check addition
#A = [0, 1, 2]
#B = [3, 4, 5]
#R = [6, 7, 8,9]  # measure output register
#AUX = [10, 11, 12, 13, 14, 15, 16]
A = [0,1]
B = [2,3]
AUX1 = [4,5,6]
R = [7,8]
AUX2 = [9,10,11]

n = len(A) + len(B) + len(R) + len(AUX1)+ len(AUX2)
circuit = QuantumCircuit(n, 3)
print("\nAddition Circuit\n")
set_bits(circuit, R, [0,0,0])
set_bits(circuit, A, [1,0])
set_bits(circuit, B, [1,1])
add(circuit, A, B, R, AUX1, AUX2)
circuit.barrier()
circuit.measure([AUX1[2],R[0],R[1]], [0, 1,2])
print_measures(circuit)
