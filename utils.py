# Simulation using AerSimulator()

from qiskit import transpile
from qiskit_aer import AerSimulator

def print_measures(circuit):
    # Define the backend
    backend = AerSimulator()
    # Transpile 
    compiled_circuit = transpile(circuit, backend)
    # Execute the circuit in the simulator
    n_shots = 1024
    result = backend.run(compiled_circuit, shots=n_shots).result()
    # Extract Information
    counts = result.get_counts(compiled_circuit)
    probs = {key:value/n_shots for key,value in counts.items()}
    decimal_result = {int(key,2):value/n_shots for key,value in counts.items()}
    print("Counts",counts)
    print("Probabilities:", probs)
    print("Decimal Result:", decimal_result)
    print()