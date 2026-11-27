import unittest

from quantum_compiler import (
    CircuitIR,
    CouplingGraph,
    cancel_adjacent_inverses,
    emit_qasm2,
    expand_swaps,
    route_circuit,
)
from quantum_compiler.ir import Gate
from quantum_compiler.verification import circuit_unitary


class ModularPackageTests(unittest.TestCase):
    def test_public_models_and_cancellation(self) -> None:
        circuit = (
            CircuitIR(num_qubits=2)
            .add("H", 0)
            .add("CNOT", 0, 1)
            .add("CNOT", 0, 1)
        )

        result = cancel_adjacent_inverses(circuit)

        self.assertEqual(result.ops, [Gate("H", (0,))])

    def test_routing_and_lowering(self) -> None:
        circuit = CircuitIR(num_qubits=3).add("CNOT", 0, 2)
        coupling = CouplingGraph(num_nodes=3, edges=[(0, 1), (1, 2)])

        routed, final_layout = route_circuit(circuit, coupling)
        lowered = expand_swaps(routed)

        self.assertEqual(lowered.ops[0].name, "CNOT")
        self.assertEqual(len(lowered.ops), 4)
        self.assertEqual(final_layout, {0: 1, 1: 0, 2: 2})
        self.assertIn("cx q[1],q[2];", emit_qasm2(lowered))
        self.assertEqual(lowered.num_qubits, 3)

    def test_unitary_helper(self) -> None:
        circuit = CircuitIR(num_qubits=1).add("X", 0)

        unitary = circuit_unitary(circuit)

        self.assertEqual(unitary.shape, (2, 2))


if __name__ == "__main__":
    unittest.main()
