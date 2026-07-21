# 5072 - history-invariant kernel heldout matrix

Marker: `MTS_5072_HISTORY_INVARIANT_KERNEL_HELDOUT_MATRIX`.

Five cases from three independent source runs test the 5071 rule: four carry
transitions, one is a zero-transition control, chain depths reach 14, and one
case has different raw path history.

All five pass. The maximum full-versus-constructed relative difference is
`2.87e-16`, the maximum quotient-space distance is `3.14e-16`, and the maximum
difference from legacy saved kernels is `7.04e-13`. The accepted equivalence
tolerance is `1e-12`, far below the integration tolerance.

## Evidence

- Result: `source-intake/functional_rg/5072/history_invariant_kernel_heldout_matrix.json`
- Rows: `source-intake/functional_rg/5072/history_invariant_kernel_rows.csv`
- Generator: `scripts/Y5_R2FR_5072_history_invariant_kernel_heldout_matrix.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5072_VALIDATION.csv`

This authorizes the argument-topology acceleration for numerical use, not a
full-theory claim.
