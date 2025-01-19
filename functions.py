# Modular Exponentiation
# Implementation of functions ordered as instructed

# General imports
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
from utils import *

# Initialization
def set_bits(circuit, A, X):
    '''
    Initialize bits of register A with binary string X.
    '''
    # Apply X-gate
    for i in range(len(X)):
        if X[i] == 1:
            circuit.x(A[i])

# Copy
def copy(circuit, A, B):
    '''
    Copy the binary string of A to the register B.
    '''
    # Apply CNOT gate
    for a, b in zip(A, B):
        circuit.cx(a, b)

# Full Adder
def full_adder(circuit, a, b, r, c_in, c_out, aux):
    '''
    Implement a full adder.
    '''
    # r = a xor b xor c_in
    circuit.cx(a, r)  # sum = a
    circuit.cx(b, r)  # sum = a ⊕ b
    circuit.cx(c_in, r)  # sum = a ⊕ b ⊕ c_in

    # Step 2: Compute carry out
    # First, compute (a AND b) into aux[0]
    circuit.ccx(a, b, aux[0])  # aux[0] = a AND b

    # Then, compute (a AND c_in) into aux[1]
    circuit.ccx(a, c_in, aux[1])  # aux[1] = a AND c_in

    # Next, compute (b AND c_in) into aux[2]
    circuit.ccx(b, c_in, aux[2])  # aux[2] = b AND c_in

    # OR all results together into c_out
    circuit.cx(aux[0], c_out)  # c_out = (a AND b)
    circuit.cx(aux[1], c_out)  # c_out = (a AND b) OR (a AND c_in)
    circuit.cx(aux[2], c_out)  # c_out = (a AND b) OR (a AND c_in) OR (b AND c_in)

    # Step 3: Uncompute auxiliary qubits (in reverse order)
    circuit.ccx(b, c_in, aux[2])
    circuit.ccx(a, c_in, aux[1])
    circuit.ccx(a, b, aux[0])

# Addition
def add(circuit, A, B, R, AUX):
    '''
    Adds number(A) and number(B).
    '''
    n = len(A)
    if len(AUX) < n + 4:
        raise ValueError(f"Need at least {n + 4} auxiliary qubits")

    carry_bits = AUX[:n + 1]  # n+1 carry bits (including initial 0)
    adder_aux = AUX[n + 1:n + 4]  # 3 auxiliary bits for full_adder

    # Initialize first carry bit to 0
    circuit.reset(carry_bits[0])

    # Forward pass: Create cascade of full-adders
    for i in range(n):
        full_adder(circuit, A[i], B[i], carry_bits[i], carry_bits[i + 1], R[i], adder_aux)

# Subtraction
def subtract(circuit, A, B, R, AUX):
    '''
    Subtracts number(A) and number(B).
    '''
    # Negate each bit of B
    for b in B:
        circuit.x(b)
    # Initialize carry-in bit to 1
    circuit.x(AUX[0])
    add(circuit, A, B, R, AUX)

# Comparison
def greater_or_eq(circuit, A, B, r, AUX):
    '''
    Test if number(A) >= number(B)
    '''
    n = len(A)
    for i in range(n-1, -1, -1):
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

# Addition Modulo N
def add_mod(circuit, N, A, B, R, aux):
    '''
    Adds number(A) to number(B) modulo number(N).
    '''
    # Add A and B, store result temporarily in aux[:len(R)]
    n = len(A)
    required_aux = 2 * n + 5
    if len(aux) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")
    # Split auxiliary register
    temp = aux[:n]
    comp_bit = aux[n]
    carry_bits = aux[n + 1:2 * n + 2]
    adder_aux = aux[2 * n + 2:2 * n + 5]
    # Add A and B into temp
    add(circuit, A, B, temp, carry_bits + adder_aux)
    # Compare temp with N
    greater_or_eq(circuit, temp, N, comp_bit, carry_bits)
    # Controlled subtraction of N from temp
    subtract(circuit, temp, N, R, carry_bits + adder_aux)
    # If no subtraction, copy temp into R
    for i in range(len(temp)):
        circuit.cx(comp_bit, temp[i])
        circuit.cx(temp[i], R[i])
        circuit.cx(comp_bit, temp[i])


# Multiplication by Two Modulo N
def times_two_mod(circuit, N, A, R, AUX):
    '''
    Doubles number(A) modulo number(N).
    '''
    n = len(A)
    required_aux = 2 * n + 5
    if len(AUX) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")
    # Split auxiliary register
    temp = AUX[:n]
    add_mod_aux = AUX[n:]
    # Copy A to R
    copy(circuit, A, R)
    # Add A to R modulo N (R = A + A mod N)
    add_mod(circuit, N, A, temp, R, add_mod_aux)


# Multiplication by a Power of Two Modulo N
def times_two_power_mod(circuit, N, A, k, R, AUX):
    '''
    Multiplies number(A) by 2^k modulo number(N).
    '''
    for _ in range(k):
        times_two_mod(circuit, N, A, R, AUX)

# Multiplication Modulo N
def multiply_mod(circuit, N, A, B, R, AUX):
    '''
    Multiplies number(A) with number(B) modulo number(N).
    '''
    n = len(A)
    required_aux = 2 * n + 6
    if len(AUX) < required_aux:
        raise ValueError(f"multiply_mod needs at least {required_aux} auxiliary qubits.")
    # Compute partial sums for k = 0 to len(B) - 1
    for k in range(len(B)):
        # Split auxiliary register
        temp = AUX[:n]
        add_mod_aux = AUX[n:]
        # Controlled multiplication by 2^k mod N
        times_two_power_mod(circuit, N, A, k, temp, add_mod_aux)
        # Controlled addition of temp to the result R modulo N
        for i in range(len(R)):
            circuit.cx(B[k], temp[i])
        add_mod(circuit, N, R, temp, R, add_mod_aux)


# Multiplication Modulo N with a hard-coded factor
def multiply_mod_fixed(circuit, N, X, B, AUX):
    '''
    Multiplies number(B) by a fixed number X modulo number(N),
    the result (X * B mod N) replaces the value in register B.
    '''
    n = len(B)
    required_aux = 2 * n + 6
    if len(AUX) < required_aux:
        raise ValueError(f"multiply_mod needs at least {required_aux} auxiliary qubits.")
    # Split auxiliary register
    temp = AUX[:n]
    add_mod_aux = AUX[n:]
    # Iterate over each bit of the fixed binary number X
    for k in range(len(X)):
        if X[k] == 1:
            # If the k-th bit of X is 1, multiply B by 2^k modulo N
            times_two_power_mod(circuit, N, B, k, temp, add_mod_aux)
            # Add the result to B modulo N
            add_mod(circuit, N, B, temp, B, add_mod_aux)


# Multiplication by X^2^k modulo N
def multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k):
    '''
    Multiplies number(B) by the number(X^2^k) modulo number(N).
    '''
    # Read N value from the circuit into a list
    circuit.measure([N[1],N[0]],[0,1])
    n_char = print_counts(circuit)
    N_bin = [int(char) for char in list(n_char.keys())[0]]
    # Convert binary numbers X and N to integers
    X_dec = int("".join(map(str, X)), 2)
    modulo = int("".join(map(str, N_bin)), 2)
    # Compute W = X^(2^k) mod N in Python
    W_dec = X_dec
    for _ in range(k):
        W_dec = (W_dec ** 2) % modulo
    # Convert W to binary as a list of integers of length X
    W_bin = list(map(int, bin(W_dec)[2:].zfill(len(X))))
    # Call multiply_mod_fixed to implement the circuit
    multiply_mod_fixed(circuit, N, W_bin, B, AUX)


# Multiplication by X^Y modulo N
def multiply_mod_fixed_power_Y(circuit,N,X,B,AUX,Y):
    '''
    Multiplies number(B) by the number(X^Y) modulo number(N).
    '''
    n = len(Y)  # Number of bits in Y
    for k in range(n):
        # If k-th bit of Y is 1, use it as a control
        # Apply multiply_mod_fixed_power_2_k for X^(2^k) modulo N
        multiply_mod_fixed_power_2_k(circuit, N, X, B, AUX, k)
        for i in range(len(B)):
            circuit.cx(Y[k], B[i])