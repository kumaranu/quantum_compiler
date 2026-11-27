from dataclasses import dataclass, field


@dataclass(frozen=True)
class Gate:
    name: str
    qubits: tuple[int, ...]
    params: tuple[float, ...] = ()


@dataclass
class CircuitIR:
    num_qubits: int
    ops: list[Gate] = field(default_factory=list)

    def add(self, name: str, *qubits: int, params: tuple[float, ...] = ()) -> "CircuitIR":
        self.ops.append(Gate(name=name, qubits=tuple(qubits), params=params))
        return self

    def copy(self) -> "CircuitIR":
        return CircuitIR(num_qubits=self.num_qubits, ops=list(self.ops))
