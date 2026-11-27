from ..ir import CircuitIR, Gate


def expand_swaps(ir: CircuitIR) -> CircuitIR:
    """Expand each SWAP gate into three CNOT gates."""
    expanded: list[Gate] = []
    for gate in ir.ops:
        if gate.name == "SWAP":
            a, b = gate.qubits
            expanded.extend([
                Gate("CNOT", (a, b)),
                Gate("CNOT", (b, a)),
                Gate("CNOT", (a, b)),
            ])
        else:
            expanded.append(gate)
    return CircuitIR(num_qubits=ir.num_qubits, ops=expanded)
