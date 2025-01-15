# Modular Exponentiation
# Implementation of functions ordered as instructed

# General imports

# Initialization
def set_bits(circuit, A, X):
    '''
    Initialize bits of register A with binary string X.
    '''
    n = len(A)
    for i in range(len(X)):
        if X[i] == 1:
            # Apply X-gate
            circuit.x(A[i])

# Copy
def copy(circuit, A, B):
    '''
    Copy the binary string of A to the register B.
    '''
    for a, b in zip(A, B):
        # Apply CNOT gate
        circuit.cx(a, b)

# Full Adder
def full_adder(circuit, a, b, r, c_in, c_out, AUX):
    '''
    Implement a full adder.
    '''
    # Compute result bit with CNOT gates
    circuit.cx(a,r)
    circuit.cx(b,r)
    circuit.cx(c_in,r)
    # Compute c_out bit with CNOT and Toffoli gates
    circuit.ccx(a, b, AUX)  # AUX = a AND b
    circuit.ccx(c_in, r, c_out)
    circuit.cx(AUX, c_out)
    # Reverse aux to |0⟩
    circuit.ccx(a, b, AUX)

# Addition
def add(circuit, A, B, R, AUX):
    '''
    Implement a circuit that adds A and B
    by creating a cascade of full-adder circuits.
    '''
    # Initialize carry-in bit to 0
    c_in = AUX[0]
    # Comput cascade of full-adders
    for i in range(len(A)):
        c_out = AUX[i+1]
        full_adder(circuit, A[i], B[i], R[i], c_in, c_out, AUX[i])
        c_in = c_out # Update for next step

# Substraction
def substract(circuit, A, B, R, AUX):
    '''
    Implement circuit that substracts A and B.
    '''
    # Negate each bit of B
    for b in B:
        circuit.x(b)
    # Initialize carry-in bit to 1
    circuit.x(AUX[0])
    add(circuit, A, B, R, AUX)
    # Reset carry-in bit to 0
    circuit.x(AUX[0])

# Comparison
def greater_or_eq(circuit, A, B, r, AUX):
    '''
    Test if A >= B
    '''
    n = len(A)
    # Check if A[i] > B[i]
    # Iterate from MSB to LSB
    for i in range(n - 1, -1, -1): 
        circuit.x(B[i]) # Negate B[i]
        circuit.mcx([A[i], B[i]], AUX[i])
        circuit.x(B[i]) # Reverse B[i]
    # Check if A[i] = B[i]
    for i in range(len(A)):
        circuit.x(AUX[i])
    # Store result in r
    circuit.mcx([AUX[:n]], r)
    # Reset AUX qubits to |0⟩
    for i in range(len(A)):
        circuit.x(AUX[i])