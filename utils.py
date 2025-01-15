# Simulation using AerSimulator()

from qiskit import transpile
from qiskit_aer import AerSimulator

def print_measures(circuit, x, y):
    # Measure two qubits and put result to classical bits
    circuit.measure(x, 0)
    circuit.measure(y, 1)
    # Print circuit diagram
    print(circuit)
    # Define the backend
    backend = AerSimulator()
    # Transpile 
    compiled_circuit = transpile(circuit, backend)
    # Execute the circuit in the simulator
    n_shots = 1024
    result = backend.run(compiled_circuit, shots=n_shots).result()
    # Extract Information
    counts = result.get_counts(compiled_circuit)
    print("Counts",counts)
