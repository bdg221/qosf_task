"""This file contains tests for the two cost functions

test use cases:

a Toffoli gate (should have same cost 0)
toffoli gate.decompose() (should have a cost of 0)

III should have some cost, but it should be relatively small
XXX should be worse

For a more complete test, you could control a Hermitian permutation on a Toffoli gate.
That test would allow you to adjust an epsilon which should correlate to the cost.
"""

from cost import frobenius_norm, trace_norm, count_comparison

import pytest
from qiskit import QuantumCircuit


from generate_circuits import generate_toffoli

toffoli_circuit = generate_toffoli()

decomposed_toffoli_circuit = generate_toffoli().decompose()

identity_circuit = QuantumCircuit(3)
identity_circuit.id(0)
identity_circuit.id(1)
identity_circuit.id(2)

xxx_circuit = QuantumCircuit(3)
xxx_circuit.x(0)
xxx_circuit.x(1)
xxx_circuit.x(2)


@pytest.mark.parametrize("cost_func", [count_comparison, trace_norm, frobenius_norm])
def test_cost_functions(cost_func: callable):
    toffoli_cost = cost_func(toffoli_circuit)
    assert toffoli_cost == 0

    decomposed_toffoli_cost = cost_func(decomposed_toffoli_circuit)
    assert decomposed_toffoli_cost == pytest.approx(toffoli_cost)

    identity_cost = cost_func(identity_circuit)
    assert identity_cost > toffoli_cost

    xxx_cost = cost_func(xxx_circuit)
    assert xxx_cost > toffoli_cost and xxx_cost > identity_cost
