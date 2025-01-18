# Addition

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit
from qiskit.providers.basic_provider import BasicSimulator

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
    # c_out = AUX[0] OR AUX[2]
    circuit.ccx(AUX[0], AUX[2], c_out)
    circuit.x(c_out)

# Addition
def add(circuit, A, B, R, AUX):
    '''
    Adds number(A) and number(B).
    '''
    n = len(A)
    if len(AUX) < n + 4:
        raise ValueError(f"Need at least {n + 4} auxiliary qubits")

    # Split auxiliary register
    carry_bits = AUX[:n + 1]  # n+1 carry bits (including initial 0)
    adder_aux = AUX[n + 1:n + 4]  # 3 auxiliary bits for full_adder

    # Create cascade of full-adders
    for i in range(n):
        full_adder(circuit, A[i], B[i], R[i],
                   carry_bits[i], carry_bits[i + 1], adder_aux)
    # Ensure all auxiliary qubits are reset to |0> after computation (optional)
    #for aux in AUX2:
    #    circuit.x(aux)

# Code check 2-qubit addition
#A = [0, 1, 2]
A = [0,1]
B = [2,3]
AUX1 = [4,5,6,9,10,11]
R = [7,8]
n = len(A) + len(B) + len(R) + len(AUX1)
circuit = QuantumCircuit(n, 3)
print("\nAddition Circuit\n")
print("A = [a0,a1] = [0,1] // B = [b0,b1] = [1,1]\n")
set_bits(circuit, R, [0,0,0])
set_bits(circuit, A, [0,1])
set_bits(circuit, B, [1,1])
add(circuit, A, B, R, AUX1)
circuit.barrier()
circuit.measure([AUX1[2],R[1],R[0]], [0,1,2])
print_measures(circuit)

# Code check 3-qubit addition
'''
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
circuit.measure([AUX1[2],R[1],R[0]], [0,1,2])
print_measures(circuit)
'''