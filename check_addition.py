# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

    
    # Ensure all auxiliary qubits are reset to |0> after computation (optional)
    #for aux in AUX2:
    #    circuit.x(aux)

# Code check addition
#A = [0, 1, 2]
#B = [3, 4, 5]
#R = [6, 7, 8,9]  # measure output register
#AUX = [10, 11, 12, 13, 14, 15, 16]
A = [0,1, 2]
B = [3,4,5]
AUX1 = [6,7,8,9,10,11,12]
R = [13,14,15]

n = len(A) + len(B) + len(R) + len(AUX1)
circuit = QuantumCircuit(n, 3)
print("\nAddition Circuit\n")
set_bits(circuit, R, [0,0,0,0])
set_bits(circuit, A, [1,0,0])
set_bits(circuit, B, [1,1,0])
add(circuit, A, B, R, AUX1)
circuit.barrier()
circuit.measure([AUX1[2],R[0],R[1]], [0, 1,2])
print_measures(circuit)
