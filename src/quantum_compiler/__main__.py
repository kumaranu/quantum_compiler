from . import (
    CircuitIR,
    CouplingGraph,
    cancel_adjacent_inverses,
    emit_qasm2,
    expand_swaps,
    route_circuit,
)


def main() -> None:
    line = CouplingGraph(num_nodes=3, edges=[(0, 1), (1, 2)])

    prog = (
        CircuitIR(num_qubits=3)
        .add("H", 0)
        .add("CNOT", 0, 2)
        .add("CNOT", 0, 2)
        .add("CNOT", 0, 2)
    )

    opt = cancel_adjacent_inverses(prog)
    routed, final_map = route_circuit(opt, line)
    lowered = expand_swaps(routed)

    print("Original ops:", prog.ops)
    print("After cancellation:", opt.ops)
    print("After routing:", routed.ops)
    print("Final logical->physical:", final_map)
    print("\n--- Emitted OpenQASM ---")
    print(emit_qasm2(lowered))


if __name__ == "__main__":
    main()
