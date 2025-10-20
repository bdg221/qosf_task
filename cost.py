"""This file is used for the cost functions associated with the project"""

from itertools import product
from typing import Union

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from generate_circuits import generate_task_circuit, generate_toffoli


def trace_overlap_cost(params_or_circuit: Union[list[float], QuantumCircuit]) -> float:
    """This uses trace overlap to determine the fidelity of a circuit and a Toffoli gate
    Then the cost 1-fidelity)"""
    if isinstance(params_or_circuit, QuantumCircuit):
        circuit = params_or_circuit.copy()
    else:
        circuit = generate_task_circuit(*params_or_circuit)

    toffoli_circuit = generate_toffoli().copy()

    circuit.save_unitary(label="optimized_circuit")
    toffoli_circuit.save_unitary(label="ideal_toffoli_circuit")

    # Transpile for simulator
    simulator_unitary = AerSimulator(method="unitary")
    toffoli_circuit = transpile(
        toffoli_circuit, simulator_unitary, optimization_level=0
    )
    circuit = transpile(circuit, simulator_unitary, optimization_level=0)

    # Run and get unitary
    result = simulator_unitary.run([toffoli_circuit, circuit]).result()
    toffoli_unitary = result.data(toffoli_circuit)["ideal_toffoli_circuit"].data
    unitary = result.data(circuit)["optimized_circuit"].data
    fidelity = (
        np.abs(np.trace(np.dot(np.conj(toffoli_unitary.T), unitary)))
        / toffoli_unitary.shape[0]
    )
    return 1 - fidelity


def frobenius_norm(params_or_circuit: Union[list[float], QuantumCircuit]) -> float:
    """This uses frobenius norm for calculating the cost"""

    if isinstance(params_or_circuit, QuantumCircuit):
        circuit = params_or_circuit.copy()
    else:
        circuit = generate_task_circuit(*params_or_circuit)

    toffoli_circuit = generate_toffoli().copy()

    circuit.save_unitary(label="test_circuit")
    toffoli_circuit.save_unitary(label="ideal_circuit")

    # Transpile for simulator
    simulator_unitary = AerSimulator(method="unitary")
    toffoli_circuit = transpile(
        toffoli_circuit, simulator_unitary, optimization_level=0
    )
    circuit = transpile(circuit, simulator_unitary, optimization_level=0)

    # Run and get unitary
    result = simulator_unitary.run([toffoli_circuit, circuit]).result()
    toffoli_unitary = result.data(toffoli_circuit)["ideal_circuit"].data
    unitary = result.data(circuit)["test_circuit"].data
    return np.linalg.norm(toffoli_unitary - unitary, "fro")


def trace_norm(params_or_circuit: Union[list[float], QuantumCircuit]) -> float:
    """This uses trace norm for calculating the cost"""

    if isinstance(params_or_circuit, QuantumCircuit):
        circuit = params_or_circuit.copy()
    else:
        circuit = generate_task_circuit(*params_or_circuit)

    toffoli_circuit = generate_toffoli().copy()

    circuit.save_unitary()
    toffoli_circuit.save_unitary()

    # Transpile for simulator
    simulator_unitary2 = AerSimulator(method="unitary")
    toffoli_circuit = transpile(
        toffoli_circuit, simulator_unitary2, optimization_level=0
    )
    circuit = transpile(circuit, simulator_unitary2, optimization_level=0)

    # Run and get unitary
    result = simulator_unitary2.run([toffoli_circuit, circuit]).result()
    toffoli_unitary = result.get_unitary(toffoli_circuit)
    unitary = result.get_unitary(circuit)
    return 0.5 * np.linalg.norm(
        toffoli_unitary @ unitary.conj().T - np.eye(toffoli_unitary.shape[0]), "fro"
    )


def count_comparison(params_or_circuit: Union[list[float], QuantumCircuit]) -> float:
    """This method simulates all possible inputs and compares the count results
    against the ideal Toffoli results. The number"""
    if isinstance(params_or_circuit, QuantumCircuit):
        circuit = params_or_circuit.copy()
    else:
        circuit = generate_task_circuit(*params_or_circuit)

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
    simulator = AerSimulator()
    results = {}
    for input_vals in product([0, 1], repeat=3):
        temp_circuit = QuantumCircuit(3, 3)
        for i, bit in enumerate(input_vals):
            if bit:
                temp_circuit.x(i)
        temp_circuit.append(circuit, [0, 1, 2])
        temp_circuit.measure_all(add_bits=False)
        transpiled_temp_circuit = transpile(
            temp_circuit, simulator, optimization_level=0
        )
        counts = (
            simulator.run(transpiled_temp_circuit).result().get_counts(temp_circuit)
        )
        total = sum(counts.values())
        probabilities = {bits: count / total for bits, count in counts.items()}
        results["".join(map(str, input_vals))] = probabilities
    return results
