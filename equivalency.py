"""This file will contain the different methods of testing equivalency between
two unitary matrices."""

from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator
import numpy as np


def state_vector_equiv(circuit1: QuantumCircuit, circuit2: QuantumCircuit) -> bool:
    """This method compares the state vectors from the two circuits.

        NOTE: This does not consider a global phase

    Parameters:
        circuit1 and circuit2 are both Qiskit circuits

    Return:
        True if the state_vectors from the circuits are equivalent
        Otherwise, False is returned."""

    return Statevector.from_instruction(circuit1).equiv(
        Statevector.from_instruction(circuit2)
    )


def unitaries_allclose(circuit1: QuantumCircuit, circuit2: QuantumCircuit) -> bool:
    """This method uses Numpy's allclose to compare the unitary matrices

    Parameters:
        circuit1 and circuit2 are both Qiskit circuits

    Return:
        Returns True if two matrices are element-wise equal within a tolerance (1e-8)
    """

    circuit1.save_unitary()
    circuit2.save_unitary()

    # Transpile for simulator
    simulator = AerSimulator(method="unitary")
    circuit1 = transpile(circuit1, simulator, optimization_level=0)
    circuit2 = transpile(circuit2, simulator, optimization_level=0)

    # Run and get unitary
    result = simulator.run([circuit1, circuit2]).result()
    unitary1 = result.get_unitary(circuit1)
    unitary2 = result.get_unitary(circuit2)
    return np.allclose(unitary1, unitary2)


def operator_equiv(circuit1: QuantumCircuit, circuit2: QuantumCircuit) -> bool:
    """This method uses the Operator's equiv function to test if the circuits are equivalent

    Parameters:
        circuit1 and circuit2 are both Qiskit circuits

    Return:
        Returns True if two matrices are element-wise equal within a tolerance (1e-8)
    """

    return Operator(circuit1).equiv(Operator(circuit2))
