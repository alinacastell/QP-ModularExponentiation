# Full Adder

from functions import *
from utils import print_measures
from qiskit import QuantumCircuit


# Code check full adder
a = 0
b = 1
c_in = 2
c_out = 3
r = 4
AUX = [5,6,7,8]
n = len(AUX)+5
circuit = QuantumCircuit(n,2)
set_bits(circuit, [a,b], [1,1])
full_adder(circuit, a, b, r, c_in, c_out, AUX)
print("\nFull Adder Circuit\n")
circuit.barrier()
circuit.measure([c_out,r], [0,1])
print_measures(circuit)