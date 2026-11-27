from collections import deque

from .ir import CircuitIR, Gate


class CouplingGraph:
    def __init__(self, num_nodes: int, edges: list[tuple[int, int]]):
        self.num_nodes = num_nodes
        self.adj: dict[int, set[int]] = {i: set() for i in range(num_nodes)}
        for u, v in edges:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def shortest_path(self, start: int, goal: int) -> list[int]:
        if start == goal:
            return [start]
        queue = deque([[start]])
        visited = {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            for nxt in sorted(self.adj[node]):
                if nxt == goal:
                    return path + [nxt]
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(path + [nxt])
        raise ValueError(f"No path between physical qubits {start} and {goal}")


def route_circuit(
    ir: CircuitIR,
    coupling: CouplingGraph,
    initial_layout: dict[int, int] | None = None,
) -> tuple[CircuitIR, dict[int, int]]:
    """Route gates onto physical qubits and return the final logical-to-physical map."""
    if coupling.num_nodes < ir.num_qubits:
        raise ValueError("Coupling graph has fewer nodes than logical qubits.")

    l2p = dict(initial_layout) if initial_layout else {q: q for q in range(ir.num_qubits)}
    p2l: dict[int, int | None] = {p: None for p in range(coupling.num_nodes)}
    for logical_qubit, physical_qubit in l2p.items():
        p2l[physical_qubit] = logical_qubit

    routed_ops: list[Gate] = []

    for gate in ir.ops:
        if len(gate.qubits) == 1:
            physical_qubit = l2p[gate.qubits[0]]
            routed_ops.append(Gate(name=gate.name, qubits=(physical_qubit,), params=gate.params))
        elif len(gate.qubits) == 2:
            logical_left, logical_right = gate.qubits
            physical_left, physical_right = l2p[logical_left], l2p[logical_right]
            path = coupling.shortest_path(physical_left, physical_right)

            while len(path) > 2:
                left, right = path[0], path[1]
                routed_ops.append(Gate(name="SWAP", qubits=(left, right)))

                logical_at_left, logical_at_right = p2l[left], p2l[right]
                p2l[left], p2l[right] = logical_at_right, logical_at_left
                if logical_at_left is not None:
                    l2p[logical_at_left] = right
                if logical_at_right is not None:
                    l2p[logical_at_right] = left

                physical_left = l2p[logical_left]
                path = coupling.shortest_path(physical_left, physical_right)

            routed_ops.append(
                Gate(name=gate.name, qubits=(physical_left, physical_right), params=gate.params)
            )
        else:
            raise NotImplementedError(f"Gates with {len(gate.qubits)} qubits not supported yet.")

    return CircuitIR(num_qubits=coupling.num_nodes, ops=routed_ops), l2p
