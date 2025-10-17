"""This file will be used for the functions that will generate the Toffoli
circuit and also the task circuit with the parameterized U3 gates."""

from qiskit import QuantumCircuit


def generate_toffoli() -> QuantumCircuit:
    """This returns a Qiskit circuit of a Toffoli gate"""
    qc = QuantumCircuit(3)
    qc.ccx(0, 1, 2)
    return qc


def generate_task_circuit(
    theta1: float = 0,
    phi1: float = 0,
    lambda1: float = 0,
    theta2: float = 0,
    phi2: float = 0,
    lambda2: float = 0,
) -> QuantumCircuit:
    """This returns a Qiskit circuit from task 1 with two
    U3 gates filled in with the appropriately passed in parameters
    (Visually confirmed to be accurate in IBM Composer)

    Paramters:
        theta1, phi1, lambda1 - parameters for the first U3 gate
        theta2, phi2, lambda2 - parameters for the second U3 gate

    Return:
        QuantumCircuit with the appropriate gates
    """
    qc = QuantumCircuit(3)
    qc.t(0)
    qc.u(theta=theta1, phi=phi1, lam=lambda1, qubit=2)
    qc.cx(0, 1)
    qc.tdg(1)
    qc.cx(0, 1)
    qc.t(1)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.cx(1, 2)
    qc.u(theta=theta2, phi=phi2, lam=lambda2, qubit=2)
    qc.cx(0, 2)
    qc.t(2)
    qc.h(2)
    return qc
