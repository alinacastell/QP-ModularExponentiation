# Utils 

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit import qpy

def print_measures(circuit):
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
    print("Counts: ",counts)

