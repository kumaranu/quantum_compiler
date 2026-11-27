# quantum-compiler

A small Python package for quantum circuit optimization, routing, SWAP expansion,
and OpenQASM 2 emission.

**See the [architecture and data-flow diagram](docs/architecture.md) for how the
package transforms and emits circuits.**

## Modules

- `ir`: `Gate` and `CircuitIR` data models
- `passes`: optimization and lowering passes
- `routing`: coupling graphs and layout/routing
- `emission`: circuit output formats
- `verification`: small-circuit unitary construction

## Run

```bash
python -m quantum_compiler
```

## Build

```bash
python -m pip install .
quantum-compiler
```
