# Modular Exponentiation
# Implementation of functions ordered as instructed

# General imports
from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate

# Initialization
def set_bits(circuit, A, X):
    '''
    Initialize bits of register A with binary string X.
    '''
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
    # Initialize carry-in to 0 for the first adder
    c_in = AUX[0]
    # Comput cascade of full-adders
    for i in range(n):
        c_out = AUX[i + 1]
        full_adder(circuit, A[i], B[i], R[i], c_in, c_out, AUX[n+1:])
        c_in = c_out # Update carry-in
    # Ensure all auxiliary qubits are reset to |0> after computation (optional)
    for aux in AUX:
        circuit.reset(aux)

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
    # Reset carry-in bit to 0
    circuit.x(AUX[0])

# Comparison
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

# Addition Modulo N
def add_mod(circuit, N, A, B, R, aux):
    '''
    Adds number(A) to number(B) modulo number(N).
    '''
    # Step 1: Add A and B, store result temporarily in aux[:len(R)]
    n = len(A)
    required_aux = 2 * n + 6

    if len(aux) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")

    # Split auxiliary register
    temp = aux[:n]  # Temporary register for intermediate results
    comp_bit = aux[n]  # Comparison result qubit
    carry_bits = aux[n + 1:2 * n + 2]  # Carry bits for addition
    adder_aux = aux[2 * n + 2:2 * n + 6]  # Auxiliary qubits for full_adder

    # Step 1: Add A and B into temp
    add(circuit, A, B, temp, carry_bits + adder_aux)

    # Step 2: Compare temp with N
    greater_or_eq(circuit, temp, N, comp_bit, carry_bits)

    # Step 3: Controlled subtraction of N from temp
    subtract(circuit, temp, N, R, carry_bits + adder_aux)

    # Step 4: If no subtraction, copy temp into R
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
    required_aux = 2 * n + 6

    if len(AUX) < required_aux:
        raise ValueError(f"add_mod needs at least {required_aux} auxiliary qubits")

    temp = AUX[:n]  # Temporary register for intermediate results
    add_mod_aux = AUX[n:]  # Remaining auxiliary qubits for add_mod

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
    
    # Represent the binary value of X
    bin_X = set_bits(circuit, AUX[:len(B)], X)
    #copy(circuit, X, bin_X)
    # Use multiply_mod to compute X * B modulo N
    multiply_mod(circuit, N, bin_X, B, B, AUX[len(B):])
    '''
    # Step 1: Copy B into a temporary register
    temp = AUX[:len(B)]  # Temporary register for intermediate results
    copy(circuit, B, temp)

    # Step 2: Multiply B by the fixed number X modulo N
    # Use the add_mod function to repeatedly add B to itself (X times modulo N)
    for i in range(X):
        add_mod(circuit, N, temp, B, temp, AUX[len(B):])

    # Step 3: Copy the result back into B
    copy(circuit, temp, B)

    # Step 4: Reset the auxiliary qubits
    for qubit in temp:
        circuit.reset(qubit)


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