# Comparison

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

def greater_or_eq(circuit, A, B, r, AUX):
    '''
    Test if number(A) >= number(B)
    '''
    n = len(A)
    for i in range(n-1, -1, -1):
        print("i = ", i)
        a = A[i]
        b = B[i]
        circuit.x(b)
        circuit.ccx(a, b, AUX[i])
        circuit.x(b)
        circuit.x(a)
        circuit.ccx(a, b, AUX[i-1])
        circuit.x(a)
        circuit.x(AUX[i-1])
        # Store result in r
        circuit.cx(AUX[i], r)



# Code check comparison
A = [0,1]
B = [2,3]
r = 4
AUX = [5,6,7,8]
n = len(A) + len(B) + len(AUX) + 1
circuit = QuantumCircuit(n,2)
set_bits(circuit, A, [1,1])
set_bits(circuit, B, [1,1])
greater_or_eq(circuit, A, B, r, AUX)
print("\nComparison Circuit\n")
circuit.barrier()
circuit.measure(r,0)
print_measures(circuit)