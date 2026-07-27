# 5047 - restricted fourth-scramble scratch matrix

Marker: `MTS_5047_RESTRICTED_FOURTH_SCRAMBLE_SCRATCH_MATRIX`.

The nine-corner pilot converges `9/9` jobs with 108 stable numerical residues
and no theorem zeros. The complete scratch run then converges `45/45` jobs with
684 stable numerical residues, no theorem zeros, no chart exclusions, and no
failed or unstable rows. Its maximum relative change from the quarantined
fourth block is `4.03598`, confirming that the scope repair is numerically
material.

The complete run authorizes replacement of the contaminated live fourth block,
subject to backup and hash verification in 5048.

## Evidence

- Pilot: `source-intake/functional_rg/5047/restricted_fourth_scramble_pilot.json`
- Matrix: `source-intake/functional_rg/5047/restricted_fourth_scramble_matrix.json`
- Comparison: `source-intake/functional_rg/5047/restricted_vs_quarantined_comparison.csv`
- Generator: `scripts/Y5_R2FR_5047_restricted_fourth_scramble_scratch_matrix.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5047_VALIDATION.csv`
