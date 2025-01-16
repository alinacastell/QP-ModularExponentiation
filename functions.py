# Modular Exponentiation
# Implementation of functions ordered as instructed

# General imports
from qiskit.circuit.library import MCXGate

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
    Adds number(A) and number(B).
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
    Substracts number(A) and number(B).
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
    Test if number(A) >= number(B)
    '''
    n = len(A)
    # Check if A[i] > B[i]
    # Iterate from MSB to LSB
    for i in range(n - 1, -1, -1): 
        circuit.x(B[i]) # Negate B[i]
        mcx_gate = MCXGate(num_controls=2)
        circuit.append(mcx_gate, qargs=[A[i], B[i], AUX[i]])
        circuit.x(B[i]) # Reverse B[i]
    # Check if A[i] = B[i]
    for i in range(len(A)):
        circuit.x(AUX[i])
    # Store result in r
    circuit.mcx([AUX[:n]], r)
    # Reset AUX qubits to |0⟩
    for i in range(len(A)):
        circuit.x(AUX[i])

# Addition Modulo N
def add_mod(circuit, N, A, B, R, aux):
    ''''''


# Multiplication by Two Modulo N
def times_two_mod(circuit, N, A, R, AUX):
    '''
    Doubles number(A) modulo number(N).
    '''
    # Copy A to R
    copy(circuit, A, R)
    # Add A to R modulo N (R = A + A mod N)
    add_mod(circuit, N, A, R, R, AUX)


# Multiplication by a Power of Two Modulo N
def times_two_power_mod(circuit, N, A, k, R, AUX):
    '''
    Multiplies number(A) by 2^k modulo number(N).
    '''
    for i in range(k):
        times_two_mod(circuit, N, A, R, AUX)


# Multiplication Modulo N
def multiply_mod(circuit, N, A, B, R, AUX):
    '''
    Multiplies number(A) with number(B) modulo number(N).
    '''
    # Initialize the result register R to |0⟩
    for r in R:
        circuit.reset(r)  # Ensure R starts at |0⟩
    # Iterate over each bit in B
    for k in range(len(B)):
        # Apply controlled multiplication by 2^k modulo N
        times_two_power_mod(circuit, N, A, k, AUX[:len(A)], AUX[len(A):])
        for i in range(len(A)):
            circuit.cx(B[k], AUX[k])


# Multiplication Modulo N with a hard-coded factor
def multiply_mod_fixed(circuit, N, X, B, AUX):
    '''
    Multiplies number(B) by a fixed number X modulo number(N),
    the result (X * B mod N) replaces the value in register B.
    '''
    # Represent the binary value of X
    bin_X = AUX[:len(B)]
    copy(circuit, X, bin_X)
    # Use multiply_mod to compute X * B modulo N
    multiply_mod(circuit, N, bin_X, B, B, AUX[len(B):])


# Multiplication by X^2^k modulo N
def multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k):
    '''
    Multiplies number(B) by the number(X^2^k) modulo number(N).
    '''
    # Pre-compute W = X^(2^k) mod N using classical computation
    W = X
    for _ in range(k):
        W = (W * W) % int(''.join(map(str, N)), 2)
    # Use the precomputed W to call multiply_mod_fixed
    multiply_mod_fixed(circuit, N, W, B, AUX)


# Multiplication by X^Y modulo N
def multiply_mod_fixed_power_Y(circuit,N,X,B,AUX,Y):
    '''
    Multiplies number(B) by the number(X^Y) modulo number(N).
    '''
    # Iterate over each bit of Y
    for k in range(len(Y)):
        # If the k-th bit of Y is 0 the operation is skipped
        # Apply the controlled multiplication by X^(2^k) mod N
        circuit.x(Y[k])  # Flip Y[k] to use it as control
        multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k)
        circuit.x(Y[k])  # Revert Y[k]