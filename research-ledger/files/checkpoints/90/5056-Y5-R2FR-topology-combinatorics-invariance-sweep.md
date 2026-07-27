# 5056 - topology combinatorics invariance sweep

Marker: `MTS_5056_TOPOLOGY_COMBINATORICS_INVARIANCE_SWEEP`.

The 240 saved `E020/E040` topology documents were split into their numerical
root signature and their discrete crossing structure. Across the 120 matched
epsilon pairs, 119 preserve the topology class, crossing multiset, pair winding
balances, and ordered crossing word. The sole exception is
`S503402_N0000/A06`. Only 29 numerical signatures are equal because the target
collision roots move with epsilon.

This rejects universal hash reuse but identifies a testable continuation route:
carry the validated crossing labels and windings from `E040`, recompute the
target roots directly at `E020`, and reserve full homotopy for structural
transitions.

## Evidence

- Result: `source-intake/functional_rg/5056/topology_combinatorics_invariance_sweep.json`
- Epsilon pairs: `source-intake/functional_rg/5056/epsilon_pair_structural_comparison.csv`
- Argument adjacency: `source-intake/functional_rg/5056/argument_adjacency_structural_comparison.csv`
- Generator: `scripts/Y5_R2FR_5056_topology_combinatorics_invariance_sweep.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5056_VALIDATION.csv`

This is an operational topology result, not amplitude or MTS evidence.
