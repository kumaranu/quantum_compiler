# Architecture and Data Flow

The compiler converts a circuit into the package's intermediate representation,
applies optimization and lowering passes, routes it onto the available hardware
topology, and emits or verifies the result.

```mermaid
flowchart LR
    A["CircuitIR"] --> B["Optimization Passes"]
    B --> C["Routing"]
    C --> D["SWAP Lowering"]
    D --> E["OpenQASM 2 Emission"]
    D --> F["Unitary Verification"]

    subgraph IR["Intermediate Representation"]
        A
        G["Gate"]
        G --> A
    end

    subgraph Passes["Compiler Passes"]
        B
        H["Cancel Adjacent Inverses"]
        H --> B
        D
        I["Expand SWAP to 3 CNOTs"]
        I --> D
    end

    subgraph Routing["Hardware Routing"]
        J["CouplingGraph"]
        K["Initial Layout"]
        J --> C
        K --> C
    end

    subgraph Outputs["Outputs"]
        E
        F
    end
```

## Module responsibilities

| Module | Responsibility |
| --- | --- |
| `ir` | Defines `Gate` and `CircuitIR`, including circuit construction helpers |
| `passes/cancellation` | Removes adjacent identical self-inverse gates |
| `passes/lowering` | Expands routed SWAP gates into CNOT sequences |
| `routing` | Finds physical paths and updates logical-to-physical mappings |
| `emission/qasm2` | Converts lowered circuits to OpenQASM 2 text |
| `verification` | Builds a full unitary matrix for small circuits |

## Package entry point

`quantum_compiler.__main__` creates an example circuit, runs cancellation and
routing, lowers SWAP operations, and prints the resulting OpenQASM output.
