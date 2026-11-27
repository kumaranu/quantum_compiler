from ..ir import CircuitIR


def emit_qasm2(ir: CircuitIR) -> str:
    lines = [
        "OPENQASM 2.0;",
        'include "qelib1.inc";',
        f"qreg q[{ir.num_qubits}];",
    ]
    for gate in ir.ops:
        if gate.name == "H":
            lines.append(f"h q[{gate.qubits[0]}];")
        elif gate.name == "X":
            lines.append(f"x q[{gate.qubits[0]}];")
        elif gate.name == "CNOT":
            lines.append(f"cx q[{gate.qubits[0]}],q[{gate.qubits[1]}];")
        else:
            qubit_args = ",".join(f"q[{qubit}]" for qubit in gate.qubits)
            lines.append(f"// custom/unmapped: {gate.name}({qubit_args})")
    return "\n".join(lines)
