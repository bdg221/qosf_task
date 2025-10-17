"""This file tests the functions in the equivalency.py file to ensure the
functions are working properly."""

import pytest
from qiskit import QuantumCircuit

from equivalency import operator_equiv, state_vector_equiv, unitaries_allclose
from generate_circuits import generate_toffoli

i_circuit = QuantumCircuit(1)
i_circuit.id(0)

xx_circuit = QuantumCircuit(1)
xx_circuit.x(0)
xx_circuit.x(0)

yy_circuit = QuantumCircuit(1)
yy_circuit.y(0)
yy_circuit.y(0)

zx_circuit = QuantumCircuit(1)
zx_circuit.z(0)
zx_circuit.x(0)

xyz_circuit = QuantumCircuit(1)
xyz_circuit.x(0)
xyz_circuit.y(0)
xyz_circuit.z(0)

x_circuit = QuantumCircuit(1)
x_circuit.x(0)

y_circuit = QuantumCircuit(1)
y_circuit.y(0)

z_circuit = QuantumCircuit(1)
z_circuit.z(0)

hxh_circuit = QuantumCircuit(1)
hxh_circuit.h(0)
hxh_circuit.x(0)
hxh_circuit.h(0)

valid_equiv_tests = [
    (generate_toffoli(), generate_toffoli(), True),
    (xx_circuit, i_circuit, True),
    (yy_circuit, i_circuit.copy(), True),
    (z_circuit, hxh_circuit, True),
]

invalid_equiv_tests = [
    (yy_circuit.copy(), x_circuit, False),
    (xyz_circuit, zx_circuit, False),
]

global_phase_off_tests = [
    (zx_circuit.copy(), y_circuit),
    (xyz_circuit.copy(), i_circuit.copy()),
]


@pytest.mark.parametrize("equiv_func", (state_vector_equiv, operator_equiv))
@pytest.mark.parametrize(
    "circ1, circ2, expected", valid_equiv_tests + invalid_equiv_tests
)
def test_circuit_equivalence(equiv_func, circ1, circ2, expected):
    """Verify that circuit equivalence functions handle all known cases correctly."""
    result = equiv_func(circ1, circ2)
    assert result == expected, f"{equiv_func.__name__} failed on {circ1} vs {circ2}"


@pytest.mark.parametrize(
    "circ1, circ2, expected", valid_equiv_tests + invalid_equiv_tests
)
def test_unitaries_allclose(circ1, circ2, expected):
    """Verify that unitaries_allclose functions properly. This must be a separate
    test so that save_unitary() can run properly"""
    result = unitaries_allclose(circ1, circ2)
    assert result == expected, f"unitaries_allclose failed on {circ1} vs {circ2}"


@pytest.mark.parametrize("circ1, circ2", global_phase_off_tests)
def test_global_phase_off(circ1, circ2):
    """Confirm that equivalency handles global phase as expected.
    This means operator_eqiuv and state_vector_equiv should be True
    and unitaries_allclose should be False"""
    assert operator_equiv(circ1, circ2)
    assert state_vector_equiv(circ1, circ2)
    assert not unitaries_allclose(circ1, circ2)
