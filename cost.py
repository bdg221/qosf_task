"""This file is used for the cost functions associated with the project"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from generate_circuits import generate_toffoli


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
