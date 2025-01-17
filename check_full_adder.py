# Full Adder

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit

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

# Code check full adder
a = 0
b = 1
c_in = 2
c_out = 3
r = 4
AUX = [5,6,7,8]
n = len(AUX)+5
circuit = QuantumCircuit(n,2)
set_bits(circuit, [a], [1])
set_bits(circuit, [b], [1])
set_bits(circuit, [c_in], [1])
full_adder(circuit, a, b, r, c_in, c_out, AUX)
print("\nFull Adder Circuit\n")
circuit.barrier()
circuit.measure([c_out,r], [0,1])
print_measures(circuit)