# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator


    
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
AUX1 = [4,5,6,9,10,11]
R = [7,8]
A = [0,1, 2]
B = [3,4,5]
AUX1 = [6,7,8,9,10,11,12]
R = [13,14,15]

n = len(A) + len(B) + len(R) + len(AUX1)
n = len(A) + len(B) + len(R) + len(AUX1)
circuit = QuantumCircuit(n, 3)
print("\nAddition Circuit\n")
print("A = [a0,a1] = [0,1] // B = [b0,b1] = [1,1]\n")
set_bits(circuit, R, [0,0,0])
set_bits(circuit, A, [0,1])
set_bits(circuit, B, [1,1])

add(circuit, A, B, R, AUX1)
set_bits(circuit, R, [0,0,0,0])
set_bits(circuit, A, [1,0,0])
set_bits(circuit, B, [1,1,0])
add(circuit, A, B, R, AUX1)
circuit.barrier()
circuit.measure([AUX1[2],R[1],R[0]], [0,1,2])
print_measures(circuit)