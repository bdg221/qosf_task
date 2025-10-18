"""This file is used for the cost functions associated with the project"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.result import Result
from qiskit_aer import AerSimulator
from itertools import product

from generate_circuits import generate_toffoli

simulator = AerSimulator()


def frobenius_norm(circuit: QuantumCircuit) -> float:
    """This uses frobenius norm for calculating the cost"""

    toffoli_circuit = generate_toffoli()

    circuit.save_unitary()
    toffoli_circuit.save_unitary()

    # Transpile for simulator
    simulator = AerSimulator(method="unitary")
    toffoli_circuit = transpile(toffoli_circuit, simulator, optimization_level=0)
    circuit = transpile(circuit, simulator, optimization_level=0)

    # Run and get unitary
    result = simulator.run([toffoli_circuit, circuit]).result()
    toffoli_unitary = result.get_unitary(toffoli_circuit)
    unitary = result.get_unitary(circuit)
    return np.linalg.norm(toffoli_unitary - unitary, "fro")


def trace_norm(circuit: QuantumCircuit) -> float:
    """This uses trace norm for calculating the cost"""

    toffoli_circuit = generate_toffoli()

    circuit.save_unitary()
    toffoli_circuit.save_unitary()

    # Transpile for simulator
    simulator = AerSimulator(method="unitary")
    toffoli_circuit = transpile(toffoli_circuit, simulator, optimization_level=0)
    circuit = transpile(circuit, simulator, optimization_level=0)

    # Run and get unitary
    result = simulator.run([toffoli_circuit, circuit]).result()
    toffoli_unitary = result.get_unitary(toffoli_circuit)
    unitary = result.get_unitary(circuit)
    return 0.5 * np.linalg.norm(
        toffoli_unitary @ unitary.conj().T - np.eye(toffoli_unitary.shape[0]), "fro"
    )


def count_comparison(circuit: QuantumCircuit) -> float:
    """This method simulates all possible inputs and compares the count results
    against the ideal Toffoli results. The number"""
    toffoli_counts = run_all_inputs(generate_toffoli())
    all_inputs_counts = run_all_inputs(circuit)
    total_cost = float(0)
    for bits in toffoli_counts.keys():
        toffoli_probabilities = toffoli_counts[bits]
        all_inputs_probabilties = all_inputs_counts[bits]
        combined_probabilites = set(toffoli_probabilities.keys()) | set(
            all_inputs_probabilties.keys()
        )
        cost = sum(
            abs(toffoli_probabilities.get(o, 0) - all_inputs_probabilties.get(o, 0))
            for o in combined_probabilites
        )
        total_cost += cost
    return total_cost / len(toffoli_counts)


def run_all_inputs(circuit: QuantumCircuit) -> dict:
    """This function runs the circuit with all possible inputs for 3 qubits. The results
    are returned as dictionary"""
    results = {}
    for input_vals in product([0, 1], repeat=3):
        temp_circuit = QuantumCircuit(3, 3)
        for i, bit in enumerate(input_vals):
            if bit:
                temp_circuit.x(i)
        temp_circuit.append(circuit, [0, 1, 2])
        temp_circuit.measure_all(add_bits=False)
        counts = (
            simulator.run(transpile(temp_circuit, simulator, optimization_level=0))
            .result()
            .get_counts()
        )
        total = sum(counts.values())
        probabilities = {bits: count / total for bits, count in counts.items()}
        results["".join(map(str, input_vals))] = probabilities
    return results
