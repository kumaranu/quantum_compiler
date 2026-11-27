from ..ir import CircuitIR, Gate

SELF_INVERSE = {"H", "X", "Y", "Z", "CNOT", "SWAP"}


def _touches_any(gate: Gate, target_qubits: set[int]) -> bool:
    return any(q in target_qubits for q in gate.qubits)


def cancel_adjacent_inverses(ir: CircuitIR) -> CircuitIR:
    """Remove pairs of identical self-inverse gates without intervening touches."""
    ops = list(ir.ops)
    i = 0
    out: list[Gate] = []

    while i < len(ops):
        gate = ops[i]
        if gate.name in SELF_INVERSE:
            target_qubits = set(gate.qubits)
            match_index = None
            for candidate_index in range(i + 1, len(ops)):
                candidate = ops[candidate_index]
                if candidate == gate:
                    match_index = candidate_index
                    break
                if _touches_any(candidate, target_qubits):
                    break

            if match_index is not None:
                out.extend(ops[i + 1 : match_index])
                i = match_index + 1
                continue

        out.append(gate)
        i += 1

    return CircuitIR(num_qubits=ir.num_qubits, ops=out)
