# 5071 - history-invariant recursive-transition kernel replay

Marker: `MTS_5071_RECURSIVE_TRANSITION_KERNEL_REPLAY`.

The depth-ten `S503402_N0000/A10` chain exposes why exact topology correction
was not initially enough: numerical breakpoints depended on all historical
roots, including distant net-zero pairs. That made quadrature depend on a
redundant representation of the same physical winding.

With breakpoints restricted to near-path collision roots while retaining every
crossed root in the residue catalogue, full and recursively constructed
topologies give exactly the same highest-order kernel and topological
correction. The old saved value remains within the declared `5e-5` adaptive
tolerance.

## Evidence

- Result: `source-intake/functional_rg/5071/recursive_transition_kernel_replay.json`
- Full gate: `source-intake/functional_rg/5071/full_topology_kernel_gate.json`
- Constructed gate: `source-intake/functional_rg/5071/recursive_constructed_kernel_gate.json`
- Generator: `scripts/Y5_R2FR_5071_recursive_transition_kernel_replay.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5071_VALIDATION.csv`

The history-invariant breakpoint rule is an explicit opt-in candidate at this
stage.
