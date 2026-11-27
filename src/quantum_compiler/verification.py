import numpy as np

from .ir import CircuitIR

H_MAT = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X_MAT = np.array([[0, 1], [1, 0]], dtype=complex)
CNOT_MAT = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    dtype=complex,
)


def circuit_unitary(ir: CircuitIR) -> np.ndarray:
    """Build a full unitary matrix for a small circuit (qubit 0 is MSB)."""
    num_qubits = ir.num_qubits
    total = np.eye(2**num_qubits, dtype=complex)

    for gate in ir.ops:
        if gate.name == "H":
            single_qubit_matrix = H_MAT
        elif gate.name == "X":
            single_qubit_matrix = X_MAT
        elif gate.name == "CNOT":
            control, target = gate.qubits
            step = np.zeros((2**num_qubits, 2**num_qubits), dtype=complex)
            for column in range(2**num_qubits):
                bits = [
                    (column >> (num_qubits - 1 - qubit)) & 1
                    for qubit in range(num_qubits)
                ]
                if bits[control] == 1:
                    bits[target] ^= 1
                output = sum(
                    bit << (num_qubits - 1 - qubit)
                    for qubit, bit in enumerate(bits)
                )
                step[output, column] = 1.0
            total = step @ total
            continue
        else:
            raise ValueError(f"Unitary not defined for {gate.name}")

        target = gate.qubits[0]
        matrices = [
            single_qubit_matrix if qubit == target else np.eye(2, dtype=complex)
            for qubit in range(num_qubits)
        ]
        step = matrices[0]
        for matrix in matrices[1:]:
            step = np.kron(step, matrix)
        total = step @ total

    return total
